#!/usr/bin/env python3
"""Registry de nós Sínkra v1: validar, promover e resolver sem dependências."""

from __future__ import annotations

import argparse
import contextlib
import copy
import datetime as dt
import hashlib
import json
import os
import re
import sys
import uuid
from pathlib import Path
from typing import Any, Iterator


NODE_SCHEMA = "sinkra-node@1"
CANDIDATE_SCHEMA = "sinkra-node-candidate@1"
COMPOSITION_SCHEMA = "sinkra-composition@1"
RUNTIME_SCHEMA = "sinkra-runtime@1"
EVIDENCE_SCHEMA = "sinkra-evidence@1"
RELATION_SCHEMA = "sinkra-relation@1"
PLAN_SCHEMA = "sinkra-promotion-plan@1"
DECISION_SCHEMA = "sinkra-promotion-decision@1"
ENTRY_SCHEMA = "sinkra-registry-entry@1"
AUDIT_SCHEMA = "sinkra-promotion-audit@1"

DEFINITION_KINDS = {
    "entity", "stage", "task", "rule", "heuristic", "process", "template",
    "artifact", "idea", "blocker",
}
COMPOSITION_KINDS = {"lifecycle", "workflow", "full-cycle", "bundle"}
RUNTIME_KINDS = {
    "entity-instance", "cycle-run", "task-run", "stage-event", "artifact-instance",
}
EVIDENCE_KINDS = {"source", "excerpt", "media", "report"}
PROMOTION_ACTIONS = {"promote-new", "promote-version", "hold", "archive"}
RELATION_SCOPES = {"constitutive", "semantic"}
CONTEXT_FIELDS = {"parent", "order", "position", "role", "when", "params"}
TASK_FIELDS = {"verb", "executor", "inputs", "outputs", "preconditions", "completion"}
REF_RE = re.compile(r"^[A-Z][A-Za-z0-9-]+@([1-9][0-9]*)$")
CANDIDATE_RE = re.compile(r"^CAND-[A-Z0-9-]+-[0-9]{4,}$")


class RegistryError(Exception):
    def __init__(self, message: str, code: int = 2):
        super().__init__(message)
        self.code = code


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise RegistryError(f"JSON inválido em {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise RegistryError(f"Objeto JSON esperado em {path}")
    return value


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    number = 0
    try:
        for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not raw.strip():
                continue
            value = json.loads(raw)
            if not isinstance(value, dict):
                raise ValueError("linha não contém objeto")
            rows.append(value)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        raise RegistryError(f"JSONL inválido em {path}:{number}: {exc}") from exc
    return rows


def render_jsonl(rows: list[dict[str, Any]]) -> bytes:
    text = "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows)
    return text.encode("utf-8")


def parse_markdown(path: Path) -> tuple[dict[str, Any], str]:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise RegistryError(f"Markdown ilegível em {path}: {exc}") from exc
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise RegistryError(f"Frontmatter JSON ausente em {path}")
    try:
        end = next(index for index, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration as exc:
        raise RegistryError(f"Frontmatter sem fechamento em {path}") from exc
    try:
        metadata = json.loads("\n".join(lines[1:end]))
    except json.JSONDecodeError as exc:
        raise RegistryError(
            f"Frontmatter de {path} deve ser JSON válido; normalize entradas legadas: {exc}"
        ) from exc
    if not isinstance(metadata, dict):
        raise RegistryError(f"Frontmatter deve ser objeto em {path}")
    body = "\n".join(lines[end + 1 :]).strip("\n")
    return metadata, body


def render_markdown(metadata: dict[str, Any], body: str) -> bytes:
    head = json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True)
    suffix = f"\n\n{body.rstrip()}\n" if body.strip() else "\n"
    return f"---\n{head}\n---{suffix}".encode("utf-8")


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp-{uuid.uuid4()}")
    try:
        with temporary.open("xb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


@contextlib.contextmanager
def registry_lock(registry: Path) -> Iterator[None]:
    registry.mkdir(parents=True, exist_ok=True)
    lock = registry / ".promotion.lock"
    try:
        lock.mkdir()
    except FileExistsError as exc:
        raise RegistryError(f"Registry bloqueado por {lock}", code=5) from exc
    try:
        atomic_write(
            lock / "owner.json",
            json.dumps({"pid": os.getpid(), "created_at": utc_now()}, sort_keys=True).encode("utf-8"),
        )
        yield
    finally:
        (lock / "owner.json").unlink(missing_ok=True)
        try:
            lock.rmdir()
        except OSError:
            pass


def require_text(meta: dict[str, Any], key: str, where: str, errors: list[str]) -> None:
    if not isinstance(meta.get(key), str) or not meta[key].strip():
        errors.append(f"{where}: campo textual obrigatório `{key}` ausente")


def validate_metadata(meta: dict[str, Any], where: str) -> list[str]:
    errors: list[str] = []
    object_class = meta.get("object_class")
    kind = meta.get("kind")
    if object_class not in {"definition", "composition", "runtime", "evidence"}:
        errors.append(f"{where}: object_class inválido: {object_class!r}")
        return errors
    require_text(meta, "kind", where, errors)

    if kind == "cycle":
        errors.append(f"{where}: normalize `cycle` como lifecycle, full-cycle ou cycle-run")
    if kind == "verification":
        errors.append(f"{where}: use kind task com capability verification")

    schema = meta.get("schema")
    if object_class == "definition":
        if kind not in DEFINITION_KINDS:
            errors.append(f"{where}: kind de definição inválido: {kind!r}")
        if schema == CANDIDATE_SCHEMA:
            require_text(meta, "candidate_id", where, errors)
            if isinstance(meta.get("candidate_id"), str) and not CANDIDATE_RE.match(meta["candidate_id"]):
                errors.append(f"{where}: candidate_id inválido: {meta['candidate_id']}")
            if meta.get("status") != "candidate":
                errors.append(f"{where}: candidato deve usar status candidate")
        elif schema == NODE_SCHEMA:
            require_text(meta, "object_id", where, errors)
            if not isinstance(meta.get("version"), int) or meta["version"] < 1:
                errors.append(f"{where}: version deve ser inteiro positivo")
        else:
            errors.append(f"{where}: schema de definição inválido: {schema!r}")
        require_text(meta, "name", where, errors)
        if not isinstance(meta.get("contract"), dict):
            errors.append(f"{where}: contract deve ser objeto")
        if not isinstance(meta.get("capabilities", []), list):
            errors.append(f"{where}: capabilities deve ser lista")
        if not isinstance(meta.get("aliases", []), list):
            errors.append(f"{where}: aliases deve ser lista")
        if not isinstance(meta.get("constraints", []), list):
            errors.append(f"{where}: constraints deve ser lista")
        if not isinstance(meta.get("provenance", []), list):
            errors.append(f"{where}: provenance deve ser lista")
        if meta.get("reuse_policy") != "reusable":
            errors.append(f"{where}: definição deve usar reuse_policy reusable")
        for field in sorted(CONTEXT_FIELDS.intersection(meta)):
            errors.append(f"{where}: `{field}` pertence ao binding, não à definição")
        if kind == "task" and isinstance(meta.get("contract"), dict):
            missing = sorted(TASK_FIELDS.difference(meta["contract"]))
            if missing:
                errors.append(f"{where}: contrato de task sem {', '.join(missing)}")
            for field in ("inputs", "outputs", "preconditions", "completion"):
                if field in meta["contract"] and not isinstance(meta["contract"][field], list):
                    errors.append(f"{where}: contract.{field} deve ser lista")
    elif object_class == "composition":
        if schema != COMPOSITION_SCHEMA:
            errors.append(f"{where}: schema de composição inválido: {schema!r}")
        if kind not in COMPOSITION_KINDS:
            errors.append(f"{where}: kind de composição inválido: {kind!r}")
        require_text(meta, "composition_id", where, errors)
        if not isinstance(meta.get("version"), int) or meta["version"] < 1:
            errors.append(f"{where}: version deve ser inteiro positivo")
        require_text(meta, "status", where, errors)
        if not isinstance(meta.get("bindings"), list):
            errors.append(f"{where}: bindings deve ser lista")
        else:
            for index, binding in enumerate(meta["bindings"]):
                label = f"{where}: binding {index + 1}"
                if not isinstance(binding, dict):
                    errors.append(f"{label} deve ser objeto")
                    continue
                require_text(binding, "ref", label, errors)
                require_text(binding, "role", label, errors)
                if "when" in binding and binding["when"] is not None:
                    when = binding["when"]
                    if not isinstance(when, dict) or not when.get("condition") or not when.get("evaluator"):
                        errors.append(f"{label}: when exige condition e evaluator")
                if "params" in binding and not isinstance(binding["params"], dict):
                    errors.append(f"{label}: params deve ser objeto")
    elif object_class == "runtime":
        if schema != RUNTIME_SCHEMA:
            errors.append(f"{where}: schema de runtime inválido: {schema!r}")
        if kind not in RUNTIME_KINDS:
            errors.append(f"{where}: kind de runtime inválido: {kind!r}")
        require_text(meta, "runtime_id", where, errors)
        require_text(meta, "definition_ref", where, errors)
        require_text(meta, "status", where, errors)
        require_text(meta, "recorded_at", where, errors)
        if not isinstance(meta.get("evidence_refs"), list):
            errors.append(f"{where}: evidence_refs deve ser lista")
        if meta.get("reuse_policy") == "reusable":
            errors.append(f"{where}: runtime nunca é reutilizável")
        if kind == "cycle-run" and meta.get("status") == "cancelled":
            if not meta.get("entity_last_stage_ref"):
                errors.append(f"{where}: cycle-run cancelado exige entity_last_stage_ref")
            open_states = {"todo", "ready", "active", "in-progress", "running"}
            for task in meta.get("tasks", []):
                if isinstance(task, dict) and task.get("status") in open_states:
                    errors.append(f"{where}: task aberta em cycle-run cancelado")
    else:
        if schema != EVIDENCE_SCHEMA:
            errors.append(f"{where}: schema de evidência inválido: {schema!r}")
        if kind not in EVIDENCE_KINDS:
            errors.append(f"{where}: kind de evidência inválido: {kind!r}")
        require_text(meta, "evidence_id", where, errors)
        require_text(meta, "source", where, errors)
        require_text(meta, "locator", where, errors)
        require_text(meta, "captured_at", where, errors)
    return errors


def validate_relation(row: dict[str, Any], where: str) -> list[str]:
    errors: list[str] = []
    if row.get("schema") != RELATION_SCHEMA:
        errors.append(f"{where}: schema de relação inválido")
    for key in ("from_ref", "type", "to_ref"):
        require_text(row, key, where, errors)
    if row.get("scope") not in RELATION_SCOPES:
        errors.append(f"{where}: scope deve ser constitutive ou semantic")
    return errors


def _load_markdown_group(paths: list[Path], errors: list[str]) -> list[tuple[Path, dict[str, Any], str]]:
    docs: list[tuple[Path, dict[str, Any], str]] = []
    for path in paths:
        try:
            meta, body = parse_markdown(path)
        except RegistryError as exc:
            errors.append(str(exc))
            continue
        errors.extend(validate_metadata(meta, str(path)))
        docs.append((path, meta, body))
    return docs


def load_bundle(root: Path) -> tuple[
    dict[str, tuple[Path, dict[str, Any], str]],
    list[tuple[Path, dict[str, Any], str]],
    list[tuple[Path, dict[str, Any]]],
    list[tuple[Path, dict[str, Any], str]],
    list[dict[str, Any]],
    list[str],
]:
    errors: list[str] = []
    candidate_paths = sorted((root / "candidates").glob("*.md"))
    candidate_paths += sorted((root / "node-candidates").glob("*.md"))
    docs = _load_markdown_group(candidate_paths, errors)
    candidates: dict[str, tuple[Path, dict[str, Any], str]] = {}
    for path, meta, body in docs:
        candidate_id = meta.get("candidate_id")
        if isinstance(candidate_id, str):
            if candidate_id in candidates:
                errors.append(f"candidate_id duplicado: {candidate_id}")
            candidates[candidate_id] = (path, meta, body)

    compositions = _load_markdown_group(sorted((root / "compositions").glob("*.md")), errors)
    runtimes: list[tuple[Path, dict[str, Any]]] = []
    for path in sorted((root / "runtime").glob("*.json")):
        try:
            meta = read_json(path)
        except RegistryError as exc:
            errors.append(str(exc))
            continue
        errors.extend(validate_metadata(meta, str(path)))
        runtimes.append((path, meta))
    evidences = _load_markdown_group(sorted((root / "evidence").glob("*.md")), errors)
    for path in sorted((root / "evidence").glob("*.json")):
        try:
            meta = read_json(path)
        except RegistryError as exc:
            errors.append(str(exc))
            continue
        errors.extend(validate_metadata(meta, str(path)))
        evidences.append((path, meta, ""))

    try:
        relations = read_jsonl(root / "relations.jsonl")
    except RegistryError as exc:
        errors.append(str(exc))
        relations = []
    for index, relation in enumerate(relations, 1):
        errors.extend(validate_relation(relation, f"{root / 'relations.jsonl'}:{index}"))
    return candidates, compositions, runtimes, evidences, relations, errors


def bundle_integrity(root: Path, external_registry: Path | None = None) -> dict[str, Any]:
    candidates, compositions, runtimes, evidences, relations, errors = load_bundle(root)
    warnings: list[str] = []
    composition_ids = {
        meta.get("composition_id") for _, meta, _ in compositions if meta.get("composition_id")
    }
    runtime_ids = {meta.get("runtime_id") for _, meta in runtimes if meta.get("runtime_id")}
    evidence_ids = {meta.get("evidence_id") for _, meta, _ in evidences if meta.get("evidence_id")}
    known = set(candidates) | composition_ids | runtime_ids | evidence_ids
    canonical_refs: set[str] = set()
    if external_registry is not None:
        registry_report = registry_integrity(external_registry)
        if registry_report["errors"]:
            errors.extend(f"Registry externo: {error}" for error in registry_report["errors"])
        else:
            canonical_refs = {entry.get("ref") for entry in load_registry(external_registry)[0]}

    def check_ref(ref: Any, where: str) -> None:
        if not isinstance(ref, str) or not ref:
            errors.append(f"{where}: referência ausente")
        elif ref.startswith("CAND-") or "@" not in ref:
            if ref not in known:
                errors.append(f"{where}: referência local inexistente: {ref}")
        elif REF_RE.match(ref):
            if external_registry is None:
                errors.append(f"{where}: referência canônica não verificável sem --registry: {ref}")
            elif ref not in canonical_refs:
                errors.append(f"{where}: referência canônica inexistente: {ref}")
        else:
            errors.append(f"{where}: formato de referência inválido: {ref}")
    lifecycle_ids = {
        meta.get("composition_id") for _, meta, _ in compositions if meta.get("kind") == "lifecycle"
    }
    bound_all: set[str] = set()
    bound_active: set[str] = set()
    lifecycle_stages: set[str] = set()
    for _, composition, _ in compositions:
        for binding in composition.get("bindings", []):
            if not isinstance(binding, dict) or not isinstance(binding.get("ref"), str):
                continue
            ref = binding["ref"]
            bound_all.add(ref)
            if composition.get("status") != "cancelled":
                bound_active.add(ref)
            if composition.get("kind") == "lifecycle":
                lifecycle_stages.add(ref)
            check_ref(ref, "composição")

    relation_refs: set[str] = set()
    constitutive_stage_refs: set[str] = set()
    for relation in relations:
        source = relation.get("from_ref")
        target = relation.get("to_ref")
        if isinstance(source, str):
            relation_refs.add(source)
        if isinstance(target, str):
            relation_refs.add(target)
        for ref in (source, target):
            check_ref(ref, "relação")
        if (
            relation.get("scope") == "constitutive"
            and relation.get("type") in {"belongs-to", "belongs_to"}
            and target in lifecycle_ids
            and isinstance(source, str)
        ):
            constitutive_stage_refs.add(source)

    for candidate_id, (_, meta, _) in candidates.items():
        if meta.get("kind") == "stage" and candidate_id not in lifecycle_stages | constitutive_stage_refs:
            errors.append(f"{candidate_id}: StageDefinition sem lifecycle")
        if candidate_id not in bound_active | relation_refs:
            warnings.append(f"unreferenced: {candidate_id}")

    for path, runtime in runtimes:
        ref = runtime.get("definition_ref")
        check_ref(ref, f"{path}: definition_ref")
        if runtime.get("entity_last_stage_ref"):
            check_ref(runtime["entity_last_stage_ref"], f"{path}: entity_last_stage_ref")
        for evidence_ref in runtime.get("evidence_refs", []):
            if evidence_ref not in evidence_ids:
                errors.append(f"{path}: evidence_ref inexistente: {evidence_ref}")

    return {
        "target": str(root),
        "kind": "bundle",
        "counts": {
            "candidates": len(candidates),
            "compositions": len(compositions),
            "runtime": len(runtimes),
            "evidence": len(evidences),
            "relations": len(relations),
        },
        "errors": sorted(set(errors)),
        "warnings": sorted(set(warnings)),
    }


def registry_paths(registry: Path) -> tuple[Path, Path, Path]:
    return registry / "registry.jsonl", registry / "relations.jsonl", registry / "audit" / "promotions.jsonl"


def load_registry(registry: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    index_path, relations_path, audit_path = registry_paths(registry)
    return read_jsonl(index_path), read_jsonl(relations_path), read_jsonl(audit_path)


def safe_registry_path(registry: Path, relative: str) -> Path:
    path = (registry / relative).resolve()
    if not path.is_relative_to(registry.resolve()):
        raise RegistryError(f"caminho escapa do Registry: {relative}")
    return path


def registry_integrity(registry: Path) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        entries, relations, audits = load_registry(registry)
    except RegistryError as exc:
        return {"target": str(registry), "kind": "registry", "counts": {}, "errors": [str(exc)], "warnings": []}

    refs: set[str] = set()
    indexed_paths: set[Path] = set()
    for index, entry in enumerate(entries, 1):
        where = f"registry.jsonl:{index}"
        if entry.get("schema") != ENTRY_SCHEMA:
            errors.append(f"{where}: schema de índice inválido")
        ref = entry.get("ref")
        if not isinstance(ref, str) or not REF_RE.match(ref):
            errors.append(f"{where}: ref canônica inválida: {ref!r}")
            continue
        if ref in refs:
            errors.append(f"{where}: ref duplicada: {ref}")
        refs.add(ref)
        relative = entry.get("path")
        if not isinstance(relative, str):
            errors.append(f"{where}: path ausente")
            continue
        try:
            path = safe_registry_path(registry, relative)
        except RegistryError as exc:
            errors.append(str(exc))
            continue
        indexed_paths.add(path)
        if not path.is_file():
            errors.append(f"{where}: objeto ausente: {relative}")
            continue
        if entry.get("sha256") != sha256_file(path):
            errors.append(f"{where}: hash divergente: {ref}")
        try:
            meta, _ = parse_markdown(path)
        except RegistryError as exc:
            errors.append(str(exc))
            continue
        errors.extend(validate_metadata(meta, str(path)))
        if f"{meta.get('object_id')}@{meta.get('version')}" != ref:
            errors.append(f"{where}: índice e frontmatter divergem para {ref}")

    for index, relation in enumerate(relations, 1):
        where = f"relations.jsonl:{index}"
        errors.extend(validate_relation(relation, where))
        for endpoint in (relation.get("from_ref"), relation.get("to_ref")):
            if endpoint not in refs:
                errors.append(f"{where}: referência inexistente: {endpoint}")

    for path in sorted((registry / "objects").glob("*/v*.md")) if (registry / "objects").exists() else []:
        if path.resolve() not in indexed_paths:
            warnings.append(f"objeto sem índice: {path.relative_to(registry).as_posix()}")
    return {
        "target": str(registry),
        "kind": "registry",
        "counts": {"objects": len(entries), "relations": len(relations), "promotions": len(audits)},
        "errors": sorted(set(errors)),
        "warnings": sorted(set(warnings)),
    }


def is_registry(path: Path) -> bool:
    return (path / "registry.jsonl").exists() or (path / "objects").exists() or (path / "audit").exists()


def command_validate(target: Path, external_registry: Path | None = None) -> int:
    if not target.is_dir():
        raise RegistryError(f"diretório inexistente: {target}")
    report = registry_integrity(target) if is_registry(target) else bundle_integrity(target, external_registry)
    report["status"] = "valid" if not report["errors"] else "invalid"
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not report["errors"] else 1


def validate_plan(plan: dict[str, Any], where: str) -> list[str]:
    errors: list[str] = []
    if plan.get("schema") != PLAN_SCHEMA:
        errors.append(f"{where}: schema de plano inválido")
    if not isinstance(plan.get("items"), list):
        errors.append(f"{where}: items deve ser lista")
        return errors
    seen: set[str] = set()
    for index, item in enumerate(plan["items"], 1):
        label = f"{where}: item {index}"
        if not isinstance(item, dict):
            errors.append(f"{label} deve ser objeto")
            continue
        candidate_id = item.get("candidate_id")
        if not isinstance(candidate_id, str):
            errors.append(f"{label}: candidate_id ausente")
        elif candidate_id in seen:
            errors.append(f"{label}: candidate_id duplicado: {candidate_id}")
        else:
            seen.add(candidate_id)
        action = item.get("action")
        if action not in PROMOTION_ACTIONS:
            errors.append(f"{label}: action inválida: {action!r}")
        if action == "promote-version" and not item.get("target_object_id"):
            errors.append(f"{label}: promote-version exige target_object_id")
    if "relations" in plan and not isinstance(plan["relations"], list):
        errors.append(f"{where}: relations deve ser lista")
    return errors


def validate_decision(decision: dict[str, Any], plan_hash: str, by: str, where: str) -> list[str]:
    errors: list[str] = []
    if decision.get("schema") != DECISION_SCHEMA:
        errors.append(f"{where}: schema de decisão inválido")
    if decision.get("status") != "approved":
        errors.append(f"{where}: decisão não aprovada")
    if decision.get("plan_sha256") != plan_hash:
        errors.append(f"{where}: hash do plano divergente")
    if decision.get("decided_by") != by:
        errors.append(f"{where}: --by difere de decided_by")
    require_text(decision, "decided_at", where, errors)
    if not isinstance(decision.get("approved_items"), list):
        errors.append(f"{where}: approved_items deve ser lista")
    return errors


def exact_ref_exists(entries: list[dict[str, Any]], ref: str) -> bool:
    return any(entry.get("ref") == ref for entry in entries)


def next_version(entries: list[dict[str, Any]], object_id: str) -> int:
    versions = [entry["version"] for entry in entries if entry.get("object_id") == object_id]
    if not versions:
        raise RegistryError(f"objeto alvo inexistente: {object_id}")
    return max(versions) + 1


def canonical_id(kind: str) -> str:
    token = re.sub(r"[^A-Z0-9]+", "-", kind.upper()).strip("-")
    return f"NODE-{token}-{uuid.uuid4()}"


def _selected_candidates(
    plan: dict[str, Any], decision: dict[str, Any], candidates: dict[str, tuple[Path, dict[str, Any], str]]
) -> list[tuple[dict[str, Any], Path, dict[str, Any], str]]:
    approved = set(decision.get("approved_items", []))
    selected: list[tuple[dict[str, Any], Path, dict[str, Any], str]] = []
    planned_ids = {item.get("candidate_id") for item in plan.get("items", []) if isinstance(item, dict)}
    unknown_approved = approved.difference(planned_ids)
    if unknown_approved:
        raise RegistryError(f"decisão aprova itens fora do plano: {', '.join(sorted(unknown_approved))}", code=3)
    for item in plan.get("items", []):
        candidate_id = item.get("candidate_id")
        if candidate_id not in candidates:
            raise RegistryError(f"candidato do plano não encontrado: {candidate_id}")
        action = item.get("action")
        if action not in {"promote-new", "promote-version"}:
            continue
        if candidate_id not in approved:
            continue
        path, meta, body = candidates[candidate_id]
        if meta.get("object_class") != "definition":
            raise RegistryError(f"{candidate_id}: somente definition pode ser promovida")
        errors = validate_metadata(meta, str(path))
        if errors:
            raise RegistryError("; ".join(errors))
        selected.append((item, path, meta, body))
    return selected


def _ensure_selected_stages_have_lifecycle(
    selected: list[tuple[dict[str, Any], Path, dict[str, Any], str]],
    compositions: list[tuple[Path, dict[str, Any], str]],
    relations: list[dict[str, Any]],
) -> None:
    valid_lifecycles = [
        (path, meta, body)
        for path, meta, body in compositions
        if meta.get("kind") == "lifecycle" and not validate_metadata(meta, str(path))
    ]
    lifecycle_ids = {
        meta.get("composition_id") for _, meta, _ in valid_lifecycles
    }
    bound = {
        binding.get("ref")
        for _, meta, _ in valid_lifecycles
        for binding in meta.get("bindings", [])
        if isinstance(binding, dict)
    }
    related = {
        relation.get("from_ref")
        for relation in relations
        if relation.get("scope") == "constitutive"
        and relation.get("type") in {"belongs-to", "belongs_to"}
        and relation.get("to_ref") in lifecycle_ids
    }
    for _, _, meta, _ in selected:
        if meta.get("kind") == "stage" and meta.get("candidate_id") not in bound | related:
            raise RegistryError(f"{meta.get('candidate_id')}: StageDefinition sem lifecycle")


def _restore(path: Path, previous: bytes | None) -> None:
    if previous is None:
        path.unlink(missing_ok=True)
    else:
        atomic_write(path, previous)


def promote(plan_path: Path, registry: Path, decision_path: Path, by: str, dry_run: bool) -> dict[str, Any]:
    plan_raw = plan_path.read_bytes()
    plan_hash = sha256_bytes(plan_raw)
    plan = read_json(plan_path)
    decision = read_json(decision_path)
    errors = validate_plan(plan, str(plan_path)) + validate_decision(decision, plan_hash, by, str(decision_path))
    if errors:
        raise RegistryError("; ".join(errors), code=3)

    bundle = plan_path.parent
    candidates, compositions, _, _, local_relations, load_errors = load_bundle(bundle)
    if load_errors:
        selected_ids = {
            item.get("candidate_id")
            for item in plan.get("items", [])
            if isinstance(item, dict)
            and item.get("action") in {"promote-new", "promote-version"}
            and item.get("candidate_id") in set(decision.get("approved_items", []))
        }
        relevant = [error for error in load_errors if any(candidate_id in error for candidate_id in selected_ids)]
        if relevant:
            raise RegistryError("; ".join(relevant))
    selected = _selected_candidates(plan, decision, candidates)
    _ensure_selected_stages_have_lifecycle(selected, compositions, local_relations)

    if not selected:
        held = [
            item.get("candidate_id")
            for item in plan.get("items", [])
            if isinstance(item, dict) and item.get("action") in {"hold", "archive"}
        ]
        return {"status": "unchanged", "reason": "no-approved-promotions", "held": held}

    if is_registry(registry):
        integrity = registry_integrity(registry)
        if integrity["errors"]:
            raise RegistryError("Registry inválido antes da promoção: " + "; ".join(integrity["errors"]))
    entries, global_relations, audits = load_registry(registry)
    repeated = next((audit for audit in audits if audit.get("plan_sha256") == plan_hash), None)
    if repeated:
        return {"status": "unchanged", "reason": "plan-already-promoted", "audit": repeated}

    prepared: list[dict[str, Any]] = []
    mapping: dict[str, str] = {}
    staged_entries = copy.deepcopy(entries)
    for item, source_path, candidate, body in selected:
        candidate_id = candidate["candidate_id"]
        source_hash = sha256_file(source_path)
        target = item.get("target_object_id") if item["action"] == "promote-version" else None
        prior = next(
            (
                entry for entry in staged_entries
                if entry.get("source_candidate_id") == candidate_id
                and entry.get("source_sha256") == source_hash
                and (target is None or entry.get("object_id") == target)
            ),
            None,
        )
        if prior:
            mapping[candidate_id] = prior["ref"]
            continue
        if item["action"] == "promote-new":
            object_id = canonical_id(candidate["kind"])
            version = 1
            supersedes = None
        else:
            object_id = str(target)
            version = next_version(staged_entries, object_id)
            previous = next(
                entry for entry in staged_entries
                if entry.get("object_id") == object_id and entry.get("version") == version - 1
            )
            if previous.get("kind") != candidate.get("kind"):
                raise RegistryError(f"{candidate_id}: kind diverge do objeto {object_id}")
            supersedes = previous["ref"]
        ref = f"{object_id}@{version}"
        canonical = copy.deepcopy(candidate)
        canonical.pop("candidate_id", None)
        canonical.update(
            {
                "schema": NODE_SCHEMA,
                "object_id": object_id,
                "version": version,
                "status": "stable",
                "promoted_from": candidate_id,
            }
        )
        if supersedes:
            canonical["supersedes"] = supersedes
        content = render_markdown(canonical, body)
        relative = Path("objects") / object_id / f"v{version}.md"
        entry = {
            "schema": ENTRY_SCHEMA,
            "ref": ref,
            "object_id": object_id,
            "version": version,
            "kind": canonical["kind"],
            "name": canonical["name"],
            "status": canonical["status"],
            "aliases": canonical.get("aliases", []),
            "capabilities": canonical.get("capabilities", []),
            "path": relative.as_posix(),
            "sha256": sha256_bytes(content),
            "source_candidate_id": candidate_id,
            "source_sha256": source_hash,
            "promoted_at": utc_now(),
            "promoted_by": by,
        }
        prepared.append({"entry": entry, "content": content, "relative": relative, "supersedes": supersedes})
        staged_entries.append(entry)
        mapping[candidate_id] = ref

    if dry_run:
        return {
            "status": "dry-run",
            "selected": [item[2]["candidate_id"] for item in selected],
            "would_create": [item["entry"]["ref"] for item in prepared],
            "would_reuse": {key: value for key, value in mapping.items() if value not in {p["entry"]["ref"] for p in prepared}},
        }

    decision_hash = sha256_file(decision_path)
    index_path, relations_path, audit_path = registry_paths(registry)
    with registry_lock(registry):
        integrity = registry_integrity(registry)
        if integrity["errors"]:
            raise RegistryError("Registry inválido durante a promoção: " + "; ".join(integrity["errors"]))
        entries, global_relations, audits = load_registry(registry)
        repeated = next((audit for audit in audits if audit.get("plan_sha256") == plan_hash), None)
        if repeated:
            return {"status": "unchanged", "reason": "plan-already-promoted", "audit": repeated}
        deduplicated: list[dict[str, Any]] = []
        for prepared_item in prepared:
            entry = prepared_item["entry"]
            prior = next(
                (
                    current for current in entries
                    if current.get("source_candidate_id") == entry.get("source_candidate_id")
                    and current.get("source_sha256") == entry.get("source_sha256")
                    and (
                        prepared_item["supersedes"] is None
                        or current.get("object_id") == entry.get("object_id")
                    )
                ),
                None,
            )
            if prior:
                mapping[entry["source_candidate_id"]] = prior["ref"]
            else:
                deduplicated.append(prepared_item)
        prepared = deduplicated
        for prepared_item in prepared:
            ref = prepared_item["entry"]["ref"]
            if any(entry.get("ref") == ref for entry in entries):
                raise RegistryError(f"ref já existe durante commit: {ref}")

        new_relations = copy.deepcopy(global_relations)
        for relation in plan.get("relations", []):
            if not isinstance(relation, dict):
                raise RegistryError("relação do plano deve ser objeto")
            row = copy.deepcopy(relation)
            row["schema"] = RELATION_SCHEMA
            row["from_ref"] = mapping.get(row.get("from_ref"), row.get("from_ref"))
            row["to_ref"] = mapping.get(row.get("to_ref"), row.get("to_ref"))
            row.setdefault("relation_id", f"REL-{uuid.uuid4()}")
            relation_errors = validate_relation(row, "promotion-plan.relations")
            if relation_errors:
                raise RegistryError("; ".join(relation_errors))
            available = {entry.get("ref") for entry in entries} | {p["entry"]["ref"] for p in prepared}
            if row["from_ref"] not in available or row["to_ref"] not in available:
                raise RegistryError(f"relação global aponta para referência inexistente: {row}")
            signature = (row["from_ref"], row["type"], row["to_ref"], row["scope"])
            if not any((r.get("from_ref"), r.get("type"), r.get("to_ref"), r.get("scope")) == signature for r in new_relations):
                new_relations.append(row)
        for prepared_item in prepared:
            if prepared_item["supersedes"]:
                new_relations.append(
                    {
                        "schema": RELATION_SCHEMA,
                        "relation_id": f"REL-{uuid.uuid4()}",
                        "from_ref": prepared_item["entry"]["ref"],
                        "type": "supersedes",
                        "to_ref": prepared_item["supersedes"],
                        "scope": "semantic",
                        "provenance": [],
                    }
                )

        final_entries = entries + [item["entry"] for item in prepared]
        audit = {
            "schema": AUDIT_SCHEMA,
            "promotion_id": f"PROM-{uuid.uuid4()}",
            "plan_sha256": plan_hash,
            "decision_sha256": decision_hash,
            "promoted": [{"candidate_id": key, "ref": value} for key, value in sorted(mapping.items())],
            "by": by,
            "at": utc_now(),
        }
        final_audits = audits + [audit]
        previous = {
            index_path: index_path.read_bytes() if index_path.exists() else None,
            relations_path: relations_path.read_bytes() if relations_path.exists() else None,
            audit_path: audit_path.read_bytes() if audit_path.exists() else None,
        }
        created: list[Path] = []
        try:
            for item in prepared:
                path = registry / item["relative"]
                if path.exists():
                    raise RegistryError(f"versão já existe e não será sobrescrita: {path}")
                atomic_write(path, item["content"])
                created.append(path)
            atomic_write(index_path, render_jsonl(final_entries))
            atomic_write(relations_path, render_jsonl(new_relations))
            atomic_write(audit_path, render_jsonl(final_audits))
        except Exception:
            for path, content in previous.items():
                _restore(path, content)
            for path in created:
                path.unlink(missing_ok=True)
                try:
                    path.parent.rmdir()
                except OSError:
                    pass
            raise
    return {"status": "promoted", "created": [item["entry"]["ref"] for item in prepared], "mapping": mapping}


def command_promote(args: argparse.Namespace) -> int:
    result = promote(args.plan.resolve(), args.registry.resolve(), args.decision.resolve(), args.by, args.dry_run)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


def command_resolve(args: argparse.Namespace) -> int:
    registry = args.registry.resolve()
    report = registry_integrity(registry)
    if report["errors"]:
        raise RegistryError("Registry inválido: " + "; ".join(report["errors"]))
    entries, _, _ = load_registry(registry)
    matches = entries
    if args.id:
        if "@" in args.id:
            matches = [entry for entry in matches if entry.get("ref") == args.id]
        else:
            matches = [entry for entry in matches if entry.get("object_id") == args.id]
    elif args.kind:
        matches = [entry for entry in matches if entry.get("kind") == args.kind]
    elif args.capability:
        matches = [entry for entry in matches if args.capability in entry.get("capabilities", [])]
    elif args.query:
        query = args.query.casefold()
        queried: list[dict[str, Any]] = []
        for entry in matches:
            path = safe_registry_path(registry, str(entry["path"]))
            searchable = " ".join(
                [
                    str(entry.get("name", "")),
                    *map(str, entry.get("aliases", [])),
                    *map(str, entry.get("capabilities", [])),
                    path.read_text(encoding="utf-8"),
                ]
            ).casefold()
            if query in searchable:
                queried.append(entry)
        matches = queried
    matches = sorted(matches, key=lambda row: (str(row.get("object_id")), int(row.get("version", 0))))
    print(json.dumps({"count": len(matches), "matches": matches}, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if matches else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Registry de nós Sínkra v1")
    sub = parser.add_subparsers(dest="command", required=True)

    validate_parser = sub.add_parser("validate", help="validar bundle ou Registry")
    validate_parser.add_argument("target", type=Path)
    validate_parser.add_argument("--registry", type=Path)
    validate_parser.set_defaults(
        handler=lambda args: command_validate(
            args.target.resolve(), args.registry.resolve() if args.registry else None
        )
    )

    promote_parser = sub.add_parser("promote", help="promover candidatos aprovados")
    promote_parser.add_argument("plan", type=Path)
    promote_parser.add_argument("--registry", required=True, type=Path)
    promote_parser.add_argument("--decision", required=True, type=Path)
    promote_parser.add_argument("--by", required=True)
    promote_parser.add_argument("--dry-run", action="store_true")
    promote_parser.set_defaults(handler=command_promote)

    resolve_parser = sub.add_parser("resolve", help="resolver referências canônicas")
    resolve_parser.add_argument("--registry", required=True, type=Path)
    filters = resolve_parser.add_mutually_exclusive_group()
    filters.add_argument("--id")
    filters.add_argument("--kind")
    filters.add_argument("--capability")
    filters.add_argument("--query")
    resolve_parser.set_defaults(handler=command_resolve)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return int(args.handler(args))
    except RegistryError as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return exc.code
    except OSError as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

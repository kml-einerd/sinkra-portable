#!/usr/bin/env python3
"""Self-test stdlib do Registry de nós Sínkra."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any


SCRIPT = Path(__file__).with_name("node_registry.py")


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def write_markdown(path: Path, metadata: dict[str, Any], body: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = f"---\n{json.dumps(metadata, ensure_ascii=False, indent=2)}\n---\n"
    if body:
        text += f"\n{body}\n"
    path.write_text(text, encoding="utf-8")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


class RegistryCliTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.bundle = self.root / "bundle"
        self.registry = self.root / "registry"
        (self.bundle / "candidates").mkdir(parents=True)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        environment = os.environ.copy()
        environment["PYTHONUTF8"] = "1"
        return subprocess.run(
            [sys.executable, str(SCRIPT), *map(str, args)],
            cwd=self.root,
            env=environment,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )

    def task(self, candidate_id: str = "CAND-TASK-0001", name: str = "Validar completude") -> Path:
        path = self.bundle / "candidates" / f"{candidate_id.lower()}.md"
        write_markdown(
            path,
            {
                "schema": "sinkra-node-candidate@1",
                "candidate_id": candidate_id,
                "object_class": "definition",
                "kind": "task",
                "name": name,
                "status": "candidate",
                "aliases": ["checagem"],
                "capabilities": ["verification"],
                "reuse_policy": "reusable",
                "contract": {
                    "verb": "validar",
                    "executor": "worker",
                    "inputs": [],
                    "outputs": [],
                    "preconditions": [],
                    "completion": ["campos obrigatórios presentes"],
                },
                "constraints": [],
                "provenance": [{"source": "fixture", "locator": "L1"}],
            },
            "Contrato completo da task.",
        )
        return path

    def stage(self) -> Path:
        path = self.bundle / "candidates" / "stage.md"
        write_markdown(
            path,
            {
                "schema": "sinkra-node-candidate@1",
                "candidate_id": "CAND-STAGE-0001",
                "object_class": "definition",
                "kind": "stage",
                "name": "Qualificado",
                "status": "candidate",
                "capabilities": [],
                "reuse_policy": "reusable",
                "contract": {"entry": [], "exit": []},
                "constraints": [],
                "provenance": [],
            },
        )
        return path

    def composition(
        self,
        composition_id: str,
        kind: str,
        bindings: list[dict[str, Any]],
        status: str = "active",
    ) -> Path:
        path = self.bundle / "compositions" / f"{composition_id.lower()}.md"
        write_markdown(
            path,
            {
                "schema": "sinkra-composition@1",
                "composition_id": composition_id,
                "object_class": "composition",
                "kind": kind,
                "name": composition_id,
                "version": 1,
                "status": status,
                "bindings": bindings,
            },
        )
        return path

    def plan_and_decision(
        self,
        items: list[dict[str, Any]],
        approved: list[str],
        *,
        source_kind: str = "as-is",
        relations: list[dict[str, Any]] | None = None,
    ) -> tuple[Path, Path]:
        plan_path = self.bundle / "promotion-plan.json"
        write_json(
            plan_path,
            {
                "schema": "sinkra-promotion-plan@1",
                "source_bundle": ".",
                "source_kind": source_kind,
                "items": items,
                "relations": relations or [],
            },
        )
        plan_hash = hashlib.sha256(plan_path.read_bytes()).hexdigest()
        decision_path = self.bundle / "decision.json"
        write_json(
            decision_path,
            {
                "schema": "sinkra-promotion-decision@1",
                "plan_sha256": plan_hash,
                "status": "approved",
                "approved_items": approved,
                "decided_by": "KML",
                "decided_at": "2026-08-02T12:00:00Z",
            },
        )
        return plan_path, decision_path

    def promote(self, plan: Path, decision: Path, *extra: str) -> subprocess.CompletedProcess[str]:
        return self.run_cli(
            "promote",
            str(plan),
            "--registry",
            str(self.registry),
            "--decision",
            str(decision),
            "--by",
            "KML",
            *extra,
        )

    def test_promotion_is_atomic_idempotent_and_resolvable(self) -> None:
        self.task()
        self.composition(
            "COMP-WORKFLOW-0001",
            "workflow",
            [{"ref": "CAND-TASK-0001", "role": "gate-a", "when": None, "params": {"severity": "blocker"}}],
        )
        self.composition(
            "COMP-WORKFLOW-0002",
            "workflow",
            [{"ref": "CAND-TASK-0001", "role": "gate-b", "when": None, "params": {"severity": "warning"}}],
        )
        plan, decision = self.plan_and_decision(
            [{"candidate_id": "CAND-TASK-0001", "action": "promote-new", "reason": "completo"}],
            ["CAND-TASK-0001"],
        )

        dry = self.promote(plan, decision, "--dry-run")
        self.assertEqual(dry.returncode, 0, dry.stderr)
        self.assertFalse(self.registry.exists())

        first = self.promote(plan, decision)
        self.assertEqual(first.returncode, 0, first.stderr)
        entries = read_jsonl(self.registry / "registry.jsonl")
        self.assertEqual(len(entries), 1)
        ref = entries[0]["ref"]
        object_path = self.registry / entries[0]["path"]
        self.assertEqual(entries[0]["sha256"], hashlib.sha256(object_path.read_bytes()).hexdigest())

        repeated = self.promote(plan, decision)
        self.assertEqual(repeated.returncode, 0, repeated.stderr)
        self.assertEqual(len(read_jsonl(self.registry / "registry.jsonl")), 1)
        self.assertIn("unchanged", repeated.stdout)

        resolved = self.run_cli("resolve", "--registry", str(self.registry), "--capability", "verification")
        self.assertEqual(resolved.returncode, 0, resolved.stderr)
        self.assertEqual(json.loads(resolved.stdout)["matches"][0]["ref"], ref)
        by_alias = self.run_cli("resolve", "--registry", str(self.registry), "--query", "checagem")
        self.assertEqual(by_alias.returncode, 0, by_alias.stderr)
        by_text = self.run_cli("resolve", "--registry", str(self.registry), "--query", "Contrato completo")
        self.assertEqual(by_text.returncode, 0, by_text.stderr)
        valid = self.run_cli("validate", str(self.registry))
        self.assertEqual(valid.returncode, 0, valid.stdout + valid.stderr)

    def test_invalid_inputs_fail_before_registry_write(self) -> None:
        task_path = self.task()
        metadata = json.loads(task_path.read_text(encoding="utf-8").split("---")[1])
        metadata["contract"].pop("completion")
        write_markdown(task_path, metadata)
        plan, decision = self.plan_and_decision(
            [{"candidate_id": "CAND-TASK-0001", "action": "promote-new", "reason": "incompleto"}],
            ["CAND-TASK-0001"],
        )
        result = self.promote(plan, decision)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.registry / "registry.jsonl").exists())

    def test_stage_requires_lifecycle(self) -> None:
        self.stage()
        plan, decision = self.plan_and_decision(
            [{"candidate_id": "CAND-STAGE-0001", "action": "promote-new", "reason": "stage"}],
            ["CAND-STAGE-0001"],
        )
        result = self.promote(plan, decision)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("sem lifecycle", result.stderr)
        self.assertFalse((self.registry / "registry.jsonl").exists())

    def test_broken_reference_and_runtime_promotion_are_rejected(self) -> None:
        self.task()
        self.composition(
            "COMP-WORKFLOW-0001",
            "workflow",
            [{"ref": "CAND-TASK-9999", "role": "missing", "when": None, "params": {}}],
        )
        validated = self.run_cli("validate", str(self.bundle))
        self.assertEqual(validated.returncode, 1)
        self.assertIn("inexistente", validated.stdout)

        self.composition(
            "COMP-WORKFLOW-0001",
            "workflow",
            [{"ref": "NODE-MISSING@1", "role": "missing", "when": None, "params": {}}],
        )
        without_registry = self.run_cli("validate", str(self.bundle))
        self.assertEqual(without_registry.returncode, 1)
        self.assertIn("não verificável sem --registry", without_registry.stdout)
        with_registry = self.run_cli("validate", str(self.bundle), "--registry", str(self.registry))
        self.assertEqual(with_registry.returncode, 1)
        self.assertIn("referência canônica inexistente", with_registry.stdout)

        runtime_path = self.bundle / "candidates" / "runtime.md"
        write_markdown(
            runtime_path,
            {
                "schema": "sinkra-runtime@1",
                "candidate_id": "CAND-TASK-RUN-0001",
                "runtime_id": "RUN-1",
                "object_class": "runtime",
                "kind": "task-run",
                "definition_ref": "CAND-TASK-0001",
                "status": "done",
            },
        )
        plan, decision = self.plan_and_decision(
            [{"candidate_id": "CAND-TASK-RUN-0001", "action": "promote-new", "reason": "não pode"}],
            ["CAND-TASK-RUN-0001"],
        )
        promoted = self.promote(plan, decision)
        self.assertNotEqual(promoted.returncode, 0)
        self.assertIn("somente definition", promoted.stderr)
        self.assertFalse((self.registry / "registry.jsonl").exists())

    def test_required_fields_for_composition_runtime_and_evidence(self) -> None:
        write_markdown(
            self.bundle / "compositions" / "incomplete.md",
            {
                "schema": "sinkra-composition@1",
                "composition_id": "COMP-WORKFLOW-0001",
                "object_class": "composition",
                "kind": "workflow",
                "bindings": [],
            },
        )
        write_json(
            self.bundle / "runtime" / "incomplete.json",
            {
                "schema": "sinkra-runtime@1",
                "runtime_id": "RUN-1",
                "object_class": "runtime",
                "kind": "task-run",
                "definition_ref": "CAND-TASK-0001",
                "status": "done",
            },
        )
        write_markdown(
            self.bundle / "evidence" / "incomplete.md",
            {
                "schema": "sinkra-evidence@1",
                "evidence_id": "EVD-1",
                "object_class": "evidence",
                "kind": "report",
                "source": "fixture",
                "locator": "L1",
            },
        )
        result = self.run_cli("validate", str(self.bundle))
        self.assertEqual(result.returncode, 1)
        self.assertIn("version deve ser inteiro positivo", result.stdout)
        self.assertIn("recorded_at", result.stdout)
        self.assertIn("evidence_refs", result.stdout)
        self.assertIn("captured_at", result.stdout)

    def test_new_version_supersedes_and_pinned_ref_stays_exact(self) -> None:
        task_path = self.task()
        plan1, decision1 = self.plan_and_decision(
            [{"candidate_id": "CAND-TASK-0001", "action": "promote-new", "reason": "v1"}],
            ["CAND-TASK-0001"],
        )
        self.assertEqual(self.promote(plan1, decision1).returncode, 0)
        first_entry = read_jsonl(self.registry / "registry.jsonl")[0]
        first_ref = first_entry["ref"]

        metadata = json.loads(task_path.read_text(encoding="utf-8").split("---")[1])
        metadata["name"] = "Validar completude revisada"
        write_markdown(task_path, metadata, "Nova versão.")
        plan2, decision2 = self.plan_and_decision(
            [
                {
                    "candidate_id": "CAND-TASK-0001",
                    "action": "promote-version",
                    "target_object_id": first_entry["object_id"],
                    "reason": "correção permanente",
                }
            ],
            ["CAND-TASK-0001"],
        )
        second = self.promote(plan2, decision2)
        self.assertEqual(second.returncode, 0, second.stderr)
        entries = read_jsonl(self.registry / "registry.jsonl")
        self.assertEqual([entry["version"] for entry in entries], [1, 2])
        second_meta = json.loads((self.registry / entries[1]["path"]).read_text(encoding="utf-8").split("---")[1])
        self.assertEqual(second_meta["supersedes"], first_ref)

        pinned = self.run_cli("resolve", "--registry", str(self.registry), "--id", first_ref)
        self.assertEqual(pinned.returncode, 0, pinned.stderr)
        matches = json.loads(pinned.stdout)["matches"]
        self.assertEqual([entry["ref"] for entry in matches], [first_ref])

    def test_hash_tamper_lock_and_unknown_relation_fail_safely(self) -> None:
        self.task()
        plan, decision = self.plan_and_decision(
            [{"candidate_id": "CAND-TASK-0001", "action": "promote-new", "reason": "ok"}],
            ["CAND-TASK-0001"],
            relations=[
                {
                    "from_ref": "CAND-TASK-0001",
                    "type": "supports",
                    "to_ref": "NODE-MISSING@1",
                    "scope": "semantic",
                }
            ],
        )
        broken = self.promote(plan, decision)
        self.assertNotEqual(broken.returncode, 0)
        self.assertFalse((self.registry / "registry.jsonl").exists())

        plan, decision = self.plan_and_decision(
            [{"candidate_id": "CAND-TASK-0001", "action": "promote-new", "reason": "ok"}],
            ["CAND-TASK-0001"],
        )
        (self.registry / ".promotion.lock").mkdir(parents=True)
        locked = self.promote(plan, decision)
        self.assertEqual(locked.returncode, 5)
        (self.registry / ".promotion.lock").rmdir()

        self.assertEqual(self.promote(plan, decision).returncode, 0)
        entry = read_jsonl(self.registry / "registry.jsonl")[0]
        object_path = self.registry / entry["path"]
        object_path.write_text(object_path.read_text(encoding="utf-8") + "alterado\n", encoding="utf-8")
        invalid = self.run_cli("validate", str(self.registry))
        self.assertEqual(invalid.returncode, 1)
        self.assertIn("hash divergente", invalid.stdout)

    def test_whatsapp_hold_and_cancelled_flow_preserve_files(self) -> None:
        idea = self.bundle / "candidates" / "idea.md"
        write_markdown(
            idea,
            {
                "schema": "sinkra-node-candidate@1",
                "candidate_id": "CAND-IDEA-0001",
                "object_class": "definition",
                "kind": "idea",
                "name": "Possível melhoria",
                "status": "candidate",
                "capabilities": [],
                "reuse_policy": "reusable",
                "contract": {},
                "constraints": [],
                "provenance": [],
            },
        )
        plan, decision = self.plan_and_decision(
            [{"candidate_id": "CAND-IDEA-0001", "action": "hold", "reason": "WhatsApp"}],
            [],
            source_kind="whatsapp",
        )
        held = self.promote(plan, decision)
        self.assertEqual(held.returncode, 0, held.stderr)
        self.assertIn("no-approved-promotions", held.stdout)
        self.assertFalse(self.registry.exists())

        self.task()
        self.stage()
        self.composition(
            "COMP-LIFECYCLE-0001",
            "lifecycle",
            [{"ref": "CAND-STAGE-0001", "role": "state", "when": None, "params": {}}],
        )
        self.composition(
            "COMP-WORKFLOW-0001",
            "workflow",
            [{"ref": "CAND-TASK-0001", "role": "check", "when": None, "params": {}}],
            status="cancelled",
        )
        runtime = self.bundle / "runtime" / "cycle-run.json"
        write_markdown(
            self.bundle / "evidence" / "cancellation.md",
            {
                "schema": "sinkra-evidence@1",
                "evidence_id": "EVD-1",
                "object_class": "evidence",
                "kind": "report",
                "source": "fixture",
                "locator": "cancelamento",
                "captured_at": "2026-08-02T12:00:00Z",
            },
        )
        write_json(
            runtime,
            {
                "schema": "sinkra-runtime@1",
                "runtime_id": "RUN-CYCLE-1",
                "object_class": "runtime",
                "kind": "cycle-run",
                "definition_ref": "CAND-TASK-0001",
                "status": "cancelled",
                "recorded_at": "2026-08-02T12:00:00Z",
                "entity_last_stage_ref": "CAND-STAGE-0001",
                "tasks": [{"status": "cancelled"}, {"status": "not-applicable"}],
                "evidence_refs": ["EVD-1"],
            },
        )
        before = {path: hashlib.sha256(path.read_bytes()).hexdigest() for path in (idea, runtime)}
        validated = self.run_cli("validate", str(self.bundle))
        self.assertEqual(validated.returncode, 0, validated.stdout + validated.stderr)
        after = {path: hashlib.sha256(path.read_bytes()).hexdigest() for path in (idea, runtime)}
        self.assertEqual(before, after)
        self.assertIn("unreferenced", validated.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)

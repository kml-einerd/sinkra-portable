#!/usr/bin/env python3
"""Validação estrutural read-only do Sínkra Portable, somente com stdlib."""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parent.parent
SKILLS = {
    "sinkra-arquitetar-sistema",
    "sinkra-auditar-sistema",
    "sinkra-elicitar-construcao",
    "sinkra-extrair-nos",
    "sinkra-forjar-skill",
    "sinkra-mapear-processo",
    "sinkra-modelar-executores",
}
REQUIRED = {
    "AGENTS.md",
    "PACKAGE.yaml",
    "PROMPT.md",
    "README.md",
    "materials/README.md",
    "materials/00-visao-canonica-sinkra.md",
    "skills/_shared/references/contracts.md",
    "skills/_shared/references/sinkra-core.md",
    "skills/_shared/templates/sinkra-work/state.yaml",
    "skills/_shared/templates/sinkra-work/gates/gate-template.yaml",
    "skills/_shared/templates/sinkra-work/outputs/output-template.yaml",
}
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
FRONTMATTER_RE = re.compile(
    r"\A---\s*\nname:\s*([^\n]+)\ndescription:\s*(.+?)\n---", re.DOTALL
)


def normalized_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def inventory() -> set[str]:
    found: set[str] = set()
    for path in ROOT.rglob("*"):
        if ".git" in path.parts:
            continue
        found.add(path.relative_to(ROOT).as_posix())
    return found


def validate_required(found: set[str], errors: list[str]) -> None:
    for relative in sorted(REQUIRED - found):
        errors.append(f"arquivo obrigatório ausente: {relative}")


def validate_skills(found: set[str], errors: list[str]) -> None:
    discovered = {
        path.name
        for path in (ROOT / "skills").iterdir()
        if path.is_dir() and path.name.startswith("sinkra-")
    }
    if discovered != SKILLS:
        errors.append(
            "skills divergentes: esperado="
            f"{sorted(SKILLS)} encontrado={sorted(discovered)}"
        )
    for name in sorted(SKILLS):
        skill_path = ROOT / "skills" / name / "SKILL.md"
        agent_path = ROOT / "skills" / name / "agents" / "openai.yaml"
        if not skill_path.is_file() or not agent_path.is_file():
            errors.append(f"skill incompleta: {name}")
            continue
        match = FRONTMATTER_RE.search(normalized_text(skill_path))
        if not match:
            errors.append(f"frontmatter inválido: {skill_path.relative_to(ROOT)}")
            continue
        declared = match.group(1).strip().strip('"\'')
        if declared != name:
            errors.append(f"nome divergente em {name}: {declared}")


def validate_links(found: set[str], errors: list[str]) -> None:
    for markdown in ROOT.rglob("*.md"):
        if ".git" in markdown.parts:
            continue
        text = normalized_text(markdown)
        for match in LINK_RE.finditer(text):
            target = unquote(match.group(1).strip())
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = target.split("#", 1)[0]
            if not target:
                continue
            lexical = os.path.normpath(str(markdown.parent / target))
            try:
                relative = Path(lexical).relative_to(ROOT).as_posix()
            except ValueError:
                line = text.count("\n", 0, match.start()) + 1
                errors.append(
                    f"link fora do pacote: {markdown.relative_to(ROOT)}:{line} -> {target}"
                )
                continue
            if relative not in found:
                line = text.count("\n", 0, match.start()) + 1
                errors.append(
                    f"link local quebrado/case incorreto: "
                    f"{markdown.relative_to(ROOT)}:{line} -> {target}"
                )


def validate_mirrors(errors: list[str]) -> None:
    pairs = [
        (
            "skills/_shared/templates/decision-record.yaml",
            "skills/_shared/templates/sinkra-work/decisions/decision-template.yaml",
        ),
        (
            "skills/_shared/templates/executor-registry.yaml",
            "skills/_shared/templates/sinkra-work/registry/executors.yaml",
        ),
    ]
    for canonical, operational in pairs:
        if normalized_text(ROOT / canonical) != normalized_text(ROOT / operational):
            errors.append(f"espelho divergente: {operational} != {canonical}")


def main() -> int:
    errors: list[str] = []
    found = inventory()
    validate_required(found, errors)
    validate_skills(found, errors)
    validate_links(found, errors)
    validate_mirrors(errors)
    if errors:
        print("Sinkra Portable: FALHOU")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        "Sinkra Portable: OK | "
        f"skills={len(SKILLS)} | markdown={len(list(ROOT.rglob('*.md')))}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

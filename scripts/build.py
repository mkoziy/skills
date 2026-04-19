#!/usr/bin/env python3

import re
import shutil
from pathlib import Path


INCLUDE_RE = re.compile(r'{{\s*include\s+"([^"]+)"\s*}}')

SKILL_OUTPUTS = {
    "claude": lambda root: root / ".claude" / "skills",
    "codex": lambda root: root / ".codex" / "skills",
    "opencode": lambda root: root / ".opencode",
}

SUBAGENT_OUTPUTS = {
    "claude": lambda root: root / ".claude" / "agents",
    "codex": lambda root: root / ".codex" / "agents",
}


def expand_includes(text: str, src_root: Path, stack: tuple[Path, ...] = ()) -> str:
    def replace(match: re.Match[str]) -> str:
        include_path = src_root / match.group(1)
        include_path = include_path.resolve()
        if include_path in stack:
            cycle = " -> ".join(str(path.relative_to(src_root.resolve())) for path in (*stack, include_path))
            raise ValueError(f"circular include detected: {cycle}")
        if not include_path.is_file():
            missing = include_path.relative_to(src_root.resolve())
            raise FileNotFoundError(f"missing include: {missing}")
        included = include_path.read_text(encoding="utf-8")
        return expand_includes(included, src_root, (*stack, include_path))

    return INCLUDE_RE.sub(replace, text)


def collect_skills(skills_root: Path) -> dict[Path, Path]:
    if not skills_root.is_dir():
        return {}

    skills: dict[Path, Path] = {}
    for template_path in sorted(skills_root.rglob("SKILL.md")):
        relative_dir = template_path.parent.relative_to(skills_root)
        skills[relative_dir] = template_path
    return skills


def collect_agents(agents_root: Path) -> dict[str, Path]:
    """Returns {agent_name: template_path} for each SKILL.md under agents_root."""
    if not agents_root.is_dir():
        return {}

    agents: dict[str, Path] = {}
    for template_path in sorted(agents_root.rglob("SKILL.md")):
        agent_name = template_path.parent.relative_to(agents_root).parts[0]
        agents[agent_name] = template_path
    return agents


def _clean_dir(output_root: Path) -> None:
    output_root.mkdir(parents=True, exist_ok=True)
    for child in output_root.iterdir():
        if child.is_dir():
            shutil.rmtree(child)
        elif child.is_file():
            child.unlink()


def build_all(project_root: Path) -> None:
    src_root = project_root / "src"

    for tool, output_root_fn in SKILL_OUTPUTS.items():
        agent_skills = collect_skills(src_root / tool / "skills")
        output_root = output_root_fn(project_root)
        output_root.mkdir(parents=True, exist_ok=True)

        for child in output_root.iterdir():
            if child.is_dir():
                shutil.rmtree(child)

        for relative_dir, template_path in agent_skills.items():
            expanded = expand_includes(template_path.read_text(encoding="utf-8"), src_root)
            output_dir = output_root / relative_dir
            output_dir.mkdir(parents=True, exist_ok=True)
            (output_dir / "SKILL.md").write_text(expanded, encoding="utf-8")
            for extra in sorted(template_path.parent.rglob("*")):
                if extra.is_file() and extra.name != "SKILL.md":
                    dest = output_dir / extra.relative_to(template_path.parent)
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(extra, dest)

    for tool, output_root_fn in SUBAGENT_OUTPUTS.items():
        tool_agents = collect_agents(src_root / tool / "agents")
        output_root = output_root_fn(project_root)
        _clean_dir(output_root)

        for agent_name, template_path in tool_agents.items():
            expanded = expand_includes(template_path.read_text(encoding="utf-8"), src_root)
            (output_root / f"{agent_name}.md").write_text(expanded, encoding="utf-8")


def main() -> int:
    build_all(Path(__file__).resolve().parent.parent)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

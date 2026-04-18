import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.build import build_all


class BuildSkillsTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp(prefix="skills-build-test-"))
        self.addCleanup(lambda: shutil.rmtree(self.temp_dir))

        src_dir = self.temp_dir / "src"
        (src_dir / "claude" / "skills" / "claude-only").mkdir(parents=True)
        (src_dir / "codex" / "skills" / "shared").mkdir(parents=True)
        (src_dir / "opencode" / "skills" / "nested" / "demo").mkdir(parents=True)

        (src_dir / "claude" / "skills" / "claude-only" / "SKILL.md").write_text(
            "# Claude Only\n",
            encoding="utf-8",
        )
        (src_dir / "codex" / "skills" / "shared" / "SKILL.md").write_text(
            "# Codex Shared\n",
            encoding="utf-8",
        )
        (src_dir / "opencode" / "skills" / "nested" / "demo" / "SKILL.md").write_text(
            "# Opencode Nested\n",
            encoding="utf-8",
        )

        stale_output = self.temp_dir / ".opencode" / "claude-only" / "SKILL.md"
        stale_output.parent.mkdir(parents=True, exist_ok=True)
        stale_output.write_text("stale\n", encoding="utf-8")

    def test_build_all_uses_only_existing_agent_files_and_preserves_structure(self):
        build_all(self.temp_dir)

        self.assertEqual(
            (self.temp_dir / ".claude" / "skills" / "claude-only" / "SKILL.md").read_text(encoding="utf-8"),
            "# Claude Only\n",
        )
        self.assertEqual(
            (self.temp_dir / ".codex" / "skills" / "shared" / "SKILL.md").read_text(encoding="utf-8"),
            "# Codex Shared\n",
        )
        self.assertEqual(
            (self.temp_dir / ".opencode" / "nested" / "demo" / "SKILL.md").read_text(encoding="utf-8"),
            "# Opencode Nested\n",
        )

        self.assertFalse((self.temp_dir / ".claude" / "skills" / "shared" / "SKILL.md").exists())
        self.assertFalse((self.temp_dir / ".codex" / "skills" / "claude-only" / "SKILL.md").exists())
        self.assertFalse((self.temp_dir / ".opencode" / "claude-only" / "SKILL.md").exists())


class BuildAgentsTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp(prefix="skills-build-agents-test-"))
        self.addCleanup(lambda: shutil.rmtree(self.temp_dir))

        src_dir = self.temp_dir / "src"
        (src_dir / "common" / "agents" / "my-agent").mkdir(parents=True)
        (src_dir / "common" / "agents" / "my-agent" / "SKILL.md").write_text(
            "# My Agent\n",
            encoding="utf-8",
        )

        (src_dir / "claude" / "agents" / "my-agent").mkdir(parents=True)
        (src_dir / "claude" / "agents" / "my-agent" / "SKILL.md").write_text(
            '{{ include "common/agents/my-agent/SKILL.md" }}',
            encoding="utf-8",
        )

        (src_dir / "codex" / "agents" / "my-agent").mkdir(parents=True)
        (src_dir / "codex" / "agents" / "my-agent" / "SKILL.md").write_text(
            '{{ include "common/agents/my-agent/SKILL.md" }}',
            encoding="utf-8",
        )

        stale = self.temp_dir / ".claude" / "agents" / "stale.md"
        stale.parent.mkdir(parents=True, exist_ok=True)
        stale.write_text("stale\n", encoding="utf-8")

    def test_agents_output_as_flat_md_files(self):
        build_all(self.temp_dir)

        self.assertEqual(
            (self.temp_dir / ".claude" / "agents" / "my-agent.md").read_text(encoding="utf-8"),
            "# My Agent\n",
        )
        self.assertEqual(
            (self.temp_dir / ".codex" / "agents" / "my-agent.md").read_text(encoding="utf-8"),
            "# My Agent\n",
        )

    def test_agents_output_dir_is_cleaned_before_rebuild(self):
        build_all(self.temp_dir)
        self.assertFalse((self.temp_dir / ".claude" / "agents" / "stale.md").exists())

    def test_common_agents_not_output_directly(self):
        build_all(self.temp_dir)
        self.assertFalse((self.temp_dir / ".claude" / "agents" / "common").exists())
        self.assertFalse((self.temp_dir / ".codex" / "agents" / "common").exists())


if __name__ == "__main__":
    unittest.main()

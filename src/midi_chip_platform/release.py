# Bestand: release.py
# Versienommer: 0.12.3
# Doel: Besit host- en toestel-release-naspeurbaarheid vir die US-005 herstel.
# Sprint: Sprint 2
# Epic: MCP-EPIC-001 Platform Foundation
# User-Story: MCP-US-005 Configuration And Secret Boundary
# Actienr: MCP-ACT-005-IMP-001-REL-001
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-005-RETEST


class ReleaseMetadata:
    def __init__(
        self,
        version="0.12.3",
        user_story="MCP-US-005",
        release_date="2026-07-16",
    ):
        self._version = str(version)
        self._user_story = str(user_story)
        self._release_date = str(release_date)

    @property
    def version(self):
        return self._version

    @property
    def user_story(self):
        return self._user_story

    @property
    def release_date(self):
        return self._release_date

    def banner(self):
        return (
            f"circuitpython-midi-chip-platform v{self._version} | "
            f"story={self._user_story} | release-date={self._release_date}"
        )

# Bestand: code.py
# Versienommer: 0.2.0
# Doel: Rapporteer veilige toestelvermoens sonder om MIDI-, klank- of netwerkdienste te begin.
# Sprint: Sprint 1
# Epic: MCP-EPIC-001 Platform Foundation
# User-Story: MCP-US-004 Board Capability Discovery
# Actienr: MCP-ACT-004-GREEN-003
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-004

from midi_chip_platform.device_runtime import DeviceRuntimeApplication
from midi_chip_platform.platform_capabilities import CircuitPythonCapabilityFactory
from midi_chip_platform.release import ReleaseMetadata


if __name__ == "__main__":
    DeviceRuntimeApplication(
        release_metadata=ReleaseMetadata(),
        capability_discovery=CircuitPythonCapabilityFactory(__import__).create_discovery(),
    ).run()

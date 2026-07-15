# Bestand: test_device_runtime.py
# Versienommer: 0.11.1
# Doel: Spesifiseer toestel-uitvoer, capability- en dependency-importbewys sonder diensaktivering.
# Sprint: Sprint 2
# Epic: MCP-EPIC-008 Portability, Quality And Release
# User-Story: MCP-US-051/MCP-US-007 Dependency-Closed Deployment Impediment
# Actienr: MCP-ACT-051-IMP-001-RED-002
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-051-IMP-001

from midi_chip_platform.device_runtime import DeviceImportSmokeCheck, DeviceRuntimeApplication
from midi_chip_platform.release import ReleaseMetadata


class TestDeviceRuntimeApplication:
    class FakeImporter:
        def __init__(self):
            self.module_names = []

        def __call__(self, module_name):
            self.module_names.append(module_name)
            return object()

    class FakeSnapshot:
        def report_lines(self):
            return (
                "CAPABILITY_DISCOVERY_STATUS=PASS",
                "BOARD_ID=lolin_s2_mini",
            )

    class FakeDiscovery:
        def discover(self):
            return TestDeviceRuntimeApplication.FakeSnapshot()

    class FakeConfigurationSnapshot:
        def report_lines(self):
            return (
                "CONFIGURATION_STATUS=PASS",
                "CONFIG_PRIVATE_WIFI_SSID=SET",
            )

    class FakeConfigurationLoader:
        def load(self):
            return TestDeviceRuntimeApplication.FakeConfigurationSnapshot()

    def test_runtime_reports_execution_proof(self) -> None:
        output = []
        application = DeviceRuntimeApplication(
            release_metadata=ReleaseMetadata(
                version="0.2.0",
                user_story="MCP-US-003",
                release_date="2026-07-14",
            ),
            output=output.append,
        )

        result = application.run()

        assert result is True
        assert output == [
            "circuitpython-midi-chip-platform v0.2.0 | "
            "story=MCP-US-003 | release-date=2026-07-14",
            "DEVICE_EXECUTION_STATUS=READY",
        ]

    def test_runtime_reports_device_import_smoke_proof_before_ready(self) -> None:
        output = []
        importer = self.FakeImporter()
        application = DeviceRuntimeApplication(
            release_metadata=ReleaseMetadata(
                version="0.11.1",
                user_story="MCP-US-051-IMP-001",
                release_date="2026-07-15",
            ),
            import_smoke_check=DeviceImportSmokeCheck(
                importer=importer,
                module_names=(
                    "adafruit_midi",
                    "midi_chip_platform.routing",
                ),
            ),
            output=output.append,
        )

        result = application.run()

        assert result is True
        assert importer.module_names == [
            "adafruit_midi",
            "midi_chip_platform.routing",
        ]
        assert output == [
            "circuitpython-midi-chip-platform v0.11.1 | "
            "story=MCP-US-051-IMP-001 | release-date=2026-07-15",
            "DEVICE_IMPORT_STATUS=PASS",
            "DEVICE_EXECUTION_STATUS=READY",
        ]

    def test_runtime_reports_injected_board_capabilities(self) -> None:
        output = []
        application = DeviceRuntimeApplication(
            release_metadata=ReleaseMetadata(
                version="0.4.0",
                user_story="MCP-US-004",
                release_date="2026-07-14",
            ),
            capability_discovery=self.FakeDiscovery(),
            output=output.append,
        )

        result = application.run()

        assert result is True
        assert output == [
            "circuitpython-midi-chip-platform v0.4.0 | "
            "story=MCP-US-004 | release-date=2026-07-14",
            "CAPABILITY_DISCOVERY_STATUS=PASS",
            "BOARD_ID=lolin_s2_mini",
            "DEVICE_EXECUTION_STATUS=READY",
        ]

    def test_runtime_reports_only_redacted_configuration_state(self) -> None:
        output = []
        application = DeviceRuntimeApplication(
            release_metadata=ReleaseMetadata(
                version="0.5.0",
                user_story="MCP-US-005",
                release_date="2026-07-15",
            ),
            configuration_loader=self.FakeConfigurationLoader(),
            output=output.append,
        )

        result = application.run()

        assert result is True
        assert output == [
            "circuitpython-midi-chip-platform v0.5.0 | "
            "story=MCP-US-005 | release-date=2026-07-15",
            "CONFIGURATION_STATUS=PASS",
            "CONFIG_PRIVATE_WIFI_SSID=SET",
            "DEVICE_EXECUTION_STATUS=READY",
        ]

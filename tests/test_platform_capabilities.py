# Bestand: test_platform_capabilities.py
# Versienommer: 0.1.0
# Doel: Spesifiseer bord-, pen-, module-, geheue- en klankbackend-ontdekking.
# Sprint: Sprint 1
# Epic: MCP-EPIC-001 Platform Foundation
# User-Story: MCP-US-004 Board Capability Discovery
# Actienr: MCP-ACT-004-RED-001
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-004

from midi_chip_platform.platform_capabilities import (
    BoardCapabilityDiscovery,
    BoardProfileRegistry,
    ImportModuleProbe,
    MemoryProbe,
)


class TestBoardCapabilityDiscovery:
    class FakeBoard:
        board_id = "lolin_s2_mini"
        IO3 = object()
        IO5 = object()
        IO7 = object()

    class UnknownBoard:
        board_id = "experimental_board"

    class FakeImporter:
        def __init__(self, available_names):
            self._available_names = set(available_names)

        def __call__(self, module_name):
            if module_name not in self._available_names:
                raise ImportError(module_name)
            return object()

    class FakeGc:
        def mem_free(self):
            return 135168

        def mem_alloc(self):
            return 32768

    def test_lolin_profile_reports_validated_max98357_defaults(self) -> None:
        discovery = BoardCapabilityDiscovery(
            board_module=self.FakeBoard(),
            module_probe=ImportModuleProbe(
                self.FakeImporter(("audiobusio", "audiopwmio", "synthio", "usb_midi", "wifi"))
            ),
            memory_probe=MemoryProbe(self.FakeGc()),
            profile_registry=BoardProfileRegistry.default(),
        )

        snapshot = discovery.discover()

        assert snapshot.board_id == "lolin_s2_mini"
        assert snapshot.profile_status == "KNOWN"
        assert snapshot.i2s_pins.bit_clock == "IO5"
        assert snapshot.i2s_pins.word_select == "IO3"
        assert snapshot.i2s_pins.data == "IO7"
        assert snapshot.i2s_pins.amplifier_data_label == "DIN"
        assert snapshot.i2s_pins.is_available is True
        assert snapshot.memory_free_bytes == 135168
        assert snapshot.memory_allocated_bytes == 32768
        assert "i2s-max98357a-mono" in snapshot.audio_backends
        assert "pwm-diagnostic-unconfigured" in snapshot.audio_backends

    def test_missing_i2s_module_keeps_profile_but_disables_backend(self) -> None:
        discovery = BoardCapabilityDiscovery(
            board_module=self.FakeBoard(),
            module_probe=ImportModuleProbe(self.FakeImporter(("usb_midi",))),
            memory_probe=MemoryProbe(self.FakeGc()),
            profile_registry=BoardProfileRegistry.default(),
        )

        snapshot = discovery.discover()

        assert snapshot.i2s_pins.is_available is True
        assert snapshot.module_available("audiobusio") is False
        assert "i2s-max98357a-mono" not in snapshot.audio_backends

    def test_unknown_board_fails_safe_without_assuming_pins(self) -> None:
        discovery = BoardCapabilityDiscovery(
            board_module=self.UnknownBoard(),
            module_probe=ImportModuleProbe(self.FakeImporter(("audiobusio",))),
            memory_probe=MemoryProbe(self.FakeGc()),
            profile_registry=BoardProfileRegistry.default(),
        )

        snapshot = discovery.discover()

        assert snapshot.profile_status == "UNKNOWN"
        assert snapshot.i2s_pins is None
        assert snapshot.audio_backends == ()

    def test_report_is_stable_and_contains_no_object_identifiers(self) -> None:
        discovery = BoardCapabilityDiscovery(
            board_module=self.FakeBoard(),
            module_probe=ImportModuleProbe(self.FakeImporter(("audiobusio", "usb_midi"))),
            memory_probe=MemoryProbe(self.FakeGc()),
            profile_registry=BoardProfileRegistry.default(),
        )

        report = discovery.discover().report_lines()

        assert report[0] == "CAPABILITY_DISCOVERY_STATUS=PASS"
        assert "BOARD_ID=lolin_s2_mini" in report
        assert "I2S_PINS=BCLK:IO5,WS:IO3,DATA:IO7->DIN" in report
        assert all("0x" not in line for line in report)


class TestBoardProfileRegistry:
    def test_profile_rejects_duplicate_i2s_pin_assignments(self) -> None:
        try:
            BoardProfileRegistry.create_lolin_s2_mini(
                bit_clock="IO5",
                word_select="IO5",
                data="IO7",
            )
        except ValueError as error:
            assert "unique" in str(error)
        else:
            raise AssertionError("duplicate I2S pin assignments must fail")

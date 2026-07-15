# Bestand: test_midi_performance.py
# Versienommer: 0.1.0
# Doel: Bewys per-kanaal pitch-bend- en CC1-modulasiestatus.
# Sprint: Sprint 2
# Epic: MCP-EPIC-002 MIDI And Clock
# User-Story: MCP-US-010 Pitch Bend And CC1 Modulation
# Actienr: MCP-ACT-010-RED-001
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-010

import pytest

from midi_chip_platform.events import ControlEvent
from midi_chip_platform.midi_performance import MidiPerformanceState


class TestMidiPerformanceState:
    def test_pitch_bend_is_normalized_to_configured_semitone_range(self) -> None:
        state = MidiPerformanceState(pitch_bend_range=2.0)

        state.process(ControlEvent.pitch_bend(1, 0))
        minimum = state.channel_state(1)
        state.process(ControlEvent.pitch_bend(1, 8192))
        center = state.channel_state(1)
        state.process(ControlEvent.pitch_bend(1, 16383))
        maximum = state.channel_state(1)

        assert minimum.pitch_bend_semitones == -2.0
        assert center.pitch_bend_semitones == 0.0
        assert maximum.pitch_bend_semitones == pytest.approx(1.999755859375)

    def test_modulation_is_normalized_and_isolated_per_channel(self) -> None:
        state = MidiPerformanceState(pitch_bend_range=12.0)

        state.process(ControlEvent.control_change(2, 1, 127))
        state.process(ControlEvent.pitch_bend(3, 12288))

        assert state.channel_state(2).modulation == 1.0
        assert state.channel_state(2).pitch_bend_semitones == 0.0
        assert state.channel_state(3).modulation == 0.0
        assert state.channel_state(3).pitch_bend_semitones == 6.0

    def test_unrelated_control_change_passes_through_without_mutation(self) -> None:
        state = MidiPerformanceState()
        event = ControlEvent.control_change(1, 64, 127)

        emitted = state.process(event)

        assert emitted == (event,)
        assert state.channel_state(1).modulation == 0.0

    def test_pitch_bend_range_must_be_positive(self) -> None:
        with pytest.raises(ValueError, match="pitch_bend_range"):
            MidiPerformanceState(pitch_bend_range=0)

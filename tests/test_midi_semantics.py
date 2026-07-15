# Bestand: test_midi_semantics.py
# Versienommer: 0.1.0
# Doel: Bewys velocity-zero, note-off en all-notes-off lewensiklusse.
# Sprint: Sprint 2
# Epic: MCP-EPIC-002 MIDI And Clock
# User-Story: MCP-US-009 Velocity And Note-Off Semantics
# Actienr: MCP-ACT-009-RED-001
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-009

from midi_chip_platform.events import ControlEvent, NoteEvent
from midi_chip_platform.midi_semantics import MidiNoteState
from midi_chip_platform.midi_usb import MidiReceiveLoop
from midi_chip_platform.testing import MemoryMidiInput


class TestMidiNoteState:
    def test_note_on_velocity_zero_is_normalized_to_note_off(self) -> None:
        state = MidiNoteState()
        state.process(NoteEvent.note_on(1, 60, 100))

        events = state.process(NoteEvent.note_on(1, 60, 0))

        assert len(events) == 1
        assert (events[0].message_type, events[0].channel, events[0].note) == (
            "note_off",
            1,
            60,
        )
        assert state.active_notes == ()

    def test_all_notes_off_releases_only_the_target_channel(self) -> None:
        state = MidiNoteState()
        state.process(NoteEvent.note_on(1, 60, 100))
        state.process(NoteEvent.note_on(1, 64, 100))
        state.process(NoteEvent.note_on(2, 67, 100))

        releases = state.process(ControlEvent.control_change(1, 123, 0))

        assert tuple((event.channel, event.note) for event in releases) == ((1, 60), (1, 64))
        assert state.active_notes == ((2, 67),)

    def test_all_sound_off_has_the_same_stuck_note_safety(self) -> None:
        state = MidiNoteState()
        state.process(NoteEvent.note_on(3, 72, 100))

        releases = state.process(ControlEvent.control_change(3, 120, 0))

        assert tuple(event.message_type for event in releases) == ("note_off",)
        assert state.active_notes == ()


class TestMidiReceiveLoopSemantics:
    class Consumer:
        def __init__(self):
            self.events = []

        def __call__(self, event):
            self.events.append(event)

    def test_receive_loop_emits_normalized_events_to_consumer(self) -> None:
        midi_input = MemoryMidiInput((NoteEvent.note_on(1, 60, 0),))
        consumer = self.Consumer()
        loop = MidiReceiveLoop(
            midi_input=midi_input,
            event_consumer=consumer,
            event_processor=MidiNoteState(),
        )

        midi_input.open()
        assert loop.poll_once() is True

        assert tuple(event.message_type for event in consumer.events) == ("note_off",)
        assert loop.received_count == 1

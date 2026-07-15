# Bestand: midi_semantics.py
# Versienommer: 0.1.0
# Doel: Normaliseer MIDI-nootlewensiklusse en voorkom hangende aktiewe note.
# Sprint: Sprint 2
# Epic: MCP-EPIC-002 MIDI And Clock
# User-Story: MCP-US-009 Velocity And Note-Off Semantics
# Actienr: MCP-ACT-009-GREEN-001
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-009

from midi_chip_platform.events import NoteEvent


class MidiNoteState:
    def __init__(self):
        self._active_notes = set()

    @property
    def active_notes(self):
        return tuple(sorted(self._active_notes))

    def process(self, event):
        if event.message_type == "note_on":
            if event.velocity == 0:
                normalized = NoteEvent.note_off(event.channel, event.note, 0)
                self._active_notes.discard((event.channel, event.note))
                return (normalized,)
            self._active_notes.add((event.channel, event.note))
            return (event,)
        if event.message_type == "note_off":
            self._active_notes.discard((event.channel, event.note))
            return (event,)
        if event.message_type == "control_change" and event.control in (120, 123):
            return self._release_channel(event.channel)
        return (event,)

    def _release_channel(self, channel):
        released_notes = []
        for active_channel, note in self.active_notes:
            if active_channel == channel:
                released_notes.append(NoteEvent.note_off(channel, note, 0))
                self._active_notes.discard((active_channel, note))
        return tuple(released_notes)

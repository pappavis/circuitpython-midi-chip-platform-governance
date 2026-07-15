# Bestand: test_usb_midi_receive.py
# Versienommer: 0.1.0
# Doel: Bewys rou USB-MIDI-vertaling en 'n begrensde ontvangslus sonder hardeware.
# Sprint: Sprint 2
# Epic: MCP-EPIC-002 MIDI And Clock
# User-Story: MCP-US-007 USB MIDI Receive Loop
# Actienr: MCP-ACT-007-RED-001
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-007

from midi_chip_platform.midi_usb import MidiMessageTranslator, MidiMessageTypes, UsbMidiInputPort


class TestUsbMidiReceive:
    class NoteOn:
        def __init__(self, note, velocity, channel=0):
            self.note = note
            self.velocity = velocity
            self.channel = channel

    class NoteOff:
        def __init__(self, note, velocity=0, channel=0):
            self.note = note
            self.velocity = velocity
            self.channel = channel

    class ControlChange:
        def __init__(self, control, value, channel=0):
            self.control = control
            self.value = value
            self.channel = channel

    class PitchBend:
        def __init__(self, pitch_bend, channel=0):
            self.pitch_bend = pitch_bend
            self.channel = channel

    class TimingClock:
        pass

    class Unknown:
        pass

    class RawMidi:
        def __init__(self, messages):
            self._messages = list(messages)

        def receive(self):
            if not self._messages:
                return None
            return self._messages.pop(0)

    class Factory:
        def __init__(self, raw_midi):
            self._raw_midi = raw_midi
            self.requested_port_index = None

        def create(self, port_index):
            self.requested_port_index = port_index
            return self._raw_midi

    def _translator(self):
        return MidiMessageTranslator(
            MidiMessageTypes(
                note_on_type=self.NoteOn,
                note_off_type=self.NoteOff,
                control_change_type=self.ControlChange,
                pitch_bend_type=self.PitchBend,
                timing_clock_type=self.TimingClock,
            )
        )

    def test_translates_note_and_control_messages_to_portable_events(self) -> None:
        translator = self._translator()

        note = translator.translate(self.NoteOn(note=60, velocity=99, channel=3))
        control = translator.translate(self.ControlChange(control=1, value=64, channel=0))
        bend = translator.translate(self.PitchBend(pitch_bend=12000, channel=15))
        clock = translator.translate(self.TimingClock())

        assert (note.message_type, note.channel, note.note, note.velocity) == ("note_on", 4, 60, 99)
        assert (control.message_type, control.channel, control.control, control.value) == (
            "control_change",
            1,
            1,
            64,
        )
        assert (bend.message_type, bend.channel, bend.value) == ("pitch_bend", 16, 12000)
        assert (clock.message_type, clock.channel) == ("timing_clock", None)

    def test_input_port_is_bounded_and_ignores_unknown_messages(self) -> None:
        raw_midi = self.RawMidi((self.Unknown(), self.NoteOff(note=62, velocity=7, channel=1)))
        factory = self.Factory(raw_midi)
        port = UsbMidiInputPort(factory=factory, translator=self._translator(), port_index=2)

        port.open()
        assert port.receive() is None
        event = port.receive()
        port.close()

        assert factory.requested_port_index == 2
        assert (event.message_type, event.channel, event.note, event.velocity) == (
            "note_off",
            2,
            62,
            7,
        )
        assert port.is_open is False

    def test_input_port_requires_open_before_receive(self) -> None:
        port = UsbMidiInputPort(
            factory=self.Factory(self.RawMidi(())),
            translator=self._translator(),
        )

        try:
            port.receive()
        except RuntimeError as error:
            assert str(error) == "USB MIDI input is closed"
        else:
            raise AssertionError("closed USB MIDI input must reject receive")

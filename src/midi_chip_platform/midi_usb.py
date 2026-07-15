# Bestand: midi_usb.py
# Versienommer: 0.2.0
# Doel: Vertaal, normaliseer en ontvang USB-MIDI sonder toestelkonstantes of import-newe-effekte.
# Sprint: Sprint 2
# Epic: MCP-EPIC-002 MIDI And Clock
# User-Story: MCP-US-009 Velocity And Note-Off Semantics
# Actienr: MCP-ACT-009-GREEN-002
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-009

from midi_chip_platform.events import ClockEvent, ControlEvent, NoteEvent
from midi_chip_platform.ports import MidiInputPort


class MidiMessageTypes:
    def __init__(
        self,
        note_on_type,
        note_off_type,
        control_change_type=None,
        pitch_bend_type=None,
        timing_clock_type=None,
        start_type=None,
        stop_type=None,
        continue_type=None,
    ):
        self._note_on_type = note_on_type
        self._note_off_type = note_off_type
        self._control_change_type = control_change_type
        self._pitch_bend_type = pitch_bend_type
        self._timing_clock_type = timing_clock_type
        self._start_type = start_type
        self._stop_type = stop_type
        self._continue_type = continue_type

    @property
    def note_on_type(self):
        return self._note_on_type

    @property
    def note_off_type(self):
        return self._note_off_type

    @property
    def control_change_type(self):
        return self._control_change_type

    @property
    def pitch_bend_type(self):
        return self._pitch_bend_type

    @property
    def timing_clock_type(self):
        return self._timing_clock_type

    @property
    def start_type(self):
        return self._start_type

    @property
    def stop_type(self):
        return self._stop_type

    @property
    def continue_type(self):
        return self._continue_type


class MidiMessageTranslator:
    def __init__(self, message_types):
        if not isinstance(message_types, MidiMessageTypes):
            raise TypeError("message_types must be MidiMessageTypes")
        self._message_types = message_types

    def translate(self, message):
        if message is None:
            return None
        if isinstance(message, self._message_types.note_on_type):
            return NoteEvent.note_on(self._domain_channel(message), message.note, message.velocity)
        if isinstance(message, self._message_types.note_off_type):
            return NoteEvent.note_off(self._domain_channel(message), message.note, message.velocity)
        if self._matches(message, self._message_types.control_change_type):
            return ControlEvent.control_change(
                self._domain_channel(message), message.control, message.value
            )
        if self._matches(message, self._message_types.pitch_bend_type):
            return ControlEvent.pitch_bend(self._domain_channel(message), message.pitch_bend)
        if self._matches(message, self._message_types.timing_clock_type):
            return ClockEvent.timing_clock()
        if self._matches(message, self._message_types.start_type):
            return ClockEvent.start()
        if self._matches(message, self._message_types.stop_type):
            return ClockEvent.stop()
        if self._matches(message, self._message_types.continue_type):
            return ClockEvent.continue_playback()
        return None

    @staticmethod
    def _domain_channel(message):
        return int(message.channel) + 1

    @staticmethod
    def _matches(message, expected_type):
        return expected_type is not None and isinstance(message, expected_type)


class UsbMidiInputPort(MidiInputPort):
    def __init__(self, factory, translator, port_index=0):
        if not isinstance(translator, MidiMessageTranslator):
            raise TypeError("translator must be MidiMessageTranslator")
        if int(port_index) < 0:
            raise ValueError("port_index must be zero or greater")
        self._factory = factory
        self._translator = translator
        self._port_index = int(port_index)
        self._raw_midi = None

    @property
    def is_open(self):
        return self._raw_midi is not None

    def open(self):
        if not self.is_open:
            self._raw_midi = self._factory.create(self._port_index)

    def receive(self):
        if not self.is_open:
            raise RuntimeError("USB MIDI input is closed")
        return self._translator.translate(self._raw_midi.receive())

    def close(self):
        self._raw_midi = None


class AdafruitMidiObjectFactory:
    def __init__(self, midi_class, usb_midi_module):
        self._midi_class = midi_class
        self._usb_midi_module = usb_midi_module

    def create(self, port_index):
        ports = self._usb_midi_module.ports
        if int(port_index) >= len(ports):
            raise ValueError("USB MIDI input port index is unavailable")
        return self._midi_class(midi_in=ports[int(port_index)], in_channel=None)


class CircuitPythonUsbMidiFactory:
    def __init__(self, importer=None):
        self._importer = importer if importer is not None else __import__

    def create_input(self, port_index=0):
        adafruit_midi = self._importer("adafruit_midi", fromlist=("MIDI",))
        usb_midi = self._importer("usb_midi")
        message_types = MidiMessageTypes(
            note_on_type=self._message_type("adafruit_midi.note_on", "NoteOn"),
            note_off_type=self._message_type("adafruit_midi.note_off", "NoteOff"),
            control_change_type=self._message_type(
                "adafruit_midi.control_change", "ControlChange"
            ),
            pitch_bend_type=self._message_type("adafruit_midi.pitch_bend", "PitchBend"),
            timing_clock_type=self._optional_message_type(
                "adafruit_midi.timing_clock", "TimingClock"
            ),
            start_type=self._optional_message_type("adafruit_midi.start", "Start"),
            stop_type=self._optional_message_type("adafruit_midi.stop", "Stop"),
            continue_type=self._optional_message_type(
                "adafruit_midi.midi_continue", "Continue"
            ),
        )
        return UsbMidiInputPort(
            factory=AdafruitMidiObjectFactory(adafruit_midi.MIDI, usb_midi),
            translator=MidiMessageTranslator(message_types),
            port_index=port_index,
        )

    def _message_type(self, module_name, class_name):
        module = self._importer(module_name, fromlist=(class_name,))
        return getattr(module, class_name)

    def _optional_message_type(self, module_name, class_name):
        try:
            return self._message_type(module_name, class_name)
        except (ImportError, AttributeError):
            return None


class MidiReceiveLoop:
    def __init__(self, midi_input, event_consumer, event_processor=None):
        if not isinstance(midi_input, MidiInputPort):
            raise TypeError("midi_input must implement MidiInputPort")
        self._midi_input = midi_input
        self._event_consumer = event_consumer
        self._event_processor = event_processor
        self._received_count = 0

    @property
    def received_count(self):
        return self._received_count

    def poll_once(self):
        event = self._midi_input.receive()
        if event is None:
            return False
        events = (event,)
        if self._event_processor is not None:
            events = self._event_processor.process(event)
        for processed_event in events:
            self._event_consumer(processed_event)
        self._received_count += 1
        return True

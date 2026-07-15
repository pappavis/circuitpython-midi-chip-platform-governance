# Bestand: midi_performance.py
# Versienommer: 0.1.0
# Doel: Besit per-kanaal pitch-bend- en CC1-modulasiestatus vir synth-kerns.
# Sprint: Sprint 2
# Epic: MCP-EPIC-002 MIDI And Clock
# User-Story: MCP-US-010 Pitch Bend And CC1 Modulation
# Actienr: MCP-ACT-010-GREEN-001
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-010


class MidiPerformanceChannelState:
    def __init__(self, channel, pitch_bend_value=8192, pitch_bend_semitones=0.0, modulation=0.0):
        self._channel = int(channel)
        self._pitch_bend_value = int(pitch_bend_value)
        self._pitch_bend_semitones = float(pitch_bend_semitones)
        self._modulation = float(modulation)

    @property
    def channel(self):
        return self._channel

    @property
    def pitch_bend_value(self):
        return self._pitch_bend_value

    @property
    def pitch_bend_semitones(self):
        return self._pitch_bend_semitones

    @property
    def modulation(self):
        return self._modulation


class MidiPerformanceState:
    def __init__(self, pitch_bend_range=2.0):
        if float(pitch_bend_range) <= 0:
            raise ValueError("pitch_bend_range must be greater than zero")
        self._pitch_bend_range = float(pitch_bend_range)
        self._channels = {}

    @property
    def pitch_bend_range(self):
        return self._pitch_bend_range

    def channel_state(self, channel):
        self._validate_channel(channel)
        current = self._channels.get(int(channel))
        if current is None:
            return MidiPerformanceChannelState(channel)
        return current

    def process(self, event):
        if event.message_type == "pitch_bend":
            current = self.channel_state(event.channel)
            semitones = ((event.value - 8192) / 8192.0) * self._pitch_bend_range
            self._channels[event.channel] = MidiPerformanceChannelState(
                channel=event.channel,
                pitch_bend_value=event.value,
                pitch_bend_semitones=semitones,
                modulation=current.modulation,
            )
        elif event.message_type == "control_change" and event.control == 1:
            current = self.channel_state(event.channel)
            self._channels[event.channel] = MidiPerformanceChannelState(
                channel=event.channel,
                pitch_bend_value=current.pitch_bend_value,
                pitch_bend_semitones=current.pitch_bend_semitones,
                modulation=event.value / 127.0,
            )
        return (event,)

    @staticmethod
    def _validate_channel(channel):
        if not 1 <= int(channel) <= 16:
            raise ValueError("channel must be between 1 and 16")

# Bestand: platform_capabilities.py
# Versienommer: 0.1.0
# Doel: Ontdek bord-, pen-, module-, geheue- en klankbackend-vermoens sonder import-newe-effekte.
# Sprint: Sprint 1
# Epic: MCP-EPIC-001 Platform Foundation
# User-Story: MCP-US-004 Board Capability Discovery
# Actienr: MCP-ACT-004-GREEN-001
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-004


class I2sPinProfile:
    def __init__(
        self,
        bit_clock,
        word_select,
        data,
        amplifier_data_label="DIN",
        is_available=False,
    ):
        pin_names = (str(bit_clock), str(word_select), str(data))
        if len(set(pin_names)) != len(pin_names):
            raise ValueError("I2S pin assignments must be unique")
        self._bit_clock = pin_names[0]
        self._word_select = pin_names[1]
        self._data = pin_names[2]
        self._amplifier_data_label = str(amplifier_data_label)
        self._is_available = bool(is_available)

    @property
    def bit_clock(self):
        return self._bit_clock

    @property
    def word_select(self):
        return self._word_select

    @property
    def data(self):
        return self._data

    @property
    def amplifier_data_label(self):
        return self._amplifier_data_label

    @property
    def is_available(self):
        return self._is_available

    def resolved_for(self, board_module):
        available = all(
            hasattr(board_module, pin_name)
            for pin_name in (self._bit_clock, self._word_select, self._data)
        )
        return I2sPinProfile(
            bit_clock=self._bit_clock,
            word_select=self._word_select,
            data=self._data,
            amplifier_data_label=self._amplifier_data_label,
            is_available=available,
        )


class BoardCapabilityProfile:
    def __init__(self, board_id, i2s_pins=None):
        self._board_id = str(board_id)
        self._i2s_pins = i2s_pins

    @property
    def board_id(self):
        return self._board_id

    @property
    def i2s_pins(self):
        return self._i2s_pins


class BoardProfileRegistry:
    def __init__(self, profiles):
        self._profiles = tuple(profiles)

    @classmethod
    def default(cls):
        return cls((cls.create_lolin_s2_mini(),))

    @classmethod
    def create_lolin_s2_mini(cls, bit_clock="IO5", word_select="IO3", data="IO7"):
        return BoardCapabilityProfile(
            board_id="lolin_s2_mini",
            i2s_pins=I2sPinProfile(
                bit_clock=bit_clock,
                word_select=word_select,
                data=data,
                amplifier_data_label="DIN",
            ),
        )

    def resolve(self, board_id):
        normalized_board_id = str(board_id)
        for profile in self._profiles:
            if profile.board_id == normalized_board_id:
                return profile
        return None


class ImportModuleProbe:
    def __init__(self, importer):
        self._importer = importer
        self._results = {}

    def available(self, module_name):
        normalized_name = str(module_name)
        if normalized_name not in self._results:
            try:
                self._importer(normalized_name)
                self._results[normalized_name] = True
            except ImportError:
                self._results[normalized_name] = False
        return self._results[normalized_name]


class MemoryProbe:
    def __init__(self, gc_module):
        self._gc_module = gc_module

    def free_bytes(self):
        return self._read_metric("mem_free")

    def allocated_bytes(self):
        return self._read_metric("mem_alloc")

    def _read_metric(self, method_name):
        method = getattr(self._gc_module, method_name, None)
        if method is None:
            return None
        try:
            return int(method())
        except (AttributeError, TypeError, ValueError):
            return None


class BoardCapabilitySnapshot:
    def __init__(
        self,
        board_id,
        profile_status,
        i2s_pins,
        module_results,
        memory_free_bytes,
        memory_allocated_bytes,
        audio_backends,
    ):
        self._board_id = str(board_id)
        self._profile_status = str(profile_status)
        self._i2s_pins = i2s_pins
        self._module_results = tuple(module_results)
        self._memory_free_bytes = memory_free_bytes
        self._memory_allocated_bytes = memory_allocated_bytes
        self._audio_backends = tuple(audio_backends)

    @property
    def board_id(self):
        return self._board_id

    @property
    def profile_status(self):
        return self._profile_status

    @property
    def i2s_pins(self):
        return self._i2s_pins

    @property
    def memory_free_bytes(self):
        return self._memory_free_bytes

    @property
    def memory_allocated_bytes(self):
        return self._memory_allocated_bytes

    @property
    def audio_backends(self):
        return self._audio_backends

    def module_available(self, module_name):
        normalized_name = str(module_name)
        for name, available in self._module_results:
            if name == normalized_name:
                return available
        return False

    def report_lines(self):
        lines = [
            "CAPABILITY_DISCOVERY_STATUS=PASS",
            f"BOARD_ID={self._board_id}",
            f"BOARD_PROFILE={self._profile_status}",
        ]
        if self._i2s_pins is None:
            lines.append("I2S_PINS=UNCONFIGURED")
        else:
            lines.append(
                "I2S_PINS="
                f"BCLK:{self._i2s_pins.bit_clock},"
                f"WS:{self._i2s_pins.word_select},"
                f"DATA:{self._i2s_pins.data}->{self._i2s_pins.amplifier_data_label}"
            )
            pin_status = "AVAILABLE" if self._i2s_pins.is_available else "MISSING"
            lines.append(f"I2S_PIN_STATUS={pin_status}")
        lines.append(f"MODULES={self._format_modules()}")
        lines.append(f"MEMORY_FREE_BYTES={self._format_metric(self._memory_free_bytes)}")
        lines.append(
            f"MEMORY_ALLOCATED_BYTES={self._format_metric(self._memory_allocated_bytes)}"
        )
        backends = ",".join(self._audio_backends) if self._audio_backends else "NONE"
        lines.append(f"AUDIO_BACKENDS={backends}")
        return tuple(lines)

    def _format_modules(self):
        return ",".join(
            f"{name}:{'yes' if available else 'no'}"
            for name, available in self._module_results
        )

    @staticmethod
    def _format_metric(value):
        return "UNAVAILABLE" if value is None else str(value)


class BoardCapabilityDiscovery:
    def __init__(self, board_module, module_probe, memory_probe, profile_registry):
        self._board_module = board_module
        self._module_probe = module_probe
        self._memory_probe = memory_probe
        self._profile_registry = profile_registry

    def discover(self):
        board_id = getattr(self._board_module, "board_id", "unknown")
        profile = self._profile_registry.resolve(board_id)
        module_names = ("audiobusio", "audiopwmio", "synthio", "usb_midi", "wifi")
        module_results = tuple(
            (module_name, self._module_probe.available(module_name))
            for module_name in module_names
        )
        i2s_pins = None
        if profile is not None and profile.i2s_pins is not None:
            i2s_pins = profile.i2s_pins.resolved_for(self._board_module)
        audio_backends = self._resolve_audio_backends(i2s_pins, module_results)
        return BoardCapabilitySnapshot(
            board_id=board_id,
            profile_status="KNOWN" if profile is not None else "UNKNOWN",
            i2s_pins=i2s_pins,
            module_results=module_results,
            memory_free_bytes=self._memory_probe.free_bytes(),
            memory_allocated_bytes=self._memory_probe.allocated_bytes(),
            audio_backends=audio_backends,
        )

    @staticmethod
    def _resolve_audio_backends(i2s_pins, module_results):
        availability = dict(module_results)
        backends = []
        if i2s_pins is not None and i2s_pins.is_available and availability.get("audiobusio"):
            backends.append("i2s-max98357a-mono")
        if availability.get("audiopwmio"):
            backends.append("pwm-diagnostic-unconfigured")
        return tuple(backends)


class CircuitPythonCapabilityFactory:
    def __init__(self, importer):
        self._importer = importer

    def create_discovery(self):
        board_module = self._importer("board")
        gc_module = self._importer("gc")
        return BoardCapabilityDiscovery(
            board_module=board_module,
            module_probe=ImportModuleProbe(self._importer),
            memory_probe=MemoryProbe(gc_module),
            profile_registry=BoardProfileRegistry.default(),
        )

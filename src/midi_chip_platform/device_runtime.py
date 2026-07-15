# Bestand: device_runtime.py
# Versienommer: 0.11.1
# Doel: Lewer toestel-, dependency-, capability- en konfigurasiebewys sonder diensstart.
# Sprint: Sprint 2
# Epic: MCP-EPIC-008 Portability, Quality And Release
# User-Story: MCP-US-051/MCP-US-007 Dependency-Closed Deployment Impediment
# Actienr: MCP-ACT-051-IMP-001-GREEN-002
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-051-IMP-001

from midi_chip_platform.release import ReleaseMetadata


class DeviceImportSmokeCheck:
    def __init__(self, importer, module_names):
        normalized_names = tuple(str(module_name) for module_name in module_names)
        if not normalized_names:
            raise ValueError("device import smoke check requires module names")
        self._importer = importer
        self._module_names = normalized_names

    def run(self):
        for module_name in self._module_names:
            self._importer(module_name)
        return True


class DeviceRuntimeApplication:
    def __init__(
        self,
        release_metadata,
        capability_discovery=None,
        configuration_loader=None,
        import_smoke_check=None,
        output=None,
    ):
        if not isinstance(release_metadata, ReleaseMetadata):
            raise TypeError("release_metadata must be ReleaseMetadata")
        self._release_metadata = release_metadata
        self._capability_discovery = capability_discovery
        self._configuration_loader = configuration_loader
        self._import_smoke_check = import_smoke_check
        self._output = output if output is not None else print

    def run(self):
        self._output(self._release_metadata.banner())
        if self._capability_discovery is not None:
            snapshot = self._capability_discovery.discover()
            for line in snapshot.report_lines():
                self._output(line)
        if self._configuration_loader is not None:
            configuration = self._configuration_loader.load()
            for line in configuration.report_lines():
                self._output(line)
        if self._import_smoke_check is not None:
            self._import_smoke_check.run()
            self._output("DEVICE_IMPORT_STATUS=PASS")
        self._output("DEVICE_EXECUTION_STATUS=READY")
        return True

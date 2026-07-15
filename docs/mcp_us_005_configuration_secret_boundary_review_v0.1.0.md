# MCP-US-005 Configuration And Secret Boundary Review

<!--
Bestand: mcp_us_005_configuration_secret_boundary_review_v0.1.0.md
Versienommer: 0.2.0
Doel: Dokumenteer die publieke konfigurasie, private settings-grens, toetse en HIL-hek.
Sprint: Sprint 1
Epic: MCP-EPIC-001 Platform Foundation
User-Story: MCP-US-005 Configuration And Secret Boundary
Actienr: MCP-ACT-051-IMP-001-DOC-005
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-051-IMP-001
-->

## Status

**IN REVIEW / MENSLIKE KONFIGURASIEHEK.** Die klasgebaseerde implementering, geheime-redaksie en host-regressie is groen. Die 2026-07-15 dependency-closed deploy het bewys dat die volume skryfbaar is en dat die konfigurasielaag op die Wemos S2 sonder import-/runtimefout laai. Private `SET`/`UNSET`-aanvaarding bly oop.

## Konfigurasieprioriteit

Van hoogste na laagste:

1. Geïnjekteerde runtime-overrides.
2. `CIRCUITPY/settings.toml`, gelees deur `os.getenv()`.
3. Publieke, klasinstansie-besitte verstekke.

Die huidige publieke klankprofiel is mono MAX98357A met IO5 BCLK, IO3 WS/LRC en IO7 DATA/DIN. Geen klank- of Wi-Fi-diens word deur hierdie story begin nie.

## Geheimegrens

- `wifi.ssid`, `wifi.password` en `web.ap.password` word as private sleutels behandel.
- Diagnostiek rapporteer slegs `SET` of `UNSET`, nooit die waarde nie.
- `public_items()` sluit private sleutels en waardes uit.
- `settings.toml` bly in `.gitignore`; `device/settings.toml.example` bevat slegs plekhouers.
- Die ou prototipewagwoord bly 'n roteeraksie vir die Product Owner voordat Wi-Fi-stories begin.

## RED/GREEN-bewys

- RED: toetsinsameling het met die verwagte `ModuleNotFoundError` vir `midi_chip_platform.configuration` gefaal.
- GREEN: 40 hosttoetse slaag op `v0.5.0`; AST- en importveiligheidsreëls bly groen.
- Geheimekontrole: kunsmatige SSID- en wagwoordwaardes verskyn nie in `report_lines()` of publieke items nie.
- Toestelherbewys: CIRCUITPY/CDC, manifest, libraries, boot, config-import en execution het geslaag; private waardes is nie gepubliseer nie.

## Menslike aanvaardingshek

1. Maak Thonny en enige serial monitor toe.
2. Stel slegs veilige toetswaardes in 'n private `settings.toml`; commit dit nooit.
3. Hard-reset en bevestig dat diagnostiek slegs private `SET`/`UNSET`-status toon, nooit waardes nie.
4. Verwyder die toetswaardes en bevestig dat publieke verstekke terugkeer.

## Virtuele spanreview

| Rol | Bydrae |
|---|---|
| Product Owner | Het US-005 en US-006 vooraf goedgekeur en menslike toetsing vir ná werk beplan. |
| Scrum Master | Hou Wi-Fi-verbinding en klankaktivering buite US-005; log die leesalleen-HIL-hek. |
| Business Analyst | Definieer override, private settings en publieke verstekke as drie eksplisiete lae. |
| Solution Architect | Vereis `ConfigurationPort`, dependency injection en geen import-newe-effekte. |
| Embedded Engineer | Gebruik CircuitPython `os.getenv()` en raak nie die bestaande private `settings.toml` aan nie. |
| MIDI Engineer | Not impacted: geen MIDI-boodskap word in US-005 ontvang of verander nie. |
| DSP/Chip Engineer | Behou die goedgekeurde MAX98357A-penprofiel maar aktiveer geen audio nie. |
| Web Engineer | Bevestig dat latere station/AP-credentials deur dieselfde private grens kom. |
| QA/HIL Engineer | Lewer RED/GREEN, lektoetse, FAT-verifikasie en 'n nie-destruktiewe menslike herstelhek. |
| Release/Documentation | Sinkroniseer weergawe, quickstart, bronne, risiko, lessons learned en Kanban. |
| External Architecture Reviewer (Copilot) | Not impacted: geen nuwe reviewer-inset is vir US-005 ontvang nie. |
| Devil's Advocate | Waarsku dat `settings.toml` skeiding bied, maar nie enkripsie of credential-rotasie vervang nie. |

## LLM-gebruik

Geen plaaslike Ollama-model is gebruik nie.

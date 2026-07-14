# MCP-US-001: Toestel- en bronbasislyn

<!--
Bestand: mcp_us_001_device_source_baseline_inventory_v0.1.0.md
Versienommer: 0.1.0
Doel: Inventariseer toestel, prototipes, bronne, hergebruik en veiligheidsbevindinge.
Sprint: Sprint 0
Epic: MCP-EPIC-001 Platform Foundation
User-Story: MCP-US-001 Device And Source Baseline Inventory
Actienr: MCP-ACT-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001
-->

## Story

As produkspan wil ons die werklike toestel, bestaande kode en eksterne bronne inventariseer, sodat die nuwe repository op bevestigde vermoëns en eksplisiete risiko’s begin.

## Aanvaardingskriteria

- Die verwysingsbord, firmware, gemonteerde volume en USB-seriële toegang is leesalleen bevestig.
- ’n private rugsteun bestaan buite die Git-repository en pas by die toestelinhoud.
- Herbruikbare kode en toetse uit beide voorgangerprojekte is geklassifiseer.
- Geen Wi-Fi-geheim, unieke toestel-ID of private rugsteun verskyn in Git nie.
- Elke virtuele spanrol het ’n sigbare bydrae en opvolgaksie.
- MVP-grense, risiko’s en volgende story is naspeurbaar.

## Bevestigde verwysingstoestel

| Eienskap | Waarneming | Gevolgtrekking |
|---|---|---|
| Bord | LOLIN/Wemos ESP32-S2 Mini | Primêre MVP-verwysingsbord |
| Firmware | CircuitPython 10.0.3 | Basislyn; opgradering is ’n aparte beheerde story |
| USB | Native USB, seriële REPL en CIRCUITPY-volume beskikbaar | Ontplooiing en diagnostiek is haalbaar |
| MIDI-biblioteek | `adafruit_midi` met Note, CC, Pitch Bend en klokmodules teenwoordig | Kontrakspike kan sonder nuwe bundel begin |
| Berging | Ongeveer 0.9 MiB sigbaar, ongeveer 0.5 MiB vry tydens inventaris | Webbates en kerne moet klein bly |
| Klankprototipe | Twee PWM-uitsette, panning en drie toonstemme bestaan | PWM is die laerisiko diagnostiese basislyn |
| Netwerk | Bestaande prototipe probeer Wi-Fi tydens boot | Moet uit `boot.py` na runtime verskuif word |

Unieke poortname, USB-ID’s en plaaslike netwerkname word doelbewus nie hier gepubliseer nie.

## Private rugsteun

’n lêervlak-rugsteun van die CIRCUITPY-volume is op 2026-07-14 gemaak en met ’n droë `rsync`-vergelyking geverifieer. Die rugsteun is buite hierdie repository gestoor, met groep- en ander-toegang verwyder. Stelselgidse soos `.Trashes` en `.fseventsd` is uitgesluit.

## Prototipebevindinge

### Huidige toestel

- `sn76489lite_main.py` bewys ’n klasgebaseerde driestem-PSG, panning en stereo-PWM.
- `audio_pwm.py` bevat ’n kleiner stereo-PWM-driver, maar ’n statiese helper en naamkonvensies moet herstel word.
- `boot.py` meng USB-konfigurasie, netwerkontdekking en toepassingstart; dit is te veel verantwoordelikheid vir bootfase.
- ’n verkeerd benoemde `settings.toml`-agtige lêer dui op ’n konfigurasie-/lêernaamrisiko.

### `pappavis/midi-chip-platform`

- Die huidige hoofimplementasie is CPython-georiënteerd (`mido`, `numpy`, `sounddevice`) en kan nie direk op CircuitPython loop nie.
- ’n gearchiveerde v0.1-struktuur bevat nuttige grense: `AudioService`, `MidiService`, `ClockService`, `ChipManager`, `PinAllocator` en `SN76489Chip`.
- Die argief se kernklas is hoofsaaklik ’n kontrak/stomp; dit is nie bewese klankemulasie nie.
- Die repository bevat bruikbare governance, backlog- en rolpatrone, maar sy statusse moet onafhanklik geverifieer word.

### `pappavis/python-d1-synth`

Die volgende gedragskontrakte is sterk hergebruikkandidate:

- note- en volgordemodelle;
- MIDI-kanaalnormalisering;
- Note On met velocity nul as Note Off;
- pitch-bend- en CC1-mapping;
- duplikaat-MIDI-beskerming;
- polifoniese triades en voice lifecycle;
- sustain/All Notes Off;
- ADSR-kontrakte;
- links/regs/stereo-roetering;
- konfigurasievoorrang en kode-naspeurbaarheid.

Die CPython-klank- en MIDI-backends self word nie na CircuitPython gekopieer nie.

## Veiligheidsbevindinge

| ID | Bevinding | Ernst | Vereiste aksie |
|---|---|---:|---|
| SEC-001 | ’n Wi-Fi-wagwoord was hardgekodeer in prototipekode | Kritiek | Roteer die wagwoord; gebruik ’n Git-geïgnoreerde `settings.toml` |
| SEC-002 | Netwerkskandering en verbinding gebeur in `boot.py` | Hoog | Hou `boot.py` minimaal; begin netwerk onder runtime-beheer |
| SEC-003 | ’n derdeparty VID/PID word in USB-identifikasie gebruik | Hoog | Gebruik veilige verstekke tydens ontwikkeling; ondersoek geldige produk-ID voor verspreiding |
| SEC-004 | Webbeheer kan toestelbronne en plaaslike netwerk blootstel | Hoog | MVP slegs op vertroude LAN, enkele kliënt, geen internetpublikasie |
| SEC-005 | Private rugsteun kan geheime bevat | Hoog | Hou buite Git; beperk lêertoegang; publiseer slegs gesaniteerde bevindinge |

## Spanbydraes

| Rol | Bydrae tot MCP-US-001 | Opvolg |
|---|---|---|
| Sales/Discovery | Produkdefinisie en kitaarpedaal-gebruik bevestig | Toets waardeproposisie met een musikant |
| Business Analyst | MVP teenoor parkeerterrein geskei | Verfyn meetbare gebruikerstrome |
| Product Owner | SN76489, USB-MIDI en hoorbare bewys geprioritiseer | Aanvaar story per hardeware-resultaat |
| Scrum Master | Afhanklikhede en besluithekke georden | Beskerm storyvolgorde teen side quests |
| Solution Architect | Poortgebaseerde multi-kern-argitektuur gekies | Definieer interfaces in MCP-US-002 |
| Embedded Engineer | Bord, firmware, volume en prototipes bevestig | Bou minimale veilige boot in MCP-US-003 |
| MIDI Engineer | Biblioteek- en boodskapvermoëns bevestig | Skryf host/board MIDI-kontrakte |
| DSP/Chip Engineer | PWM-prototipe en driestemlimiet geëvalueer | Definieer SN76489-lite akkuraatheidsvlak |
| Web Engineer | HTTP/WebSocket-haalbaarheid en beperking erken | Ontwerp eenkliënt beheerprotokol |
| QA/HIL Engineer | Rugsteun, rooi/groen en meetbare I/O-toetse vereis | Skep host-simulator en HIL-runbook |
| Release/Docs | Openbare/private skeiding en naspeurbaarheid vasgelê | Handhaaf changelog, headers en installasiepad |

## Uitkoms

MCP-US-001 is dokumentêr gereed vir Product Owner-aanvaarding. Die veilige volgende stap is **MCP-US-002: Clean Repository And Project Skeleton**. Dit skep slegs die klasgebaseerde poorte, host-toetsopstelling en minimale lêerstruktuur; toestelontplooiing bly ’n latere story.


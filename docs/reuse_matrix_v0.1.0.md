# Hergebruiksmatriks

<!--
Bestand: reuse_matrix_v0.1.0.md
Versienommer: 0.1.0
Doel: Besluit wat hergebruik, geporteer, herskryf of verwerp word.
Sprint: Sprint 0
Epic: MCP-EPIC-001 Platform Foundation
User-Story: MCP-US-001 Device And Source Baseline Inventory
Actienr: MCP-ACT-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001
-->

| Bron | Element | Besluit | Rede | Vereiste bewys voor gebruik |
|---|---|---|---|---|
| Toestelprototipe | `PSG76489LiteStereo` | Port en toets | Reeds hoorbare drie-stem/pan-bewys | Host-golden samples, frekwensie- en stemtoetse |
| Toestelprototipe | `PWMAudioOutStereo` | Refaktor | Werkende PWM, maar busy-wait kan MIDI/web blokkeer | Latensie-, jitter- en Ctrl-C/REPL-hersteltoets |
| Toestelprototipe | `PracticeSequencer` | Idee hergebruik | Nuttige opstarttoets, maar note verskil van G-C-D-vereiste | Deterministiese G-C-D sestiendenoottoets |
| Toestelprototipe | `boot.py` | Herskryf | Geheime, netwerkwerk, USB- en runtime-verantwoordelikhede gemeng | Minimale boot/safe-mode/USB-endpoint-toets |
| midi-chip-platform argief | `MidiService` | Port kontrak | `adafruit_midi` en USB-poorte pas by mikrobeheerder | Note/CC/bend/clock normaliseringstoetse |
| midi-chip-platform argief | `ClockService` | Inspekteer en herskryf | Goeie grens; implementasie moet teen 24 PPQN gevalideer word | Fake-clock en eksterne-jittertoetse |
| midi-chip-platform argief | `ChipManager` | Port ontwerp | Kanaal-tot-kern-roetering pas by produkdoel | Geen globale status, rollback en meerkernkontrakte |
| midi-chip-platform argief | `PinAllocator` | Port | Belangrik vir willekeurige borde | Botsing, alias en onbekende-pen-toetse |
| midi-chip-platform argief | `SN76489Chip` | Kontrak slegs | Metodes is hoofsaaklik stubs; geen klankbewys | Koppel aan getoetste SN76489-lite-enjin |
| midi-chip-platform huidige | CPython monoliet | Gedragsverwysing | Kan nie op CircuitPython loop nie | Geen direkte invoer van `mido/numpy/sounddevice` |
| python-d1-synth | NoteEvent/sequence-kontrakte | Herimplementeer klein | Goed getoets en platform-onafhanklik in betekenis | CircuitPython-versoenbare klasse sonder dataclasses-afhanklikheid indien nodig |
| python-d1-synth | MIDI-normalisering | Herimplementeer | Bewese randgevalle en kanaalsemantiek | Adafruit MIDI fixtures en velocity-zero-toets |
| python-d1-synth | Pitch bend/CC1/sustain | Herimplementeer | Hardeware-getoetste gedrag | Geheue- en kanaalbeleid vir mikrobeheerder |
| python-d1-synth | Dedupe guard | Herimplementeer opsioneel | Nuttig vir duplikaatroetes | Mag nie geldige herhaalde note of klok onderdruk nie |
| python-d1-synth | `sounddevice`/NumPy audio | Verwerp vir firmware | CPython/native afhanklikhede | Slegs host-simulator mag desktopbiblioteke gebruik |
| Adafruit-biblioteke | `adafruit_midi` | Gebruik | Onderhoude boodskapparser vir USB-MIDI | Weergawe vaspen en bundelversoenbaarheid toets |
| CircuitPython runtime | `synthio` | Spike, nie kernfundament nie | Nuttige envelope/pan/bend, maar eksperimenteel en bordafhanklik | Beskikbaarheid, polifonie en CPU/RAM per bord meet |
| CircuitPython runtime | `audiobusio.I2SOut` | Spike | Beter digitale klankpad indien bord/DAC ondersteun | Penprofiel, stereoformaat en dropoutmeting |
| CircuitPython runtime | `pwmio.PWMOut` | MVP-diagnostiek | Reeds op verwysingsbord bewys | RC-filter, vlakke en sample-skedulering meet |

## Reël

“Hergebruik” beteken nie woordelikse kopie nie. Elke kandidaat moet die nuwe poortkontrak, kodeheader, klasreël, geheimegrens en rooi/groen-toetse slaag.


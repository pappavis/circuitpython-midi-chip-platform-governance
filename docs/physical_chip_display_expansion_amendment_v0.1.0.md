# Physical Chip And Display Expansion Amendment

<!--
Bestand: physical_chip_display_expansion_amendment_v0.1.0.md
Versienommer: 0.1.0
Doel: Orden eksterne displays en fisiese retrochips ná MVP sonder scope-drift.
Sprint: Post-MVP discovery
Epic: MCP-EPIC-010 Physical Chip And Display Expansion
User-Story: MCP-US-069 tot MCP-US-074
Actienr: MCP-ACT-PHYSICAL-001-SCOPE-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-007-ACCEPTANCE-START
-->

## Besluit

Die MVP bly op die emuleerde D1-basiskern, MAX98357 mono-I2S en daarna SN76489-Lite. SSD1306-status, fisiese SN76489/SID6581/OPL2 en ArduinoOPL2-SPI is waardevolle uitbreidings, maar hulle word nie tussen die huidige afhanklikhede ingeskuif nie.

## Aanbevole argitektuur

`SynthCore` besit musikale gedrag. 'n Afsonderlike, geïnjekteerde `CoreBackendPort` voer die kern se uitset uit:

- `EmulatedAudioBackend` render monsters deur `AudioOutputPort` en is altyd die verstek.
- `PhysicalRegisterBackend` stuur begrensde register-/busopdragte deur 'n `ChipTransportPort` en render nie 'n tweede plaaslike audiostroom nie.
- `ChipCapabilityProbe` bepaal of 'n gekonfigureerde adapter beskikbaar en veilig is; afwesigheid, timeout of fout kies emulasie en rapporteer 'n geredigeerde rede.
- I2C-displaystatus gebruik 'n eie `StatusDisplayPort`; die synth het geen display nodig om te begin of te speel nie.

Hierdie skeiding voorkom dat I2C-, SPI-, pen- of breakoutbesonderhede in MIDI-routing of kernalgoritmes beland. Backendwisseling moet by 'n veilige grens gebeur, nie halfpad deur 'n aktiewe noot nie.

## Elektriese discovery-hek

Voor enige fisiese chipkode moet die Chip Engineer die presiese partnommer, datasheet, voedingsspanning, logikavlakke, klokbron, reset, buswydte, skryftiming en analooguitvoer bevestig. `PCF8574`, 'n 16-bit expander, direkte GPIO, SPI en 'n moontlike DAC is slegs kandidate. Veral die SID-pad kry eers 'n feasibility/no-go-besluit; geen I2C-na-analoog-aanname is goedgekeur nie.

## Bronne en gebruiksgrens

- `DhrBaksteen/ArduinoOPL2/src` word by MCP-US-073 vir SPI-protokol, lisensie en HIL bestudeer.
- `Malvineous/pyopl` word by MCP-US-041 as gedrags-/toetsverwysing geëvalueer; geen hergebruik word vooraf aanvaar nie.
- Die gebruiker se fisiese chipvoorraad is HIL-invoer, nie 'n universele platformkonstante nie.

## Spanbydrae

| Rol | Bydrae |
|---|---|
| Product Owner | Plaas die uitbreiding ná MVP en aanvaar emulasie as verstek/fallback. |
| Scrum Master | Hou MCP-US-069 tot US-074 buite die huidige hoorbare vertikale sny. |
| Business Analyst | Skeur display, transport, chipspesifieke adapters en backendkeuse in toetsbare stories. |
| Chief Enterprise Architect | Plaas fisiese uitvoering agter dieselfde kernvermoë en capabilitymodel. |
| Solution Architect | Definieer `CoreBackendPort`, `ChipTransportPort` en `StatusDisplayPort` as vervangbare grense. |
| Embedded Engineer | Vereis bordprofiele, nie-blokkerende ontdekking en veilige fallback. |
| MIDI Engineer | Not impacted: alle backends ontvang dieselfde draagbare events. |
| DSP/Chip Engineer | Besit elektriese feasibility, registersemantiek, klok en analooguitvoerbewys. |
| Web Engineer | Latere UI kies backend via dieselfde konfigurasiediens; geen eie chiplogika nie. |
| QA/HIL Engineer | Vereis emulasie-, fisiese-, afwesigheid- en fault-injection-bewys per adapter. |
| Release/Documentation | Registreer lisensies, bronweergawes, bekende beperkings en bedrading. |
| External Architecture Reviewer (Copilot) | Not impacted: geen nuwe reviewerbevinding vir hierdie amendment is ontvang nie. |
| Devil's Advocate | Waarsku teen spanningskade, foutiewe chipidentiteit, buslatensie en 'n vals gevoel van hot-swap-veiligheid. |

## LLM-gebruik

Geen plaaslike Ollama-model is vir hierdie amendment gebruik nie.

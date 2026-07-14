# ADR-003: PWM-diagnostiek en I2S-besluitspike

<!--
Bestand: ADR-003-audio-strategy.md
Versienommer: 0.1.0
Doel: Orden PWM en I2S sonder ’n voortydige finale keuse.
Sprint: Sprint 0
Epic: MCP-EPIC-003 Audio And Chip Core
User-Story: MCP-US-001 Device And Source Baseline Inventory
Actienr: MCP-ACT-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001
-->

## Status

Voorlopig aanvaar; finale keuse volg ná MCP-US-016.

## Besluit

- Stereo PWM bly die altyd-beskikbare diagnostiese MVP-pad op die verwysingsbord omdat ’n prototipe reeds werk.
- I2S word met ’n aparte DAC en eksplisiete pen-/geheue-/latensiemeting geëvalueer.
- Alle kerne skryf na ’n `AudioOutput`-poort en ken nie die fisiese backend nie.

## Besluitmaatstawwe

- dropout/jitter tydens MIDI en webpolling;
- CPU- en heapverbruik;
- stereo-integriteit en geraas;
- bordportabiliteit en komponentkoste;
- herstelbaarheid in debugmodus.

## Gevolge

PWM is nie ’n belofte van finale lynvlak-klankgehalte nie. I2S word nie gekies net omdat dit teoreties beter is nie; dit moet op die werklike bord en DAC slaag.


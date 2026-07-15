# MCP-US-007 USB MIDI Receive Loop Review

<!--
Bestand: mcp_us_007_usb_midi_receive_review_v0.1.0.md
Versienommer: 0.1.0
Doel: Dokumenteer die USB-MIDI ontvangsadapter, hostbewys en oorblywende HIL-aanvaarding.
Sprint: Sprint 2
Epic: MCP-EPIC-002 MIDI And Clock
User-Story: MCP-US-007 USB MIDI Receive Loop
Actienr: MCP-ACT-007-REVIEW-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-007-IN-REVIEW
-->

## Gelewer

- `MidiMessageTranslator` vertaal Adafruit Note On, Note Off, CC, pitch bend en klok na die draagbare eventmodel.
- `UsbMidiInputPort` kies 'n poort volgens generiese indeks; geen vervaardiger- of toestelnaam is 'n kodekonstante nie.
- `CircuitPythonUsbMidiFactory` laai hardewaremodules eers wanneer die toesteladapter geskep word.
- `MidiReceiveLoop.poll_once()` is begrens, klasgebaseer en geskik vir 'n latere kooperatiewe scheduler.
- Onbekende boodskappe word veilig geïgnoreer.

## RED/GREEN-bewys

Die nuwe kontraktoets het eers tydens collection gefaal omdat `midi_chip_platform.midi_usb` nog nie bestaan het nie. Ná implementering slaag die volledige hosttoetsstel.

## Status

**In Review.** Hostgedrag is groen. Fisiese USB-MIDI Note On/Off op die Wemos S2 wag totdat die Product Owner weer by die toestel is en die leesalleen `CIRCUITPY`-impediment opgelos is. Geen USB-MIDI-hardewareaanvaarding word uit hosttoetse afgelei nie.

## Menslike toets later

1. Herstel skryftoegang tot `CIRCUITPY` en deploy die HIL-manifest.
2. Koppel enige klas-kompatibele MIDI-bron via rekenaar, DAW of eksterne USB-host.
3. Stuur Note On en Note Off op enige kanaal.
4. Verifieer in die REPL dat die domeinevent se kanaal, noot en velocity korrek is.

Hierdie story maak nog nie klank nie.

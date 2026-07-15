# MCP-US-009 Velocity And Note-Off Semantics Review

<!--
Bestand: mcp_us_009_note_semantics_review_v0.1.0.md
Versienommer: 0.1.0
Doel: Dokumenteer genormaliseerde note-off en vassteekbeveiliging.
Sprint: Sprint 2
Epic: MCP-EPIC-002 MIDI And Clock
User-Story: MCP-US-009 Velocity And Note-Off Semantics
Actienr: MCP-ACT-009-REVIEW-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-009-DONE
-->

## Resultaat

`MidiNoteState` hou aktiewe `(kanaal, noot)`-pare per instansie. Note On met velocity nul word na Note Off genormaliseer. Gewone Note Off verwyder die noot. CC120 All Sound Off en CC123 All Notes Off genereer Note Off-events vir slegs die geteikende kanaal en maak daardie kanaal se toestand leeg.

`MidiReceiveLoop` kan nou 'n ingespuitte eventprocessor gebruik voordat events na die consumer gaan. Die bestaande gedrag sonder processor bly versoenbaar.

## RED/GREEN

Die toetse het eers tydens collection gefaal omdat `midi_semantics` nie bestaan het nie. Ná implementering slaag die volledige stel: **63 passed**.

## Status

**Done.** Die semantiek is hardeware-onafhanklike domeinlogika. Hoorbare release tails en voice shutdown behoort aan die latere klank-/envelope-stories; hierdie story waarborg die korrekte events en skoon aktiewe status.

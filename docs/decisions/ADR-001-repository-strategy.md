# ADR-001: Skoon repository met beheerde hergebruik

<!--
Bestand: ADR-001-repository-strategy.md
Versienommer: 0.1.0
Doel: Besluit die repository- en migrasiestrategie.
Sprint: Sprint 0
Epic: MCP-EPIC-001 Platform Foundation
User-Story: MCP-US-001 Device And Source Baseline Inventory
Actienr: MCP-ACT-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001
-->

## Status

Aanvaar op 2026-07-14.

## Besluit

Skep `pappavis/circuitpython-midi-chip-platform` as ’n skoon repository. Vorige kode word slegs via die hergebruiksmatriks ingevoer, met nuwe kontrakte, headers en toetse.

## Redes

- Die bestaande repo meng CPython, gearchiveerde CircuitPython en dokumentgenerasies.
- Die toestelprototipe bevat waardevolle bewys, maar ook geheime en bootrisiko’s.
- ’n Skoon geskiedenis maak MVP-status, lisensie en release claims eerlik.

## Gevolge

- Aanvanklike tempo is effens stadiger.
- Elke migrasie is meetbaar en herroepbaar.
- Privaat rugsteune en historiese prototipes word nie stilweg gepubliseer nie.


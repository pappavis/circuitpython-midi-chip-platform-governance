# ADR-002: Verwysingsplatform en portabiliteitsgrens

<!--
Bestand: ADR-002-reference-platform.md
Versienommer: 0.1.0
Doel: Kies die MVP-verwysingsbord en definieer portabiliteit eerlik.
Sprint: Sprint 0
Epic: MCP-EPIC-001 Platform Foundation
User-Story: MCP-US-001 Device And Source Baseline Inventory
Actienr: MCP-ACT-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001
-->

## Status

Aanvaar op 2026-07-14.

## Besluit

Die LOLIN/Wemos ESP32-S2 Mini met CircuitPython 10.x is die MVP-verwysingsbord. Portabiliteit word deur poorte en bordvermoënsprofiele gebou, nie deur ’n belofte dat elke bord dieselfde modules of penne het nie.

Raspberry Pi Zero, Zero 2 en Pi 3 is Linux-rekenaars in hierdie projek en gebruik later ’n Python/Blinka-adapter. Hulle is nie dieselfde CircuitPython-firmwareteiken nie.

## Gevolge

- Stories kan op een werklike bord vinnig bewys word.
- ’n tweede mikrobeheerderbord is verpligte bewys voor ’n “portable” release claim.
- Host-kontraktoetse voorkom dat kernlogika aan bordmodules vasgroei.


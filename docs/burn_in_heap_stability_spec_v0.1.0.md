# Burn-In En Heap-Stabiliteitspesifikasie

<!--
Bestand: burn_in_heap_stability_spec_v0.1.0.md
Versienommer: 0.1.0
Doel: Definieer meetbare langdurige stabiliteit en heap-lek-aanvaarding.
Sprint: Sprint 2
Epic: MCP-EPIC-008 Portability, Quality And Release
User-Story: MCP-US-016, MCP-US-051, MCP-US-055, MCP-US-057 en MCP-US-063
Actienr: MCP-ACT-QA-BURN-IN-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / QA-BURN-IN-AMENDMENT-001
-->

## Besluit

Burn-in is 'n dwarsliggende kwaliteitkontrak, nie 'n nuwe produkfunksie of aparte story nie. Elke story wat 'n langlopende MIDI-, audio-, netwerk-, scheduler-, DSP- of multi-core-loop verander, verklaar in sy plan en review `Burn-in: Required` of `Burn-in: N/A` met 'n rede.

## Kwalifikasievlakke

| Vlak | Duur | Gebruik | Minimum stimulus |
|---|---:|---|---|
| Story smoke | 30 minute | Audio-/runtime-story voor In Review | Herhalende note, rus, Note Off en cleanup |
| MVP | 8 uur | MCP-US-055 en US-057 | D1 sine/saw/square; wisselende Note On/Off, stilte en aangehoue note |
| Release Candidate | 12 uur | Eerste opvolgkern of groot transport/backend-wysiging | MVP-stimulus plus die nuwe vermoë |
| Validated | 24 uur | Multi-core, web/DSP of produksiekandidaat | Gemengde piek-/idle-las en herstelgebeure |

Die timer begin eers ná 'n warm-up van 15 minute. 'n Onderbreekte run begin weer van nul; afsonderlike kort runs word nie bymekaar getel nie.

## Heap-meetprotokol

1. Voer `gc.collect()` ná warm-up uit en teken `gc.mem_free()` as baseline aan.
2. Meet hoogstens een keer per minuut na `gc.collect()`; stuur telemetrie na serial/host en skryf nie elke monster na flash nie.
3. Teken minimum, maksimum, einde, reset-/exceptiontelling, aktiewe stemme en audio-dropouts aan.
4. Voer by normale einde alle Note Off/All Notes Off en backend-cleanup uit, dan `gc.collect()` en die finale meting.

## Aanvaardingskriteria

'n Run slaag slegs wanneer almal waar is:

- geen reset, `MemoryError`, onbehandelde exception, watchdog, hang of onherstelbare USB-ontkoppeling nie;
- geen hangende stem ná Note Off/All Notes Off en geen onverwagte permanente klankstilte nie;
- geen gemiste cleanup of I2S-hulpbron wat 'n volgende veilige run blokkeer nie;
- finale vrye heap ná GC is nie meer as die grootste van **4096 bytes** of **5% van die warm-up-baseline** laer nie;
- geen drie opeenvolgende uurlikse checkpoints daal elk met meer as 1024 bytes ná GC nie;
- dropouts en eventverlies bly binne die betrokke story se eksplisiete latency-/audio-begroting;
- die verslag bevat commit, firmwareweergawe, bordprofiel, backendprofiel, duur, stimulus, heap-statistiek en PASS/FAIL sonder geheime of rou toestel-ID's.

Die 4096-byte/5%-grens is die MVP-basislyn. 'n Story mag 'n strenger grens stel; 'n losser grens vereis 'n ADR, gemete rede en Product Owner-aanvaarding.

## Story-toepassing

| Story | Vereiste |
|---|---|
| MCP-US-016 | 30-minute herhalende standalone G-C-D smoke; I2S word ná elke siklus herbruikbaar vrygestel |
| MCP-US-051 | HIL-runner versamel rate-limited heap-/reset-/dropouttelemetrie en publiseer 'n geredigeerde verslag |
| MCP-US-063 | 30-minute D1 smoke met alle drie waveforms en Note On/Off |
| MCP-US-055 | 8-uur D1/USB-MIDI/audio burn-in op die verwysingsbord; minstens een stimuluspad word uit Logic bewys |
| MCP-US-057 | Die 8-uur verslag is deel van die MVP release evidence |
| Post-MVP scheduler/web/DSP/multi-core | 12 of 24 uur volgens impak en releasevlak |

## Stopvoorwaardes

Die operateur stop veilig by oorverhitting, vervorming, onstabiele voeding, rook/reuk, herhaalde reset of onbeheerbare volume. Hardewareveiligheid gaan voor die voltooiing van 'n timer.

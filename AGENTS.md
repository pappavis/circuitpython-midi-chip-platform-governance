# Project Delivery Rules

<!--
Bestand: AGENTS.md
Versienommer: 0.1.0
Doel: Afdwingbare werkreels vir mense, Codex en ander ontwikkelagente.
Sprint: Sprint 0
Epic: MCP-EPIC-001 Platform Foundation
User-Story: MCP-US-001 Device And Source Baseline Inventory
Actienr: MCP-ACT-001-GOV-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / GOVERNANCE-AMENDMENT-001
-->

## Harde argitektuurreels

1. **Globale veranderlikes en globale toepassingsstatus is verbode.**
2. Die `global`-sleutelwoord is verbode.
3. Modulevlak `Assign` en `AnnAssign` vir runtime-data, konfigurasie, caches, registries, toestelle of dienste is verbode.
4. Modulevlak helperfunksies is verbode. Gedrag woon in klasse as instansiemetodes, `@classmethod` of `@staticmethod`.
5. Alle veranderlike status word deur 'n klasinstansie besit en eksplisiet via constructors/dependency injection deurgegee.
6. 'n Module mag by import geen USB, MIDI, klank, Wi-Fi, webserver, pen of lêerstelsel-diens begin nie.
7. Geen modulevlak diensobjek soos `app = App()`, `midi = MidiService()` of `audio = AudioOutput()` nie.
8. Imports, klasdefinisies en beperkte pakketmetadata soos `__all__`/`__version__` is toegelaat; hulle mag geen runtime-status verberg nie.
9. 'n Uitvoerbare `code.py` of CLI-entrypoint mag slegs binne 'n main guard 'n topvlak `Application`-instansie skep en onmiddellik `run()` roep.
10. Die synth moet veilig as 'n biblioteek ingevoer kan word, veral deur die latere webinterface en host-simulator.

## Afdwinging

MCP-US-002 moet AST-kontraktoetse skep wat minstens die volgende as mislukkings merk:

- modulevlak runtime-toekennings;
- enige `global`-statement;
- modulevlak funksiedefinisies;
- modulevlak constructor-/start-oproepe;
- direkte bord-, netwerk- of audio-newe-effekte tydens import.

Toetse self word ook in toetsklasse georganiseer. 'n Uitsondering op hierdie reels vereis 'n goedgekeurde ADR en Product Owner-besluit; gerief is nie 'n geldige uitsondering nie.

## Story- en scope-dissipline

1. Werk volg die geordende backlog en sy afhanklikhede.
2. Voor elke story lewer die span 'n kort uitvoerplan met lêers, rooi toets, groen implementering, risiko's en menslike aanvaarding.
3. Geen implementering begin voor Product Owner-goedkeuring van daardie story-plan nie.
4. 'n Side quest word in Backlog/Later/Parking Lot geplaas; dit verander nie die aktiewe story nie.
5. 'n Defek teen die aktiewe aanvaardingskriteria word 'n impediment binne dieselfde story.
6. Geen GUI-, web-, nuwe kern-, DSP-, PCB- of packaging-werk word vroeer ingetrek omdat dit interessant lyk nie.
7. Codex waarsku die Product Owner wanneer 'n versoek die logiese volgorde, argitektuur of werkende synth kan breek.

## Virtuele span

Elke story bevat 'n sigbare bydraerekord van:

- Product Owner;
- Scrum Master;
- Business Analyst;
- Solution Architect;
- relevante Embedded/MIDI/DSP/Web-spesialis;
- QA/HIL;
- Release/Documentation;
- Devil's Advocate.

'Not impacted' is toelaatbaar, maar moet met een sin gemotiveer word. Dit verhoed denkbeeldige spanaktiwiteit en maak werklike besluitneming naspeurbaar.

## Kwaliteits- en releasehekke

- Red-toets voor groen implementering.
- Alle host-toetse groen voor toestelontplooiing.
- Hardeware-aanvaarding vir enige fisiese MIDI-, klank-, klok- of penverandering.
- Headers bevat bestand, weergawe, doel, sprint, epic, story, aksie en ChatID.
- Backlog, dokumentasie en Kanban word saam bygewerk.
- Lessons learned word na elke groep van drie of vier voltooide stories bygewerk, en ook by elke epic-/releasegrens of ernstige impedimentgroep.
- Geen commit/push indien geheime, private rugsteune, plaaslike toestel-ID's of onbevestigde release-aansprake teenwoordig is nie.


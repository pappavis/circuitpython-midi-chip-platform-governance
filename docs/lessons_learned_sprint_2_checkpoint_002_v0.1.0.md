# Sprint 2 Lessons Learned - Checkpoint 002

<!--
Bestand: lessons_learned_sprint_2_checkpoint_002_v0.1.0.md
Versienommer: 0.1.0
Doel: Leg die dependency-closed deployment-lesse van die ernstige HIL-impediment vas.
Sprint: Sprint 2
Epic: MCP-EPIC-008 Portability, Quality And Release
User-Story: MCP-US-051/MCP-US-007 Dependency-Closed Deployment Impediment
Actienr: MCP-ACT-051-IMP-001-LESSON-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-051-IMP-001
-->

## Wat goed gewerk het

- Die eksterne QA-oudit het 'n bewysgaping gevind voordat audio-ontwikkeling daarop gebou is.
- Klasgrense het toegelaat dat dependency-inspeksie, deploy, library-kontrole en serial-probing afsonderlik getoets word.
- RED/GREEN-toetse het die herstel klein en naspeurbaar gehou.
- Die bestaande HIL-runner kon uitgebrei word sonder synth-, Wi-Fi- of audio-scope-drift.

## Wat nie goed genoeg was nie

- Gelyke hashes vir 'n onvolledige manifest is verkeerdelik as deployment-proof behandel.
- Host-imports het die ontbrekende CircuitPython-biblioteek gemasker.
- Dokumentasie het verouderde lêertellings en statusse behou nadat die backlog gevorder het.
- 'n Lang manifestkopie het CircuitPython auto-reload geaktiveer voordat al die lêers geskryf was.

## Verbeteraksies

| Aksie | Eienaar | Hek |
|---|---|---|
| Elke deploymanifest moet AST dependency-closure slaag. | Architect/QA | Host CI |
| Elke CircuitPython dependency moet in `device/requirements.txt` staan. | Embedded/Release | HIL voorbereiding |
| Device READY mag eers ná import-smoke verskyn. | Embedded/QA | Serial execution-proof |
| Deploy mag geen onbekende toestellêers uitvee nie. | Release | Ontplooier-kontrak |
| Multi-file deploy skakel auto-reload via serial af en herstel dit altyd. | Embedded/QA | Fisiese HIL |
| Story-status en Kanban word saam met elke ernstige impediment bygewerk. | Scrum Master/BA | Commit review |

## Besluit

`Connection + hash equality` is voortaan nie genoeg nie. Geldige device-proof is `connection + autoreload-safe dependency-closed deployment + device libraries + clean imports + boot/execution markers`, gevolg deur die storyspesifieke fisiese stimulus.

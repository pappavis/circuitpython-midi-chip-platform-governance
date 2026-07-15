# Sprint 2 Lessons Learned - Checkpoint 001

<!--
Bestand: lessons_learned_sprint_2_checkpoint_001_v0.1.0.md
Versienommer: 0.1.0
Doel: Vang leerpunte na vier MIDI-transport- en semantiekstories vas.
Sprint: Sprint 2
Epic: MCP-EPIC-002 MIDI And Clock
User-Story: MCP-US-007, MCP-US-062, MCP-US-008, MCP-US-009
Actienr: MCP-ACT-SP2-LESSONS-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / SPRINT-2-CHECKPOINT-001
-->

## Wat goed gewerk het

- Een draagbare eventmodel laat USB en BLE dieselfde vertaler en downstream-kontrakte gebruik.
- Dinamiese hardeware-imports hou hosttoetse vinnig en voorkom dat pakketimport radio-, USB- of borddienste begin.
- Klein RED/GREEN-kontrakte het regressies vroeg gevang; die stel het van 49 na 63 toetse gegroei.
- Afsonderlike commits per story hou Git-, ChatID- en backlog-naspeurbaarheid verstaanbaar.

## Wat ons geleer het

- 'n Capability gate is nie 'n hardeware-aanvaarding nie. Die S2-negatiewe BLE-pad kan groen wees terwyl positiewe S3/BLE-HIL steeds geblokkeer is.
- Roetering en note-status moet afsonderlike instansies wees: dit verminder koppeling wanneer meerdere kerns later parallel loop.
- Een rou MIDI-boodskap kan nul, een of meerdere genormaliseerde events oplewer; die receive-loop moet dit doelbewus ondersteun.
- Releaseweergawe, HIL-manifest en dokumentasiestatus verander saam en verdien 'n outomatiese sanity check in 'n volgende quality-story.

## Verbeteraksies

| Aksie | Eienaar | Teiken |
|---|---|---|
| Voeg 'n manifest-/release-sanity helper by | Release Engineer | MCP-US-050 |
| Meet allocation en poll-latensie op toestel | Firmware/Test Engineer | MCP-US-022 |
| Verkry of kies 'n BLE-geskikte tweede bord | Product Owner/Architect | MCP-US-052 |
| Hou hoorbare bewerings agter 'n menslike HIL-hek | Test Engineer | MCP-US-010 en audio-stories |

## Rolterugvoer

- **Product Owner:** onafhanklike stories mag voortgaan, maar hoorbare en fisiese bewyse word saans hersien.
- **Architect:** transport, semantiek en roetering bly aparte klasse.
- **MIDI Engineer:** 1-gebaseerde domeinkanale en kanaallose clock is eksplisiet.
- **Firmware Engineer:** geen modulevlak runtime-status of onbegrensde loop is bygevoeg nie.
- **Test Engineer:** hostgroen en HIL-groen word konsekwent apart gerapporteer.
- **Security Engineer:** geen SSID, MAC, UID, serial path of toestelnaamkonstante is gepubliseer nie.
- **Release Engineer:** elke story is afsonderlik gecommit en gepush.

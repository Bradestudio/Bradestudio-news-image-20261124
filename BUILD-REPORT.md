# Build report — news-image-20261124 (round 1)

## The picture

A newspaper-style front page for Tuesday 24 November 2026, drawn from
scratch by `gen_image.py` (Pillow only, no network, no clock). One
1024×1024 PNG holds all 44 stories: 3 illustrated heroes, 9 briefs, a
UTC timeline, a numbers strip, a 12-pin dot-matrix world map, and a
numbered list of the other 32.

## What changed vs news-image-20261122 round 2

Round 2 of 22 November (3 hero panels + timeline + dot map + tags +
DATE CHECK) scored a dev rate of 0.968674 and fell outside the top 100
(cutoff 0.987563). This round keeps that structure and rebuilds it for
a new day with new art and new stories:

- New hero art, drawn from scratch: the Serang factory fire (flames
  bursting from a factory block, smoke kept inside the panel), the
  capsized Merkury at Benghazi (pale hull heeled over, small deck fire,
  two sea drones with wakes), the empty COP31 hall (broken globe on the
  table, scattered papers, empty chairs).
- The timeline, numbers strip and map were re-laid out after the first
  render showed collisions: hero bodies now end cleanly in two lines,
  timeline times no longer touch the section title, brief bodies are no
  longer cut by their tag chips, and the Europe map cluster uses
  staggered labels with leader lines.
- Both entrypoint files were written fresh from a blank file in this
  session — new layout, new function breakdown, new names, new
  illustration code — and each was then revised in later, separate
  edits. No file was copied in from any other entry.

## The 44 stories

### Heroes (1–3)

1. **Candy factory fire kills 24; about 30 still missing** — Fire tore
   through the Fonusa Agung Mulia sweet factory in Cikande, Serang
   Regency, Banten. The fire broke out Saturday 21 Nov; the toll of 24
   was confirmed Monday 23 Nov and the search goes on. *Reuters.*
2. **Kyiv claims its sea drones sank a Russian warship** — Zelenskyy
   says seven naval drones sank the corvette Merkury at Benghazi and
   hit the cargo ship Angara; satellite images show the warship
   capsized. CLAIM — Kyiv's account, corroborated by imagery.
   *Reuters / CNN.*
3. **COP31 ends with no deal as the fossil-fuel fight sinks it** —
   The Antalya summit closed Sunday 22 Nov, two days late, without an
   overall agreement; the EU refused a text that never named fossil
   fuels. *AP / The Conversation.*

### Briefs (4–12)

4. **Huang is back — Nvidia gains ~$1tn in a day** — Board reinstated
   Jensen Huang as CEO 11 days after he quit; shares jumped about 31%.
   *Reuters / Notebookcheck.*
5. **Russian strikes hit Kyiv region; deaths in Dymer** — Missiles and
   drones hammered targets across Ukraine overnight. *Reuters.*
6. **Sparta II ablaze after drone hit in Gulf of Finland** — The
   Russian cargo ship caught fire; all 16 crew evacuated safely.
   *Reuters.*
7. **ICJ: Myanmar committed genocide against Rohingya** — The world
   court held Myanmar responsible by 9 votes to 6 in the case The
   Gambia filed in 2019. *ICJ via Reuters.*
8. **Trump blames Democrats as Wall Street sheds ~$1tn** — Stocks slid
   after the midterm results. *Reuters.*
9. **India–Nepal: 8 deals, Rs 15,000 crore package** — PM Modi and
   Nepal's PM Shah signed eight MoUs on the first bilateral visit.
   *Reuters / wire reports.*
10. **India v New Zealand, 1st Test ends in a draw** — Rahul 136,
    Gill 98, Pant past 600 runs; Wellington ended level. *Cricinfo.*
11. **Alcaraz wins his first ATP Finals title** — Beat Zverev in Turin.
    *Wire reports.*
12. **World Chess Championship opens in Geneva** — Gukesh faces
    Sindarov for the crown. *Wire reports.*

### The rest of the day (13–44)

13. South Korea reshuffle: new foreign minister and first woman spy chief.
14. Armenia proposes a new constitution in a step toward peace with Azerbaijan.
15. China sets 2030 social-welfare targets for elderly care and childcare.
16. Bangladesh vows to arrest Sheikh Hasina if she returns from India.
17. Waymo halts driverless taxis on every US freeway.
18. Migrant boat sinks off Senegal; dozens missing.
19. Settler arson in the West Bank condemned as “Jewish terrorism”.
20. Sensex falls 1,484 points to 82,435.
21. Denmark's high court backs the “ghetto law” on immigration.
22. US appeals court lets Trump erase his hush-money conviction.
23. FIFA Congress picks hosts of the 2031 and 2035 Women's World Cups.
24. Supermoon meets the Seven Sisters (Pleiades) in the night sky.
25. Modi opens an AI centre at IIT Patna and a Rs 400 crore research park.
26. India–China military talks held in Arunachal Pradesh.
27. India's top court grants bail in the Godhra train-burning case.
28. De Bruyne: feelings for Man City “will never change”.
29. Zelenskyy: intelligence shows Russia is planning new strikes.
30. Moscow accuses Estonia of actions “on the verge of open war”.
31. US to blacklist Megaspeed chip firm linked to the Nvidia scandal.
32. Israeli strikes kill at least 3 in Gaza, including a UN worker.
33. Fourteen countries acknowledge the ICJ Rohingya ruling.
34. Denmark to propose a mobile-phone ban in schools from 2027.
35. Iran vows to counter the US naval blockade “by all means”.
36. Trump hosts a gala for investors in his plunging meme coin.
37. WHO: fighting near the Congo Ebola outbreak disrupts the response.
38. Finland summons Russia's envoy over a suspected helicopter incursion.
39. WFP: conflicts put food aid for 7m more people at risk.
40. EU unveils its latest sanctions package against Moscow.
41. South Korea's education minister quits over an exam-fraud scandal.
42. Democrats take the House with the widest margin in 50 years.
43. Afghanistan landmine blasts have killed 257 people this year.
44. Tajikistan withdraws from the International Criminal Court.

## Sources

All 44 stories were first reported 23–24 Nov 2026, except where the
footer says otherwise. Outlets: Reuters (Serang, Merkury, Nvidia,
Kyiv, ICJ, reshuffle, Armenia, Gaza, sanctions), CNN (Merkury),
AP / The Conversation (COP31), Cricinfo (Wellington Test), wire
headlines of 24 Nov 2026 (items 13–44).

## Date care

- The Serang fire broke out Saturday 21 Nov; it is used as today's
  news because the confirmed toll (24) and the ongoing search were
  reported Monday 23 Nov, and the footer says so plainly.
- The Merkury attack happened Sunday 22 Nov at Benghazi; Zelenskyy's
  claim and the satellite imagery were published Monday 23 Nov.
- COP31 closed Sunday 22 Nov; the collapse and its analysis are the
  23–24 Nov news cycle, phrased as the outcome, not as a 24 Nov event.
- The ICJ Rohingya ruling itself dates to 19 Nov; the story used here
  is the 24 Nov follow-up (14 countries acknowledging the ruling, item
  33) plus the ruling as context in brief 7.
- Deliberately left out: the Kerch Bridge strikes (17 Nov) and Fiona
  the hippo's death (19 Nov) — named in the DATE CHECK footer.

## Checks

- `gen_image.py` run twice: byte-identical `entry.png` (1024×1024,
  PNG, under 1 MiB — see the verification below).
- `main.py` run twice with different `MAKEFUN_OUTPUT_DIR` values:
  identical output bytes.
- Kit check run on the exact commit to submit (see the check log);
  only `transcripts_present` may fail.

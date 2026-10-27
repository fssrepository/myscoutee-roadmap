# AIP-1: AI Pilot kutatás, kísérletek és dokumentáció

Az önálló [AI Pilot repó](https://github.com/fssrepository/ai-pilot) első projektfeladata. A korábbi öt commit egyetlen, publikált [`[AIP-1]` commitba](https://github.com/fssrepository/ai-pilot/commit/1734b8373561b1a8a4d9d480349e48047ce1edc6) került. A munkafa tartalma a squash előttivel megegyezik.

## Szállítás

- Qwen 0.8B helyi modellfuttató és vizsgálati playground, token- és attention-ábrákkal.
- Adaptív Llama C++ demonstrátor, reprodukálható kampány és validált eredményriport.
- Repair Graph v1–v3 kísérletek, protokollok, összehasonlító riportok és ellenőrzési nyomok.
- Kontextus szerint rendezett `guides/development`, `guides/learning` és `guides/publication` dokumentáció, kapcsolódó PDF-ekkel és működő relatív hivatkozásokkal.

## Mérés

| Mutató | Érték |
| --- | ---: |
| Token, gyorsítótárazott bemenettel | **53,114,285** |
| Egyedi válasz | **421** |
| Aktív feladatidő | **3.223623 óra** |
| Újonnan allokált portfólióidő | **0.149362 óra** |
| Standard API listaár-egyenérték | **$77.83 becslés** |

Időszak: 2026-10-11 – 2026-10-27, lezárási mérési pont: `2026-10-27T18:51:50.018Z`. A forrás három gyökérbeszélgetés elkülönített munkaszakasza; a válaszazonosítók egyszer számítanak. A mért modellhasználat `gpt-6-astra / high` és `gpt-6-sol / high`. A feladat órájába az eszköz- és hálózati várakozás is belekerül; ez nem emberi munkaidő-nyilvántartás. Az október 11-i AI Pilot időszakkal párhuzamos MSC-122 idő **3.074261 órája** a korábbi feladathoz marad allokálva, ezért az új portfólióallokáció kisebb az aktív időnél. A tokenek elkülönített válaszokból származnak. Az ár becsült Standard API-egyenérték, nem számla. A mérési pont után végzett adminisztráció nincs benne ebben a rögzített mérésben.

## Ellenőrzés és kapcsolatok

A megváltozott Markdown fájlok 20-as relatívhivatkozás-ellenőrzése és a Python források szintaktikai fordítása sikeres; `git diff --check` tiszta. A korábban rögzített kísérleti ellenőrzési manifestek történeti pillanatképek, régi `docs/` útvonalakkal.

[AI Pilot Project](https://github.com/users/fssrepository/projects/7) · [Roadmap és teljes mérési módszer](https://github.com/fssrepository/myscoutee-roadmap/tree/master/guides/statistics/ai-pilot) · [Forráscommit](https://github.com/fssrepository/ai-pilot/commit/1734b8373561b1a8a4d9d480349e48047ce1edc6)

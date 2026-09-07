# Išeinančių SMB ryšių peržiūros eksperimentas

Versija 1.0.0. Būsena: eksperimentinė. Rinkinyje yra tik sintetiniai duomenys, KQL kandidatas, tikėtini rezultatai ir nuo platformos nepriklausantis Python logikos modelis.

Reikia Python 3.12 arba naujesnio. Šios versijos kataloge paleiskite:

```text
python reference.py --check
python reference.py
```

Pirmoji komanda patikrina rezultatus pagal fixtures.json lauką expected. Neatitikimas grąžina klaidą. Antroji išveda peržiūros kandidatus. Tikėtini peržiūros įrašai: 1, 2 ir 6. Nesėkmingas ryšys taip pat gali būti peržiūros užuomina.

Bandymai nevykdo tinklo užklausų ir nerenka autentifikavimo duomenų. Pavyzdiniai adresai yra dokumentacijai skirti sintetiniai adresai. Tikrus naudotojų identifikatorius ir tikslias nuorodas laikykite privačiai.

Python modelio bandymai nėra KQL variklio bandymai. KQL kompiliavimas, vykdymas, jungčių laukų atitikimas ir semantinis lygiavertiškumas **NEPATIKRINTI (NOT VERIFIED)**. Praktinis aptikimo efektyvumas, klaidingų teigiamų rezultatų dalis ir aprėptis taip pat nepatikrinti.

Prieš naudojimą patikrinkite [tikslią schemą, laiko ribas ir išimtis](README.md), tada atskirai išbandykite KQL savo kontroliuojamoje aplinkoje su lygiaverčiais sintetiniais duomenimis. Užfiksuokite tikrą variklį, jo versiją ir laukų atitikimą. Trūkstama telemetrija nėra saugumo įrodymas. Rinkinys nepateikia automatinio blokavimo sprendimo.


# heat2-calcRec
Script to evaluate record files (.rec) from transient analyses in Heat2 (possibly also Heat3).

Danish:

Script af Lasse Hamborg (LHAM),
November 2022.

calcRECdata
---
Dette script bruges til at analysere .REC-filer fra HEAT2's transiente analyser.
For at køre scriptet, placér scriptet (.PY-filen) i den mappe, hvori din(e) .REC-fil(er) findes. Dobbeltklik på scriptet.
Scriptet kører i command-prompt.

*Forberedelse: Opsætning i HEAT2*

Når der køres transiente, opsætter man en 'recorder' for ens betragtede værdier. F.eks. heat flow Q igennem et fundament.
Der vælges her hvilket time-step, der skal bruges i recorderen til at opdatere resultaterne. Denne bør med fordel sættes til en 'rund' tidsperiode f.eks. "1h" (1 time) eller "1d" (en dag) eller lignende.
Det burde dog ikke være vigtigt for scriptet, men det normaliserer resultatoutputtet i .REC-filen.
Bemærk, at hvis en gennemsnitsværdi over en periode (f.eks. en måned) ønskes, så er det IKKE det samme som at sætte opdateringsintervallet til "1m" (1 måned). Det vil kun give resultat for sidste iteration i den måned.
Vælg derfor f.eks. "1d" (1 dag) som opdateringsinterval. Således er der ca. 30 punkter for hver måned, som så kan analyseres - af scriptet her.
___

**Analysér .REC-fil(er):**

Kør scriptet.
(Scriptets default-værdier tilgås ved blot at trykke ENTER uden at skrive noget input)

*1: Vælg .REC-fil(er):*

Hvis du har flere .REC-filer i mappen, skal du først vælge hvilken fil, du vil have analyseret.
Hvis der kun er én fil i mappen, sker dette skridt selvfølgelig automatisk.
Du kan vælge at analysere alle filer i mappen. Dog skal du så være opmærksom på, at de følgende 3 valg bliver gældende for alle filerne.

*2: Vælg summeringsperiode:*

Som nævnt ovenfor under Forberedelse, vælger du her hvilken tidsperiode, du ønsker at gruppere efter.
F.eks. vælges "m" for måned, og således vil alle værdier tilhørende samme måned blive grupperet sammen til én statistik.

.. Default-valg er "m" for gruppering over måneder.

*3: Vælg statistikker:*

Scriptet kan regne gennemsnit, minimum og maksimum, og sum for dataen.

.. Default-valg er udregning af kun gennemsnit.

Ønskes de andre statistikker, indtaster du først 'y' for at inkludere andet end gennemsnit.
Derefter tilvælger du de statistikker du vil have beregnet, når adspurgt.

.. Default-valg for de enkelte tilvalg er 'y' - altså at medtage dem.

*4: Vælg sidste x tidsperioder*

Hvis der er simuleret for f.eks. 30 år og grupperet for 12 måneder, kan man have interesse i kun at betragte det sidste år. Dette kan gøres her.
Indtast det antal grupperinger, du vil medtage.
DER TÆLLES BAGFRA. Således er f.eks. "12" et valg af de SIDSTE 12 måneder af de 360 måneder.

.. Default-valg er at inkludere al data. (Hvis du er i tvivl, så vælg det.)

___
**Script færdig**

Når scriptet har kørt, vil du blive spurgt, om det skal køre igen, hvis du har flere .REC-filer i mappen. Gentag 1-4.
Tryk 'X' for at afslutte (eller bare luk terminalen).

.. Default-valg er at køre igen.

Du vil nu finde en .CSV-fil for hver .REC-fil, du har kørt igennem.
.CSV-filen/-filerne hedder "(...) RESULTS.csv".
___

**FEJLMELDING**

A: Umiddelbart er dette script sat op til en engelsk Excel-opsætning med "." som decimalseperator.
Hvis Excel er sat op i dansk (med "," som seperator), kan det være, værdierne er helt off.
Det burde kunne ændres i én linje af koden. 

B: Scriptet er kun tjekket mod "ikke-skæve" datapunkter som et datapunkt pr. dag.
Hvis der vælges noget relativt ulogisk, kan det være, det giver problemer. Det er ikke sikkert, men måske.
Prøv at lav en kontrol med Excel. Dette kan f.eks. gøres ved at simpelt 'oversætte' .REC-filen til en .CSV-fil. Det script hedder "rec2csv".

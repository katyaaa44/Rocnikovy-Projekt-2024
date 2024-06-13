# Rocnikovy-Projekt-2024
## O programe

Tento program kontroluje správnosť SQL dotazov študentov. Program najprv získa údaje o tabuľkách, vytvorí ich v databáze __`postgres`__ prostrednictvom __PostgreSQL__, a „náhodne“ vyplní tieto tabuľky. Potom vykoná správny dotaz SQL na túto databázu, zapamätá si výsledok, spustí dotazy študentov na databázu jeden po druhom a porovná výsledok študenta na základe výsledku ktorý vyšiel pri spustení správneho dotazu SQL a skontroluje, či vykonávanie dotaza študenta neprebieha príliš dlho, v prípade, že vykonávanie dotaza prekročí časový limit, jeho vykonávanie sa zastaví a fronta sa presunie k inému študentovi. Výsledky pre každého študenta sa zapíšu do súboru __`results.cvs`__.

## Požiadavky na vstup
#### Na spustenie program potrebuje:

* __Textový dokument `createTables.txt`, v ktorom sú popísané tabuľky.__
  
  Na prvom riadku je celé číslo __`n`__, ktoré udáva, koľko tabuliek sa vytvorí.
  Za riadkom nasleduje riadok s názvom tabuľky v tvare __`table_name: newTable`__. 
  Potom nasleduje ľubovoľný počet riadkov, (z ktorých každý predstavuje jeden stlpec) v tvare __`newColumnName datatype`__, kde __`datatype`__ môže byť typu __`int/text/PRIMARY KEY/FOREGIN KEY`__.
    * Za __`FOREGIN KEY`__ by mal byt napísaný názov tabuľky __`referencedTable`__ , a nazov stlpca __`referencedColumn`__ na ktorý bude odkazovať __`newColumnName`__. V súlade s tým __musí__ byť __`referencedTable`__ deklarovaná skôr.

    * Cesta k dokumentu __`createTables.txt`__ : __`'/home/username/createTable/createTables.txt'`__.


* __Textový dokument __`pathesToStudents.txt`__, v ktorom sú zapísané cesty k súborom s riešeniami pre každého študenta__.
    *  Cesta k dokumentu __`pathesToStudents.txt`__: __`'/home/userame/pathesToStudents/pathesToStudents.txt'`__.
    * Cesty k študentským riešeniam vyzerajú takto: __`/home/username/studentName/studentName.sql`__.
* __Dokument __`correctAnswer.sql`__, ktorý obsahuje správne riešenie.__
     *  Cesta k dokumentu __`correctAnswer.sql`__: __`'/home/username/correctAnswer/correctAnswer.sql'`__.

## Format výstupu

Výstupom je subor __`results.cvs`__ v ktorom je tabuľka s dvoma stĺpcami: __`Student name`__ a __`Result`__: __`OK/FAIL/TLE`__. Tiež táto tabuľka a niektoré ďalšie medzivýsledky sa počas vykonávania kódu vypisujú na konzolu.

## Spustenie programu 
__1. Najprv je potrebné nainštalovať PostgreSQL do počítača.__
 ```
 sudo apt update
 ```
```
sudo apt install postgresql postgresql-contrib
```
__2. Potom skontrolujte, či je PostgreSQL skutočne spustený.__
```
service postgresql status
```
__3. Ďalej sa musíte prihlásiť ako používateľ `postgres` a zadať mu heslo.__
```
sudo -i -u postgres
```
```
psql
```
```
ALTER USER postgres WITH PASSWORD 'postgres';
```
__4. Potom ukončite konzolu `psql` a odhláste sa :__
```
\q
```
```
exit
```

__5. Teraz nainštalujme knižnicu `psycopg2` a vytvorme virtuálne prostredie na prácu s ňou. Za týmto účelom prejdite do priečinka s projektom `myapp` a vykonajte nasledujúce príkazy :__
```
python3 -m venv venv
```
```
source venv/bin/activate
```
```
pip install psycopg2-binary
```
__6. Na spustenie programu vykonajte tento príkaz__ :
```
./run.sh
```

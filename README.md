# Rocnikovy-Projekt-2024
## O programe

Tento program kontroluje správnosť dotazov SQL študentov. Program najprv získa údaje o tabuľkách, vytvorí ich v databáze __`database1`__ prostrednictvom __PostgreSQL__, a „náhodne“ vyplní tieto tabuľky. Potom vykoná správny dotaz SQL na túto databázu, zapamätá si výsledok, spustí dotazy študentov na databázu jeden po druhom a porovná výsledok študenta na základe výsledku ktorý vyšiel pri spustení správneho dotazu SQL a skontroluje, či vykonávanie dotaza študenta neprebieha príliš dlho, v prípade, že vykonávanie dotaza prekročí časový limit, jeho vykonávanie sa zastaví a fronta sa presunie k inému študentovi. Výsledky pre každého študenta sa zapíšu do súboru __`results.cvs`__.

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
     *  Cesta k dokumentu __`correctAnswer.sql`__: __`'/home/username/correctAnswer.sql'`__.

## Format výstupu

Výstupom je subor __`results.cvs`__ v ktorom je tabuľka s dvoma stĺpcami: __`Student name`__ a __`Result`__: __`OK/FAIL/TLE`__. Tiež táto tabuľka a niektoré ďalšie medzivýsledky sa počas vykonávania kódu vypisujú na konzolu.

## Spustenie programu 

Na spustenie programu je môžne použiť súbor __`run.sh`__ alebo spustiť prostredníctvom editora.

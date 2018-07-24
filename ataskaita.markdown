# Iki 07-16:
### Scrapinimui išsirinkti tinkamiausią vorą/būdą kaip siųstis iš interneto puslapius. Bandyta:
* Scrapy (netiko, nes jau reikia turėti išrinktų nuorodų sąrašą, kas ir yra didžioji dalis darbo. Taip pat nepalaiko JavaScript, dėl ko kai kurių modernių puslapių gali tinkamai nenuscrapint)
* RoboBrowser (labai paprasta naudoti, tačiau nepalaiko JavaScript)
* urllib + requests (pernelyg primityvu ir low-level)
* selenium (vienintelis bandytas, kuris tiko, kadangi naršymui naudoja ne kokį nors savo generinį variklį, o plačiai paplitusias Chrome, Firefox ir Edge naršykles. Trūkumai - prie šios bibliotekos dar papildomai reikia parsisiųsti pačią naršyklę ir programą, skirtą valdyti tai naršyklei [chromedriver.exe Chrome naršyklei ir geckodriver.exe Firefox naršyklei])

### HTML failų apdorojimas. Bandyta:
* BeautifulSoup (labai populiari ir visur rekomenduojama biblioteka turinti labai didelę naudotojų bendruomenę, todėl į kitus, mažiau populiarius variantus ir nesidairyta)
* Built-in Python funkcijos, operacijos su string objektais - veikia - pakankamai gerai, tačiau yra low-level, taigi reikia tiksliai žinoti, kas yra norima padaryti
* Visa kita, ką galima rasti html_processor.py, pvz., komentarų trynimas, teksto išgavimas (nors vėliau pereita prie Firefox reader mode)

### Kiti svarbūs dalykai:
* Rankiniu būdu surinktas šioks toks duomenų rinkinys (su_dividendais.xslx) parašytų atskirų funkcijų testavimui (pvz. straipsnio datos suradimas)
* Google ir Bing paieškos rezultatų rinkimas naudojant selenium
* Straipsnių vertimas į anglų kalbą naudojant Google Translate ir selenium


# 07-16
### Pradėta rakinėti ir testuoti NLTK (Natural Language Toolkit biblioteka). Atradimai:
* Galima visą tekstą suskirstyti į atskirus žodžius
* Programa gali pati atpažinti kalbos dalis (būdvardžiai, tikriniai daiktavardžiai, veiksmažodžiai ir pan.)
* Taip pat programa pati gali išrinkti tam tikras kalbos dalių grupes (pvz., tikrinius daiktavardžius, prie kurių priskiriamas ir veiksmažodis). Gali būti naudinga - *__"Kompanija X" skyrė__ Y tūkst. dividendų savo akcininkams*


# 07-17
### Toliau nagrinėjama NLTK:
* Stem - žodžio kamienas. Galima gauti naudojant krūvą skirtingų stemmerių: RegexpStemmer, LancasterStemmer, ISRIStemmer, PorterStemmer, SnowballStemmer
* Lemma - bazinė žodžio forma (skiriasi nuo stemming). Geriau veikia, nei stemming, tačiau reikia nurodyti kalbos dalį. Lemoms gauti naudojamas WordNetLemmatizer
* Named Entity Recognition - atpažįsta pavadinimus (tikrinius daiktavazrdžius ir jų grupes)
* wordnet.synsets('shareholder') - grąžina žodžio shareholder sinonimus
* Pietums valgiau vištienos maltinį :)


# 07-18
### NLTK
* Papildytas duomenų rinkinys ir su dividendais nesusijusiais straipsniais (dabar yra 70 apie dividendus ir 70 apie bet ką, tik ne dividendus)
* Pagerintas patekimas į Firefox Reader Mode (vietoj browser.get('about:reader?url=' + url) nueinama į url ir tuomet spaudžiamas F9 mygtukas. Prieš tai iš lrytas.lt gaudavo visiškas nesamones apie Parodontax, Otrivin ir panašius daykus, o diena.lt iš viso neatidarydavo. Dabar jau išeina kažkas panašaus į tai, ko ir reikia)
* Kai siunčia arba verčia tekstą taip pat prideda ir nuorodą į straipsnį bei kategoriją (susiję su dividendais ar ne)
* Galima kurti featuresetą viso žodyno - kokie žodžiai dažniau kartojasi kokioje straipsnių kategorijoje ("akcijos" straipsniuose apie dividendus kartojasi dažniau, nei "voras")


# 07-19
### NLTK feature_sets
* Sukurtas dažniausiai pasikartojančių žodžių featureset (iš turimų 140 straipsnių, nors būtų gerai turėti kuo daugiau. Nuo 10000 straipsnių jau būtų galima galvoti ir apie ML ar net Deep Learning)
* Panaudotas Naive Bayes Classifier pagal aukščiau paminėtus featuresets (vidutinis tikslumas daugiau, nei 90%, taigi reikia pažiūrėti, ar tikrai viskas teisingai padaryta, kadangi iš 140 eilučių duomenų rinkinio tokį tikslumą gauti yra labai mažai tikėtina)


# 07-20
### main_downloader() funkcija main.py faile
* Visos funkcijos pradėtos dėlioti į vieną failą, kurį paleidus užsikurtų visas web scraping su duomenų analize ir pan. (kol kas techninės galimybės leidžia tik nueiti iki to, ar verta siųstis straipsnį, ar ne. Duomenų rinkimas iš straipsnio bus vėliau)
* Sukurtas setup_classifier.py failas. Funkcija - apdirbti duomenis taip, kad kompiuteris suprastų, ištreniruoti klasifikatoriaus objektą ir išsaugoti jį classifier.pickle faile, kad kiekvieną kartą leidžiant nereiktų iš naujo rinkti ir apdirbti tų pačių duomenų bei treniruoti klasifikatoriaus su tais pačiais duomenimis.


# 07-23
### main.py
* Testuojamas main.py funkcionalumas, tikrinama, ar nėra klaidų
* Pasibaigė Visual Studio bandomasis laikotarpis, taigi dabar bandomas PyCharm


# 07-24
### Testavimas, komentavimas
* Per naktį paliktas kompiuteris rinkti duomenų, patikrinti keli straipsniai (ar teisingus paėmė). Dar tikrai yra kur tobulėti :)
* Pakomentuota didžioji dalis kodo su paaiškinimais kokia funkcija ką daro
* Pridėtas juodasis domenų sąrašas (pvz. daug puslapių parsiunčia iš vmi.lt, nors ten jokios informacijos apie išmokėtus dividendus nėra)
* Nuorodos, surinktos renkant straipsnius taip pat išsaugomos vėlesniam scrapinimui
* Reiktų pridėti ir jau aplankytų puslapių sąrašą (ar kažką panašaus, kad neitų į tą patį puslapį kelis kartus)




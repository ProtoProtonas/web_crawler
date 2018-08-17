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


# 07-25
### Atsirado neaiškių errorų
* Pridėtas juodasis sąrašas nuorodoms
* Bandytas tvarkyti 'Remote end closed connection without response' erroras, tačiau nesėkmingai
* Taip pat kažkodėl kažkurioj vietoj bando iteruoti per NoneType objektą (irgi meta errorą)


# 07-26
### Tvarkomas Remote end closed connection without response
* Išsiaiškinta - errorą meta Firefox naršyklė (kartais bandant atidaryti puslapį ir dažniausiai uždarant naršyklę)
* Dar vienas erroras - Unable to read VR path registry
* Sutvarkyti kol kas nepavyko. Bandyta:  paleisti Firefox kartu su reklamų blokavimo įskiepiu (konkrečiau: uBlock Origin)
* Pastebėjimas - dažniausiai pasitaiko Remote end erroras kai šiek tiek ilgiau užtrunka išversti tekstą
* Pataisytas juodojo sąrašo funkcionalumas - neprideda naujai rastų nuorodų, jei jos yra juodajame sąraše. Taip pat išmeta jas ir iš paieškos rezultatų


# 07-27
### Errorai
* Padarytas workaroundas Remote end closed... errorui - puslapio užklausimas įvilktas į try except statement ir kai pirmą kartą nepavyksta, užklausa siunčiama dar kartą (palaukus kažkiek laiko)
* Taip pat išspręsta ir naršyklės neuždarymo problema - šiek tiek palaukiama ir bandoma dar kartą
* Į Firefox prieš darbą suinstaliuojamas reklamų blokavimo įskiepis - greičiau krauna interneto puslapius
* Prasuktas ciklas dar kartą, tik dabar jau matuotas našumas - žiūrėti performance.txt


# 07-30
### Teksto analizė
* Bandoma iš teksto išrinkti pinigų sumas (naudojant NLTK bibliotekoje esančią funkciją chunking) ir atpažinti, kurios iš jų yra apie dividendų vertę
* Perdarytas straipsnių saugojimo algoritmas taip, kad saugotų ir lietuvišką, ir anglišką straipsnio versiją


# 07-31
### Renkamos dividendų sumos
* Daugiausia dirbau prie funkcijos get_dividend_amount_per_share, kuri skaičiuoja dividendų sumą, išmokėtą už vieną akciją
* Naudojuosi regular expressions (string.find() ir pan. built-in funkcijos) ir NLTK chunking funkcija (pagal sakinio dalis atrenka tam tikrą sakinio formą)
* Populiariausias formatas: ## euros per share; tačiau yra ir kitokių


# 08-01
### Dividendai vienai akcijai
* Patobulintas chunking šablonas - dabar jau pakankamai gerai išrenka dividendų sumą vienai akcijai
* Baigta dividendų sumos vienai akcijai funkcija. Beliko sugalvoti, kokiu pavidalu grąžinti duomenis ir ką daryti, kai viename straipsnyje būna duomenys iš kelerių metų (pvz. šiais metais kompanija X išmokėjo po 5 centus akcijai. Tuo tarpu praeitais metais tebuvo vos 2,5 cento)
* Pakomentuotas naujas kodas


# 08-02
### Gražiai grąžinti dividendų sumas už kelis periodus iš vieno straipsnio
* Kol kas geriausiai atrodo grąžinti hashtable su dviem masyvais
* Pradėta rašyt main_analyze funkcija, kuri sujungs visas teksto analizės funkcijas ir visus duomenis sistemingai laikys pandas.DataFrame objekte


# 08-03
### Tekste ieškoma data
* Tekste ieškoma datos (t.y. sveikųjų skaičių, kurie patenka į intervalą [1990; 2018]. Anksčiau ieškoti nelabai yra prasmės, nes prie ruso nebuvo daug įmonių, kurios prekiautų akcijomis (man taip labai stipriai atrodo))
* Taip pat parašyta funkcija, kuri randa kasmetinio akcininkų susirinkimo datą (jei tokia yra), nes tuomet iš jos galima atimti vienerius metus ir gausim metų periodą, už kurį išmokėti dividendai.


# 08-06
### Perdarytas dividendų sumos ieškojimas
* Pakeistas būdas, kaip ieškoma dividendų suma - anksčiau planuota buvo atskiros funkcijos rasti dividendus už 1 akciją ir dividendus iš viso, dabar pakeistas kodas taip, kad tą darbą atliktų viena funkcija
* Periodo, už kurį mokami dividendai, suradimas
* +- parašytas pilnos dividendų sumos chunking šablonas


# 08-07
### Baigta ieškoti dividendų sumų
* Parašytas pilnos dividendų sumos chunking šablonas (gal dar būtų galima patobulinti, bet jau nebeužsiimsiu)
* Parašyta funkcija, kuri ieško dividendų (už vieną akciją ir iš viso). Veikia +- gerai (iš sakinių su žodžiu dividend išrenka beveik viską). 
* Problemų yra su skaičių parsinimu - neparsina 3.942.000, 3 942 000, 3.942.000,00
* Pakomentuotas naujas kodas


# 08-08
### Saugo analizuotus duomenis į *.csv
* pandas.DataFrame objektas saugomas į .csv failą
* Sutvarkyta, kai saugojo metus kaip float64 (dabar kaip int)
* Perdaryta, kad metaduomenis saugotų šalia išversto ir originalaus teksto, o ne prie .html
* Galvojami algoritmai, kaip surasti įmonės pavadinimą


# 08-09
### Ieškomas kompanijos pavadinimas
* Kol kas konkrečių idėjų neturiu, tačiau yra keletas variantų, kur galima būtų pradėti:
1) Ieškoti kabučių pradžios ir pabaigos, ir jei atstumas tarp jų yra mažiau, nei, pvz., 35 simboliai - tai ir bus kažkokios kompanijos pavadinimas
2) Kadangi jau turime išrinktas dividendų sumas, būtų galima tekste ieškoti tų skaičiukų ir tuomet pagal kabutes (arba žodžius šalia AB/UAB) surasti pavadinimą
3) Straipsnio pavadinime ieškoti žodžių tarp kabučių arba žodžių, kurie vidury sakinio prasideda didžiąja raide
4) Visus šitus kaip nors sukombinuoti


# 08-10
### Toliau ieškomas kompanijos pavadinimas
* Jau kažką pavyko sukurpti - pagal dividendų vertes surandami lietuviški sakiniai ir juose tada jau galima ieškoti žodžių tarp kabučių arba tokių, kurie viduryje sakinio prasideda didžiąja raide


# 08-13
### Kompanijos pavadinimas iš sakinio
* Kai pagrindiniame tekste yra kalbama apie kompaniją X, tačiau šalimais viename sakinyje yra minima ir kompanija Y (pvz., Tuo tarpu X konkurentai kompanija Y išmokėjo n eurų dividendų) ir n skaičiukui yra priskriamas Y pavadinimas, nes kitaip būtų arba jokio pavadinimo, arba neteisingas (jei visoms dividendų sumoms iš to straipsnio būtų priskiriamas X pavadinimas)
* Jau galima paimti Y pavadinimą, taip pat padarytas ir gražus duomenų atidavimas bei naujo hashtable suformavimas, kad būtų kur laikyti kompanijos pavadinimą


# 08-14
### Išrinkti kompanijų pavadinimai
* Parašytas algoritmas, kuris išrenka kompanijų pavadinimus iš teksto
* Aišku veikia tikrai netobulai (vienas iš pavadinimų: Media bitės mano daktaras media bitės lions share) tačiau didžioji masė pavadinimų surinkta teisingai (visų nebandžiau, tačiau iš 15-20 ranka tikrintų neteisingų tebuvo 2-3)
* Dar kažką reikia daryti su šalimis (kaip nors pažymėti, kad jos yra paminėtos tekste)


# 08-16
### Testuojamas tikslumas
* Ranka patikrintas algoritmo tikslumas, kol kas 62%
* Kompanijų pavadinimų neranda nelietuviškuose tekstuose


# 08-17
### Toliau bandomas tikslumas
* Prie viso teksto dar pridedamas straipsnio pavadinimas, tai pakėlė tikslumą iki 65%
* Galima būtų pridėti kompanijos pavadinimo, paimto iš straipsnio pavadinimo, svorį (kai neranda tame pačiame sakinyje kompanijos pavadinimo, kad imtų kompanijos pavadinimą iš straipsnio pavadinimo su, pvz., 40% tikimybe, kad tai ir yra reikalingasis pavadinimas)
* Taip pat reiktų pagalvoti, kaip atpažinti ir atmesti neteisingus įrašus

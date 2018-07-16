# Iki 07-16:
### Scrapinimui išsirinkti tinkamiausią vorą/būdą kaip siųstis iš interneto puslapius. Bandyta:
* Scrapy (netiko, nes jau reikia turėti išrinktų nuorodų sąrašą, kas ir yra didžioji dalis darbo. Taip pat nepalaiko JavaScript, dėl ko kai kurių modernių puslapių gali tinkamai nenuscrapint)
* RoboBrowser (labai paprasta naudoti, tačiau nepalaiko JavaScript)
* urllib + requests (pernelyg primityvu ir low-level)
* selenium (vienintelis bandytas, kuris tiko, kadangi naršymui naudoja ne kokį nors savo generinį variklį, o plačiai paplitusias Chrome, Firefox ir Edge naršykles. Trūkumai - prie šios bibliotekos dar papildomai reikia parsisiųsti pačią naršyklę ir programą, skirtą valdyti tai naršyklei [chromedriver Chrome naršyklei ir geckodriver Firefox naršyklei])

### HTML failų apdorojimas. Bandyta:
* BeautifulSoup (labai populiari ir visur rekomenduojama biblioteka turinti labai didelę naudotojų bendruomenę, todėl į kitus, mažiau populiarius variantus ir nesidairyta)
* Built-in Python funkcijos, operacijos su string objektais - veikia - pakankamai gerai, tačiau yra low-level, taigi reikia tiksliai žinoti, kas yra norima padaryti

### Kiti svarbūs dalykai:
* Rankiniu būdu surinktas šioks toks duomenų rinkinys (su_dividendais.xslx) parašytų atskirų funkcijų testavimui (pvz. straipsnio datos suradimas)
* Google ir Bing paieškos rezultatų rinkimas naudojant selenium
* Straipsnių vertimas į anglų kalbą naudojant Google Translate ir selenium

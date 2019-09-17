1. Aplinkos sutvarkymas - reikia Python 3.7+, Git. Pasitikrinti, ar Python importuoja _sqlite3
2. Reikalingi Python pip moduliai:
+ bs4
+ googletrans
+ lxml
+ nltk
+ numpy
+ pandas
+ pycountry
+ scipy
+ sklearn 

3. VM paleisti šitą (nuklonuos iš Git): _git clone https://github.com/au6155/web_crawler_
4. Perskaityti https://github.com/au6155/web_crawler/blob/master/web_crawler/atmintine.txt
5. Tada toj pačioj VM paleisti šitą: _cd web_crawler/web_crawler && nohup python3 main.py_ ir įsitikinti, kad programa pasileidžia tvarkingai

6. Savo asmeniniame kompiuteryje sukurti 2 .bat failus:

   - ECHO ON
   - ECHO "Jungiamasi prie sd-v-03"
   - ssh -t augser@sd-v-03.lbank.lt "cd web_crawler/web_crawler && nohup python3 main.py"
   - PAUSE
   
###### Pastaba: _nohup_ numeta procesą į backgroundą, todėl kai nutraukiama SSH sesija procesas lieka veikti

**Ir**:

   - ECHO ON
   - ECHO "Jungiamasi prie sd-v-03"
   - scp augser@sd-v-03.lbank.lt:web_crawler/web_crawler/maindataframe.csv main.csv
   - PAUSE

7. Iš pradžių paleisti pirmą, o po to, kai programa baigs darbą ir antrąjį
8. https://github.com/au6155/web_crawler/blob/master/web_crawler/web_navigator.py funkcijoje get_bing_search_links() yra eilutė prasidedanti *headers = {'Ocp-Apim-Subscription-Key':*. Ten reikės įrašyti Bing API raktą (https://helpcenterhq.com/knowledgebase.php?article=189) kai jau LB turės Azure paskyrą

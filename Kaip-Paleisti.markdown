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
4. Tada toj pačioj VM paleisti šitą: _cd web_crawler/web_crawler && nohup python3 main.py_ ir įsitikinti, kad programa pasileidžia tvarkingai

5. Savo asmeniniame kompiuteryje sukurti 2 .bat failus:

   - ECHO ON
   - ECHO "Jungiamasi prie sd-v-03"
   - ssh -t augser@sd-v-03.lbank.lt "cd web_crawler/web_crawler && nohup python3 main.py"
   - PAUSE   
**Ir**:
   - ECHO ON
   - ECHO "Jungiamasi prie sd-v-03"
   - scp augser@sd-v-03.lbank.lt:web_crawler/web_crawler/maindataframe.csv main.csv
   - PAUSE

6. Iš pradžių paleisti pirmą, o po to, kai programa baigs darbą ir antrąjį

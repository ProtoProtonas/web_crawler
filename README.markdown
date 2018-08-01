# Web data collector 3000

### Web data scraper (working on this part) and analyzer (working on this part as well ;)

### Background
* My summer internship project at the Bank of Lithuania

### What is does?
* This is a web scraping tool that collects data about dividends (targeting Lithuanian companies so you might see Google Translate source language chosen as Lithuanian or something else related to the country)
* This thing heavily relies on selenium and NLTK but other libraries are also welcome (such as random or time :)

### Inner workings
1. With Google Chrome goes to google.com and bing.com and collects search results from a given keyword (testing on 'dividendai 2018')
2. After that is done the browser is switched to Mozilla Firefox as the built-in reader mode is a lifesaver in this case
3. Once the article has been opened, reader mode is triggered so that the only thing left is just plain article text
4. After that the article is translated to English a featureset is created from most common words of sample dataset (can be found in su_dividendais.txt) and pre-trained classifier then decides whether the article talks anything about dividends or not
5.1 If not, goes back to step 3 but with another article
5.2 If yes, page source and article in both original language and English are downloaded and stored in folder named 'straipsniai'

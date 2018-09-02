# Web Parasite 3000

## Web data scraper and analyzer (sort of)

### Background
* My summer internship project at the Bank of Lithuania

### What it does?
* Browser internet to find data about dividends (web-scraping tool, if you will). Currently targeting Lithuanian companies so you will see Google Translate source language chosen as Lithuanian or something else related to the country
* This thing heavily relies on selenium and NLTK but other libraries are also welcome (such as random or time :)

### Pulling data from the internet
1. With Google Chrome goes to google.com and bing.com and collects search results from a given keyword (testing on 'dividendai 2018')
2. After that is done the browser is switched to Mozilla Firefox as the built-in reader mode is a lifesaver in this case
3. Once an article has been opened, reader mode is triggered so that the only thing left is just plain article text
4. After that the article is translated to English and a featureset is created from most common words of sample dataset (can be found in su_dividendais.txt) and pre-trained classifier (Naive Bayes) then decides whether the article talks anything about dividends or not (90-100% accuracy)
5. If not, goes back to step 3 but with URL of another article
5. If yes, page source and article in both original language and English are downloaded and stored in folder named 'straipsniai'
6. Once all the articles have finished downloading a wild text analysis appears!

### Analyzing data
1. When both English and Lithuanian texts are saved, some metadata is saved along with them - article name (from <head><title>Name</title><head> of the page source), date (all the dates in page source are parsed, nomalized and the most common is chosen. If no dates found - 7777-11-11 so that it definitely stands out from the rest) as well as the URL
2. To get amount of dividends (both total and per share) NLTK is used (chunking). Templates of "correct" sentences are created using trial and error
3. After that each sentence of each article is fed to the templates and if any dividends are found the computer starts to look for date (any number between 1990 and current year) and currency (looks for 'eur', 'ltl' and 'sek' so far. More to be added soon :) )
4. Once the dividends are parsed from text we turn back to Lithuanian text and find sentences with any number that equals to the dividend amount
5. In the sentence we look for quotes or AB as the two usually go with the name of the company
6. For quotes simply text within the quotes is added next to dividends
7. For AB (akcinė bendrovė in Lithuanian) words that start with a capital letter and are close to the AB in the sentence make up the company name that is placed next to dividends
8. If there are still some names missing the most common name is chosen from the whole text
9. Overall this produces results with about 72% accuracy (bear in mind that it is plain text analysis) which is quite good result

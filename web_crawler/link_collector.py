# get_links(url) is duotos nuorodos isrenka visas nuorodas is html failo, i kuri veda duotoji nuoroda. grazinamas string masyvas

# pagridine funkcija yra get_links(url). url tipas yra string.
# visos kitos funkcijos tik "dirba" pagrindinei get_links funkcijai.

from bs4 import BeautifulSoup as bs
from selenium import webdriver

# grazina pilna nuoroda (su https://domainname.com/folder) nesvarbu, ar paduota jau su domain name (https://domainname.com/folder) ar be jo (/folder). taip pat domainname.com pavercia i https://domainname.com
def normalize_link(link, website):  # link - nuoroda i konkretu puslapi ar folderi;  website - domeno pavadinimas
    new_link = link
    new_website = website

    if 'http' not in website:
        new_website = 'https://' + new_website + '/'  #pradzioje priklijuoja https://, kad narsyklei kiltu maziau klausimu (http puslapiai redirectina, kai i juos bandoma ieiti su https
    else:
           new_website = new_website + '/' # del viso pikto ant galo priklijuoja /

    if 'http' not in link:
        if 'www' in link:
            new_link = 'https://' + new_link
        else:
            new_link = new_website + '/' + new_link   # suklijuoja nuoroda is pagrindinio domeno ir nuorodos, rastos bet_koks_puslapis.html atributuose

    while new_link.find('//') != -1:
        new_link = new_link.replace('//', '/')  # sutvarko visus besidubliuojancius pasviruosius bruksnelius 

    new_link = new_link.replace(':/', '://') # atstato dviguba pasviraji bruksneli iskart po http ir pries domeno pavadinima

    if new_link[-1] == '/':
        new_link = new_link[:-1]   #jei nuoroda baigiasi bruksneliu, tas bruksnelis yra pasalinamas

    return new_link


#def get_whole_html(url):       # is url paima html faila

#    headers = {}
#    headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"  # butina, kitaip nemaza dalis puslapiu paprasciausiai neleis prisijungti, nes galvos, kad esate robotas

#    # sitas budas nepalaiko javascript, taigi yra prastas pasirinkimas siais laikais
#    req = urllib.request.Request(url, headers = headers) 
#    resp = urllib.request.urlopen(req)
#    respData = resp.read()
#    # paverciama i BeautifulSoup objekta, kad butu lengviau manipuliuoti (siuo atveju paruosia html failo suformatavimui, kad zmogui butu paprasciau skaityti 
#    resp = bs(respData, "lxml")  
#    resp = resp.prettify() #butent tai, kas parasyta - pagrazina resp


#    return '<!--' + url + '-->' + '\n' + resp

def get_whole_html(url):
    capabilities = { 'chromeOptions':  { 'useAutomationExtension': False, 'args': ['--disable-extensions']}}
    browser = webdriver.Chrome(executable_path = 'chromedriver.exe', desired_capabilities = capabilities)
    browser.get(url)
    
    html = bs(browser.page_source)
    html = html.prettify()
    browser.close()
    return html


def get_links_from_html(whole_html, url):
    
    soup = bs(whole_html, 'lxml') 
    links = []

    # iesko <a arba <link tagu ir per visu rastu tagu masyva iteruoja, ieskodamas href atributu
    for link in soup.findAll('a'):
        try:
            full_link = normalize_link(link.get('href'), url)
            if full_link not in links:  # kad nesikartotu nuorodos tame paciame dokumente
                links.append(full_link)
        except Exception as e:
            print(e)

    # tas pats
    for link in soup.findAll('link'):
        try:
            full_link = normalize_link(link.get('href'), url)
            if full_link not in links:
                links.append(full_link)
        except Exception as e:
            print(e)

    return sorted(links)


def get_links(url):      # -> [str]
    url = normalize_link('', url)    # pradziai sutvarko pradine nuoroda
    whole_html = get_whole_html(url) 
    return get_links_from_html(whole_html, url)


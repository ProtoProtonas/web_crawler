from bs4 import BeautifulSoup as bs
from selenium import webdriver

# returns full url (https://domainname.com/folder) regardless whether it has domain name in it (https://domainname.com/folder) or not (/folder). Also turns domainname.com into https://domainname.com
def normalize_link(link, website):  # link - url to specific article or location;  website - domain name
    new_link = link
    new_website = website

    if 'http' not in website:
        new_website = 'https://' + new_website + '/'  # stick https:// to the beginning making it easier for the browser (http pages just redirect to correct address when trying to enter https)
    else:
           new_website = new_website + '/' # just in case sticks '/' at the back

    if 'http' not in link:
        if 'www' in link:
            new_link = 'https://' + new_link
        else:
            new_link = new_website + '/' + new_link

    while new_link.find('//') != -1:
        new_link = new_link.replace('//', '/')  # remove any double slashes (also works on triple, quadruple and even more slashes)

    new_link = new_link.replace(':/', '://') # puts back double slash in https://

    if new_link[-1] == '/':
        new_link = new_link[:-1]   # removes the last slash

    return new_link


#def get_whole_html(url):

#    headers = {}
#    headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17" # computer disguises itself as not a robot :D

#    # requests do not support javascript which makes it not the best choice these days
#    req = urllib.request.Request(url, headers = headers) 
#    resp = urllib.request.urlopen(req)
#    respData = resp.read()
#    # easier to manipulate BeautifulSoup object than a regular string
#    resp = bs(respData, "lxml")  
#    resp = resp.prettify()


#    return '<!--' + url + '-->' + '\n' + resp

def get_whole_html(url):
    capabilities = { 'chromeOptions':  { 'useAutomationExtension': False, 'args': ['--disable-extensions']}}
    browser = webdriver.Chrome(executable_path = 'chromedriver.exe', desired_capabilities = capabilities)
    browser.get(url)
    
    html = bs(browser.page_source) # get page source
    html = html.prettify()
    browser.close()
    return html


def get_links_from_html(whole_html, url): # extracts urls from html
    
    soup = bs(whole_html, 'lxml') 
    links = ['']
    
    # looks for <a and <link tags and in those looks for href attributes
    for link in soup.findAll('a'):
        try:
            full_link = normalize_link(link.get('href'), url)
            if full_link not in links:
                links.append(full_link)
        except Exception as e:
            print(e)
            
    # same thing
    for link in soup.findAll('link'):
        try:
            full_link = normalize_link(link.get('href'), url)
            if full_link not in links:
                links.append(full_link)
        except Exception as e:
            print(e)

    return sorted(links)


def get_links(url):      # -> [str]
    url = normalize_link('', url)    # tidies up the initial url
    whole_html = get_whole_html(url) 
    return get_links_from_html(whole_html, url)
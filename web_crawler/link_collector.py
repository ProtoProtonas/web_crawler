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

def get_links_from_html(whole_html, url): # extracts urls from html
    try:
        soup = bs(whole_html, 'lxml')

    except:
        return []

    links = ['']
    # looks for <a and <link tags and in those looks for href attributes
    links = soup.find_all('a')
    if type(links) is not None:
        if len(links) > 0:
            for link in links:
                try:
                    full_link = str(normalize_link(link, url))
                    if full_link not in links:
                        links.append(full_link)
                except:
                    pass
            
    # same thing
    links = soup.find_all('link')
    if type(links) is not None:
        if len(links) > 0:
            for link in links:
                try:
                    full_link = str(normalize_link(link, url))
                    if full_link not in links:
                        links.append(full_link)
                except:
                    pass

    try: 
        links = sorted(links)
    except:
        pass

    return links

def get_links(url):      # -> [str]
    url = normalize_link('', url)    # tidies up the initial url
    whole_html = get_whole_html(url) 
    return get_links_from_html(whole_html, url)
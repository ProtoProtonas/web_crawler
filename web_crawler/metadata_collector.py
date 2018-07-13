from bs4 import BeautifulSoup as bs
from link_collector import get_whole_html
import datetime
from collections import Counter

# ^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w
# funkcija paimti straipsnio pavadinimui
# ^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w

def get_title(html):
    head = html.split('</head>')[0]

    title_start = head.find('<title')  
    # kadangi title tag gali tureti ir atributu (nors dazniausiai neturi) tai ieskome '>' tik nuo tos vietos, kur jis prasidejo 
    title_start = head[title_start:].find('>') + title_start + 1 
    title_end = head.find('</title>')
    title = head[title_start:title_end]

    while '  ' in title:    # nuima dvigubus (ar keliagubus) tarpus, kurie gali buti like po html failo nuskaitymo
        title = title.replace('  ', ' ')

    while '\n' in title:    # pasalina \n
        title = title.replace('\n', '')

    while title[0] == ' ':  # nuima tuscius tarpus is pradzios
        title = title[1:]

    while title[-1] == ' ': # nuima tuscius tarpus nuo pabaigos
        title = title[:-1]

    return title

# ^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w
# melejonas funkciju, skirtu nustatyti straipsnio data
# ^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w

# nelabai tiksli funkcija, is bandyto dataseto teisingai atrinko 68%
def get_date(html):  
    dates = iterate_string_for_date(html)
    print(dates)
    print(Counter(dates).values())
    return most_common(dates)

def detect_date_in_string(stew_of_characters):
    #datos ilgis 10
    # is html stringo pasiimti 20 simboliu substringa ir jame ieskot datos vis paslenkant stringa kas 10 simboliu
    datos_stringas = stew_of_characters

    datos_stringas = datos_stringas.replace('"', ' ')
    datos_stringas = datos_stringas.replace('-', ' ')
    datos_stringas = datos_stringas.replace('T', ' ')
    datos_stringas = datos_stringas.replace('(', ' ')
    datos_stringas = datos_stringas.replace(')', ' ')
    datos_stringas = datos_stringas.replace('\n', ' ')

    nums = []
    [nums.append(int(s)) for s in datos_stringas.split() if s.isdigit()]

    # datos formatas lietuviskuose puslapiuose - yyyy mm dd

    article_date = datetime.date(1, 1, 1)

    for i in range(len(nums) - 2):
        if nums[i] > 2000:
            article_date = datetime.date(nums[i], nums[i + 1], nums[i + 2])
            break

    if article_date > datetime.date.today():
        raise Exception
    elif article_date.year < 2000:
        raise Exception

    return article_date


def iterate_string_for_date(html):

    months = ['sausio', 'vasario', 'kovo', 'balandžio', 'gegužės', 'birželio', 'liepos', 'rugpjūčio', 'rugsėjo', 'spalio', 'lapkričio', 'gruodžio']

    iterations = int(len(html) / 10)
    dates = []

    for x, month in enumerate(months):
        print(x + 1, ' ', month)
        while month in html:
            html = html.replace(month, str(x + 1))
            if 'm.' in html:
                html = html.replace('m.', '')
            print(x + 1, 'month checked')

    for i in range(iterations):
        substr = html[10*i : 10*i + 20]
        try:
            dates.append(detect_date_in_string(substr))
        except Exception:
            pass

    return dates


def most_common(lst):
    return max(set(lst), key=lst.count)

# ^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w
# funkcija, skirta paimti nuoroda i straipsni
# ^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w

def get_link(html):

    link = html.split('\n')[0]
    link = link[4:-3]
    return link


#urls = ['https://www.lzinios.lt/lzinios/Lietuva/urm-iesko-naujos-vietos-adolfo-ramanausko-vanago-paminklui-jav/268204', 'https://www.alfa.lt/straipsnis/50302909/korupcijos-skandalo-purtomai-panevezio-valdziai-dar-viena-pareigunu-zinia', 'https://www.delfi.lt/keliones/po-lietuva/i-ypatinga-vieta-lietuvoje-plustantys-uzsienieciai-tai-viena-graziausiu-vietu-pasaulyje.d?id=78436439', 'https://www.15min.lt/verslas/naujiena/energetika/briuselyje-pasirasytas-susitarimas-del-elektros-tinklu-sinchronizavimo-664-993920', 'https://www.lrytas.lt/lietuvosdiena/aktualijos/2018/06/28/news/i-kauna-atvyksta-ypatingas-svecias-pamate-nustebsite-kol-kas-ne-ant-zirgo-6784437/', 'http://www.diena.lt/naujienos/vilnius/menas-ir-pramogos/dainu-sventeje-tukstantis-kuriniu-ir-dalyvis-vyresnis-uz-nepriklausoma-lietuva-870436', 'https://www.vz.lt/informacines-technologijos-telekomunikacijos/2018/06/28/valstybes-kontrole-it-istekliai-vis-dar-valdomi-prastai', 'https://naujienos.alfa.lt/leidinys/iq/pazymos-ir-isvados/', 'http://www.ve.lt/naujienos/klaipeda1/klaipeda/per-juros-svente-vaziuosime-nemokamai-1645555/']

#names = ['lzinios.html', 'alfa.html', 'delfi.html', '15min.html', 'lrytas.html', 'diena.html', 'vz.html', 'iq.html', 've.html']

#for name in names:
#    file = open(name, 'r', encoding = 'utf-16')
#    disco_stu = file.read()
#    file.close()

#    print(get_date(disco_stu))

#def main():
#    for x in range(9):
#        #html = get_whole_html(urls[x])
#        with open(names[x], 'r', encoding = 'utf-16') as f:
#            html = f.read()
#            print(get_link(html))
            
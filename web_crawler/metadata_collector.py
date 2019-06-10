import datetime
from text_processor import normalize_text
from bs4 import BeautifulSoup as bs

# ^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w
# function to get article name
# ^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w

def get_title(html):

    try:
        soup = bs(html, 'lxml')
        soup = soup.find('head')
        soup = soup.find('title')
        return soup.text
    except:
        return ' '


# ^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w
# way too much functions to get article date (roughly 68% accuracy when tested)
# ^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w^w

def get_date(html):  
    dates = iterate_string_for_date(html)
    return most_common(dates)

def detect_date_in_string(stew_of_characters):
    # the length of the date is 10 symbols
    # take chunks of 20 symbols (but each time shift the chunk only by 10 symbols so none of the dates are missed
    datos_stringas = stew_of_characters

    datos_stringas = datos_stringas.replace('"', ' ')
    datos_stringas = datos_stringas.replace('-', ' ')
    datos_stringas = datos_stringas.replace('T', ' ')
    datos_stringas = datos_stringas.replace('(', ' ')
    datos_stringas = datos_stringas.replace(')', ' ')
    datos_stringas = datos_stringas.replace('\n', ' ')

    nums = []
    [nums.append(int(s)) for s in datos_stringas.split() if s.isdigit()]

    # date format in Lithunian pages - yyyy mm dd

    article_date = datetime.date(1, 1, 1)

    for i in range(len(nums) - 2):
        if nums[i] > 2000: # we are not really interested in articles posted before the year 2000 and also this is not a bad way to check for errors
            article_date = datetime.date(nums[i], nums[i + 1], nums[i + 2])
            break

    if article_date > datetime.date.today(): # the most recent articles are posted today and they cannot be posted tommorow (or later)
        raise Exception
    elif article_date.year < 2000:
        raise Exception

    return article_date


def iterate_string_for_date(html):

    months = ['sausio', 'vasario', 'kovo', 'balandžio', 'gegužės', 'birželio', 'liepos', 'rugpjūčio', 'rugsėjo', 'spalio', 'lapkričio', 'gruodžio']

    iterations = int(len(html) / 10)
    dates = []

    for x, month in enumerate(months):
        while month in html:
            html = html.replace(month, str(x + 1))
            if 'm.' in html:
                html = html.replace('m.', '')

    for i in range(iterations):
        substr = html[10*i : 10*i + 20]
        try:
            dates.append(detect_date_in_string(substr))
        except Exception:
            pass

    return dates


def most_common(lst):
    return max(set(lst), key=lst.count)

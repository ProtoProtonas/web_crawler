
def remove_duplicates(sorted_links):
    links = sorted_links
    how_many_urls = len(links)

    for i in range(how_many_urls - 1):
        n = 1
        while links[i] == links[i + n]:
            links[i + n] = '#####'
            if i + n + 1 == how_many_urls:
                break
            n += 1

    how_many_removed = 0
    while '#####' in links:
        links.remove('#####')
        how_many_removed += 1
    print(how_many_removed, 'URLs removed')

    for i, _ in enumerate(links):
        while ' ' in links[i]:
            links[i] = links[i].replace(' ', '')
        while '\n\n' in links[i]:
            links[i] = links[i].replace('\n\n', '\n')
    return links



def main():
    with open('nuorodos/links_collected_from_scraping.txt', 'r', encoding = 'utf-16') as f:
        urls = f.readlines()

    urls = sorted(urls)
    urls = remove_duplicates(urls)

    with open('nuorodos/links_collected_from_scraping_no_duplicates.txt', 'w', encoding = 'utf-16') as f:
        for url in urls:
            f.write(url)



main()


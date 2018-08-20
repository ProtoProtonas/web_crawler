
def main():
    companies = ['PST', 'Panevėžio statybos trestas', 'Birių krovinių terminalas', 'Šiaulių bankas']

    with open('list_of_companies.txt', 'w', encoding = 'utf-16') as f:
        for company in companies:
            f.write(company + '\n')


main()

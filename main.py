import argparse
import collections
import datetime
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader, select_autoescape


def get_drinks_sorted_by_category_from_excel(file_name):
    excel_data_df = pandas.read_excel(file_name, sheet_name='Лист1',
                                      usecols=['Категория', 'Имя', 'Сорт',
                                               'Цена', 'Картинка', 'Акция'],
                                      na_values='some_dummy_na_value',
                                      keep_default_na=False)
    unsorted_drinks = excel_data_df.sort_values('Категория').to_dict(
        orient='records')

    drinks_sorted_by_category = collections.defaultdict(list)
    for drink in unsorted_drinks:
        drinks_sorted_by_category[drink['Категория']].append(drink)

    return drinks_sorted_by_category


def create_parser(path_to_file_with_drinks):
    parser = argparse.ArgumentParser()
    parser.add_argument('path_to_file_with_drinks',
                        help='Введите путь к вашему Excel файлу с напитками',
                        nargs='?',
                        default=path_to_file_with_drinks)
    return parser


def main():

    load_dotenv()

    parser = create_parser(os.getenv("PATH_TO_EXCEL_FILE"))
    args = parser.parse_args()

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')

    drinks_sorted_by_category = get_drinks_sorted_by_category_from_excel(args.path_to_file_with_drinks)

    rendered_page = template.render(
        winery_age=datetime.datetime.now().year - 1920,
        drinks_sorted_by_category=drinks_sorted_by_category,
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()


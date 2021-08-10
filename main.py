import collections
import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

excel_data_df = pandas.read_excel('wine.xlsx', sheet_name='Sheet1',
                                  usecols=['Категория', 'Имя', 'Сорт',
                                           'Цена', 'Картинка', 'Акция'],
                                  na_values='some_dummy_na_value',
                                  keep_default_na=False)
drinks_unsorted = excel_data_df.sort_values('Категория').to_dict(orient='records')

drinks_sorted_by_category = collections.defaultdict(list)
for drink in drinks_unsorted:
    drinks_sorted_by_category[drink['Категория']].append(drink)

rendered_page = template.render(
    winery_age=datetime.datetime.now().year-1920,
    drinks_data=drinks_sorted_by_category,
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()


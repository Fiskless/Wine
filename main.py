from http.server import HTTPServer, SimpleHTTPRequestHandler
import datetime
import pandas
from pprint import pprint
import collections

from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

excel_data_df = pandas.read_excel('wine2.xlsx', sheet_name='Лист1',
                                  usecols=['Категория', 'Название', 'Сорт',
                                           'Цена', 'Картинка'],
                                  na_values='some_dummy_na_value',
                                  keep_default_na=False)
wine_data = excel_data_df.to_dict(orient='records')

# categories_list = []
# for wine in wine_data:
#     categories_list.append(wine['Категория'])

# wine_dict = {}
# for category in set(categories_list):
#     wine_dict[category] = [wine for wine in wine_data if category == wine['Категория']]


wine_dict = collections.defaultdict(list)
for wine in wine_data:
    wine_dict[wine['Категория']].append(wine)
pprint(wine_dict)




rendered_page = template.render(
    winery_age=datetime.datetime.now().year-1920,
    # wine_data=wine_data,
)


with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()


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

excel_data_df = pandas.read_excel('wine.xlsx', sheet_name='Sheet1',
                                  usecols=['Category', 'Name', 'Sort',
                                           'Price', 'Picture', 'Discount'],
                                  na_values='some_dummy_na_value',
                                  keep_default_na=False)
wine_data = excel_data_df.sort_values('Category').to_dict(orient='records')

drinks_dict = collections.defaultdict(list)
for wine in wine_data:
    drinks_dict[wine['Category']].append(wine)

rendered_page = template.render(
    winery_age=datetime.datetime.now().year-1920,
    drinks_data=drinks_dict,
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()


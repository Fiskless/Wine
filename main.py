from http.server import HTTPServer, SimpleHTTPRequestHandler
import datetime
import pandas

from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

excel_data_df = pandas.read_excel('wine.xlsx', sheet_name='Лист1',
                                  usecols=['Название', 'Сорт',
                                           'Цена', 'Картинка'])
wine_data = excel_data_df.to_dict(orient='records')

rendered_page = template.render(
    winery_age=datetime.datetime.now().year-1920,
    wine_data=wine_data,
)


with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
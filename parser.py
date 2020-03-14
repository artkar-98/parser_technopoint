from urllib import request
from bs4 import BeautifulSoup
import xlwt


def get_html(url):
    query = request.Request(url)
    response = request.urlopen(query)
    return BeautifulSoup(response, features='html.parser')


def get_name(tags, n):
    name_list = []
    tags_name_list = tags.find_all('a', {'class': 'ui-link', 'data-lines-to-clamp': '2'})
    for i in range(0, n):
        name_list.append(str(tags_name_list[i].next))
    return name_list


def get_code(tags, n):
    code_list = []
    tags_code_list = tags.find_all('span', {'data-product-param': 'code'})
    for i in range(0, n):
        code_list.append(str(tags_code_list[i].next))
    return code_list


def get_price(tags, n):
    price_list = []
    href_list = tags.find_all('a', {'class':'ui-link', 'data-role': 'clamped-link'})
    for i in range(0, n):
        url_price = href_list[i].get('href')
        tags_price = get_html('https://technopoint.ru/' + url_price)
        price_list.append(str(tags_price.find('span', {'class': "current-price-value"}).get('data-price-value')))
    return price_list


def get_img(tags, n):
    img_list = []
    tags_img_list = tags.find_all('source', {'type': 'image/webp'})
    for i in range(0, n):
        img_list.append(tags_img_list[i].get('data-srcset'))
    return img_list


def write_to_excel(name_list, code_list, price_list, img_list, n):
    work_file = xlwt.Workbook()
    ws = work_file.add_sheet('1')
    ws.write(0, 0, 'Наименование')
    ws.write(0, 1, 'Код товара')
    ws.write(0, 2, 'Цена')
    ws.write(0, 3, 'Ссылка на картинку')
    for i in range(1, n + 1):
        ws.write(i, 0, name_list[i - 1])
        ws.write(i, 1, code_list[i - 1])
        ws.write(i, 2, price_list[i - 1])
        ws.write(i, 3, img_list[i - 1])
    return work_file


if __name__ == '__main__':
    tags = get_html('https://technopoint.ru/catalog/recipe/e351231ca6161134/2020-goda/')
    write_to_excel(get_name(tags, 10), get_code(tags, 10), get_price(tags, 10), get_img(tags, 10), 10).save('smartphones.xls')

from bs4 import BeautifulSoup
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
import csv
import xlsxwriter as x
import requests
import io
import os
from PIL import Image

PATH = str(Path('geckodriver').resolve())
s = Service(PATH)

def write_excel(tuple):
    workbook = x.Workbook('results.xlsx')
    worksheet = workbook.add_worksheet('products')
    bold = workbook.add_format({'bold':True})
    
    row = 0
    col = 0
    
    worksheet.write(row, col, 'Nombre del Producto', bold)
    worksheet.write(row, col + 1, 'Precio', bold)
    worksheet.write(row, col + 2, 'Link', bold)
    worksheet.write(row, col + 3, 'Link de imagen', bold)
    row += 1
    
    for title, price, url, img_url in (tuple):
        worksheet.write(row, col, title)
        worksheet.write(row, col + 1, price)
        worksheet.write_url(row, col + 2, url, string='Producto')
        worksheet.write_url(row, col + 3, img_url, string='Imagen del producto')
        row += 1
    
    workbook.close()
    
def download_image(download_path, url, file_name):
     try:
         image_content = requests.get(url).content
         image_file = io.BytesIO(image_content)
         image = Image.open(image_file)
         file_path = download_path + file_name

         with open(file_path, 'wb') as f:
             image.save(f, 'JPEG')
 
         print('SUCCESS')
     except Exception as e:
         print('FAILED -', e)
 
def imgs_directory(dir_name):
    directory = dir_name
    parent_dir = '/home/bdsw3207/Code/Python/WScraping'
    path_dir = os.path.join(parent_dir, directory)
    os.mkdir(path_dir)

def url_filters():
    url_base = 'https://listado.mercadolibre.com.mx/'

    full_tag = '_Envio_Full'
    free_tag = '_CostoEnvio_Gratis'
    
    products_search = input('What are you looking for? ')
    free_shipping = input('Do you want to display only products tagged with "Free Shipping"? (Y/N) -> ')
    full_shipping = input('Do you want to display only products with FULL shipping? (Y/N) -> ')

    if free_shipping == 'Y' and full_shipping == 'Y': 
        url = f'{url_base}{products_search}{free_tag}{full_tag}'
    elif free_shipping == 'Y':
        url = (f'{url_base}{products_search}{free_tag}')
    elif full_tag == 'Y':
        url = (f'{url_base}{products_search}{full_tag}')

    return url

def get_html(url):
    wd = webdriver.Firefox(service=s)
    wd.get(url)        
    return wd.page_source
        
        
def scrape_data(product):
        title = product['title']
        url = product['href']
        # print(f'product: {title}, url: {url}')
        # print(len(product.contents))
        prices = product.find_all('span', {'class':'price-tag-fraction'})
        price = prices[1].string
        price = f'${price}'
        
        data = [title, price, url]
        
        return data

def main():
    url = url_filters()
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    
    products = soup.find_all('a', {'class': 'ui-search-result__content ui-search-link'})
    imagenes = soup.find_all('img', {'class': 'ui-search-result-image__element'})
    
    print(len(products))
    
    data_list = []
    urls = []
    
    for index, product in enumerate(products):
        data = scrape_data(product)
        img_url = imagenes[index]['src']
        data.append(img_url)
        data_list.append(data)
        urls.append(img_url)
        
    data_tuple = tuple(data_list)
    write_excel(data_tuple)
    
    directory_name = input('Directory name: ')
    imgs_directory(directory_name)
    for i, url in enumerate(urls):
        download_image(f'{directory_name}/', url, str(i) + '.jpg')
        
if __name__ == '__main__':
    main()
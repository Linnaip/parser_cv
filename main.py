import time
import undetected_chromedriver

from bs4 import BeautifulSoup


def get_product_links(url):
    """Функция собирает все ссылки товаров на странице."""
    driver = undetected_chromedriver.Chrome()
    driver.get(url)
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    links = []
    products = soup.find_all('div', attrs={'class': 'css-n9ebcy-Item'})
    for product in products:
        try:
            a_tag = product.find('a', attrs={'class': 'productCardPictureLink active css-3d15b0'})['href']
            product_link = f'https://www.auchan.ru' + f'{a_tag}'
            links.append(product_link)
        except:
            continue
    driver.quit()
    return links


def scrape_product_data(url):
    """Функция находит на странице теги товара и забирает их."""
    driver = undetected_chromedriver.Chrome()
    driver.get(url)
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    title = soup.find('h1', class_='css-pa63tw').text.strip()
    price = soup.find('div', class_='fullPricePDP css-1129a1l').next_element
    try:
        price_full = soup.find('div', class_='css-1a8h9g1').next_element
    except:
        price_full = 'Нет скидки'
    id_product = soup.find('table', attrs={'class': 'css-p83b4h'})
    tr_tag = id_product.find('td', class_='css-2619sg').text
    brend_prod = soup.find('a', class_='css-9bo89x').text

    driver.quit()
    return f'{title}, {price}, {price_full}, {tr_tag}, {brend_prod}, {url}\n'


def get_all_product_link(url):
    """Функция находит ссылки пагинации."""
    links = []
    driver = undetected_chromedriver.Chrome()
    driver.get(url)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    product_link = get_product_links(driver.current_url)
    links.extend(product_link)
    pagination = soup.find('li', class_='pagination-item css-5hicrt')
    if pagination:
        ul_tag = soup.find('ul', attrs={'class': 'css-gmuwbf'})
        page_links = ul_tag.find_all('a', attrs={'class': 'css-jzep9t'})
        for page_url in page_links[:len(page_links)-1]:
            link = page_url["href"]
            page_url = f'https://www.auchan.ru' + f'{link}'
            product_links = get_product_links(page_url)
            links.extend(product_links)
    driver.quit()
    return links


def main():
    """Основная функция."""
    base_url = 'https://www.auchan.ru/catalog/sobstvennye-marki-ashan/kazhdyy-den/bakaleya/'
    links = get_all_product_link(base_url)
    with open('products.csv', "w", encoding='utf-8') as file:
        for link in links:
            product_data = scrape_product_data(link)
            file.write(product_data)
        file.close()


if __name__ == '__main__':
    main()

import requests
from bs4 import BeautifulSoup
import time

# 获取该store所有page的url
def get_all_page_url_of_store(front_page_url):
    urls = [front_page_url]
    for i in range(2, 21):
        url = front_page_url + "?page=" + str(i)
        urls.append(url)

    return urls


# 获取单页信息
def get_id_of_page(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/65.0.3325.146 Safari/537.36 '
    }
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    body = soup.find_all('span', {'style': 'color: #333; font-size: 12px;'})
    ids = []

    for i in body:
        try:
            id = i.get_text().strip()[2:-1]
            if id.isdigit():
                ids.append(id)

        except AttributeError as e:
            continue
    return ids


# 获取商品标题、价格
def get_item_title_price(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/65.0.3325.146 Safari/537.36 '
    }
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    item=soup.find('h1', {'class': 'tm-marketplace-buyer-options__listing_title'})
    pricetemp=soup.find('p', {'class': 'tm-buy-now-box__price p-h1'})
    title = 'Undefine'
    price = 'listing closed'
    if item:
        title=item.get_text()
        if pricetemp:
            price = pricetemp.find('strong').get_text()
    temp_list = [title, price]
    return temp_list


def main():
    time_start = time.time()
    try:
        dicts = {}
        urls = get_all_page_url_of_store("https://www.trademe.co.nz/stores/smartdepot/feedback")
        for url in urls:
            item_ids = get_id_of_page(url)
            for id in item_ids:
                item_url = "https://www.trademe.co.nz/a/marketplace/listing/" + id
                item_dict = {"url": item_url, "count": 1}

                if id in dicts.keys():
                    dicts[id]["count"] += 1
                else:
                    get_item_title_price(item_url)
                    item_dict["title"] = item_url[0]
                    item_dict["price"] = item_url[1]
                    dicts[id] = item_dict
    except Exception as e:
        print(e)

    time_end = time.time()
    print('time cost', time_end - time_start, 's')
    print(dicts)


main()

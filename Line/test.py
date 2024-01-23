class product(object):
    def __init__(self, brand, name, price, store) -> None:
        self.brand = brand
        self.name = name
        self.price = price
        self.store = store

if __name__ == '__main__':
    a = str([('EPSON', 'EPSON WF-C5890高速商用傳真複合機', 79200, '元墨數位科技公司', '台中市中區中山路33號', '04-2225-9272'), ('EPSON', 'Epson WorkForce Pro WF-C869R 省 彩印A3微噴影印機', 198000, '元墨數位科技公司', '台中市中區中山路33號', '04-2225-9272'), ('EPSON', 'Epson WorkForce Pro WF-C878R省彩印A3微噴影印機', 228000, '元墨數位科技公司', '台中市中區中山路33號', '04-2225-9272')])
    for i in ['[', ']']:
        a = a.replace(i, '')
    a = a.split('), (')
    a[0] = a[0].replace('(', '')
    a[-1] = a[-1].replace(')', '')
    for i in range(len(a)):
        a[i] = a[i].replace('\'', '')

    b = []
    for i in a:
        b.append(i.split(', '))

    products = []
    store_set = set()
    for i in b:
        products.append(product(brand=i[0], name=i[1], price=i[2], store=i[3::]))
        store_set.add(' '.join(i[3::]))

    products_info = ''
    len_products = len(products)
    for i in range(len_products):
        products_info += '品牌: ' + products[i].brand + '\n' + '名稱: ' + products[i].name + '\n' + '售價: ' + products[i].price + '\n' + '店家名稱: ' + products[i].store[0] + '\n' + '店家電話: ' + products[i].store[1] + '\n' + '店家地址: ' + products[i].store[2]
        if i < len_products - 1:
            products_info += '\n\n'
    
    print(products_info)
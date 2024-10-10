from pathlib import Path
import json, requests, sqlite3, os

BASE_DIR = Path(__file__).resolve().parent.parent.parent

def get_products_from_external_api(message):
    data = json.loads(message)
    if not data:
        return

    page = int(data.get('page'))
    # Fetch product data from external API
    api_url = f"https://canilgu.dev/makyaj-api/product/?page={page}"
    response = requests.get(api_url)
    if response.status_code != 200:
        print(f"Failed to fetch products")
        return

    product_datas = response.json().get('data')
    if not product_datas:
        print(f"No data for products")
        return

    # Map external data to internal schema
    conn = sqlite3.connect(f'{BASE_DIR}/sqlite.db')
    cursor = conn.cursor()

    for product_data in product_datas:
        product = {
            'id': product_data['_id'],
            'name': product_data['product_name'],
            'description': product_data['product_description'],
            'price': float(product_data['product_price'].replace('₺', '').replace(',', '.')),
            'photo_url': str(product_data['product_image'][0]),
            'category': product_data['product_category'],
            'vendor_id': product_data['product_brand_id']
        }

    

        # Store product data into SQLite
        cursor.execute('''
            INSERT OR REPLACE INTO products (id, name, description, price, photo_url, category, vendor_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            product['id'],
            product['name'],
            product['description'],
            product['price'],
            product['photo_url'],
            product['category'],
            product['vendor_id']
        ))
        conn.commit()

    conn.close()
    print(f"Products stored in SQLite")


def get_vendors_from_external_api(message):
    data = json.loads(message)
    if not data:
        return

    # Fetch product data from external API
    api_url = f"https://canilgu.dev/makyaj-api/brand/"
    response = requests.get(api_url)
    if response.status_code != 200:
        print(f"Failed to fetch products")
        return

    vendor_datas = response.json().get('data')
    if not vendor_datas:
        print(f"No data for vendors")
        return

    # Map external data to internal schema
    conn = sqlite3.connect(f'{BASE_DIR}/sqlite.db')
    cursor = conn.cursor()

    for vendor_data in vendor_datas:
        vendor = {
            '_id':vendor_data['_id'],
            'brand_name':vendor_data['brand_name'],
            'brand_logo':vendor_data['brand_logo']
        }

    
        # Store vendor data into SQLite
        cursor.execute('''
            INSERT OR REPLACE INTO vendors (id, brand_name, brand_logo)
            VALUES (?, ?, ?)
        ''', (
            vendor['_id'],
            vendor['brand_name'],
            vendor['brand_logo'],
        ))
        conn.commit()

    conn.close()
    print(f"Products stored in SQLite")
from pyflink.datastream import StreamExecutionEnvironment, TimeCharacteristic
from pyflink.datastream.connectors import FlinkKafkaConsumer
from pyflink.common.serialization import SimpleStringSchema
import json
import requests
import sqlite3
import os

def main():
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_stream_time_characteristic(TimeCharacteristic.EventTime)

    kafka_consumer = FlinkKafkaConsumer(
        topics='product_requests',
        deserialization_schema=SimpleStringSchema(),
        properties={
            'bootstrap.servers': 'localhost:9092',
            'group.id': 'flink_consumer_group'
        }
    )

    data_stream = env.add_source(kafka_consumer)

    def process_message(message):
        data = json.loads(message)
        product_id = data.get('product_id')
        if not product_id:
            return

        # Fetch product data from external API
        api_url = f"https://canilgu.dev/makyaj-api/product/{product_id}"
        response = requests.get(api_url)
        if response.status_code != 200:
            print(f"Failed to fetch product {product_id}")
            return

        product_data = response.json().get('data')
        if not product_data:
            print(f"No data for product {product_id}")
            return

        # Map external data to internal schema
        product = {
            'id': product_data['_id'],
            'name': product_data['product_name'],
            'description': product_data['product_description'],
            'price': product_data['product_price'],
            'photo_url': product_data['product_image'][0] if product_data['product_image'] else None,
            'category': product_data['product_category'],
            'vendor_id': product_data['product_brand_id']
        }

        # Store product data into SQLite
        conn = sqlite3.connect('sqlite.db')
        cursor = conn.cursor()

        # Ensure the table exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id TEXT PRIMARY KEY,
                name TEXT,
                description TEXT,
                price TEXT,
                photo_url TEXT,
                category TEXT,
                vendor_id TEXT
            )
        ''')

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
        print(f"Product {product_id} stored in SQLite")

    data_stream.map(process_message)

    env.execute("Flink Kafka Consumer Job")

if __name__ == '__main__':
    main()
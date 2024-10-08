from pyflink.datastream import StreamExecutionEnvironment, TimeCharacteristic
from pyflink.datastream.connectors.kafka import KafkaSource, KafkaOffsetsInitializer
from pyflink.common.serialization import SimpleStringSchema
from pyflink.datastream.stream_execution_environment import StreamExecutionEnvironment, RuntimeExecutionMode
from pyflink.common import Configuration, WatermarkStrategy
from pathlib import Path
import json, requests, sqlite3, os


def main():
    jars_path = f"home/{os.environ.get('USER')}/jars/"

    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    print(BASE_DIR)
    
    env = StreamExecutionEnvironment.get_execution_environment()
    env.add_jars("file:///" + jars_path + "flink-sql-connector-kafka-3.1.0-1.17.jar")
    env.set_stream_time_characteristic(TimeCharacteristic.EventTime)
    env.set_runtime_mode(RuntimeExecutionMode.STREAMING)
    env.set_parallelism(1)


    kafka_consumer = KafkaSource.builder() \
                    .set_bootstrap_servers("localhost:29092").set_topics( 'product_requests') \
                    .set_starting_offsets(KafkaOffsetsInitializer.earliest()).set_value_only_deserializer(SimpleStringSchema()).build()
    
    kafka_consumer2 = KafkaSource.builder() \
                    .set_bootstrap_servers("localhost:29092").set_topics('product_by_id') \
                    .set_starting_offsets(KafkaOffsetsInitializer.earliest()).set_value_only_deserializer(SimpleStringSchema()).build()
    
    watermark_strategy = WatermarkStrategy.no_watermarks()

    data_stream = env.from_source(
        source=kafka_consumer,
        watermark_strategy=watermark_strategy,
        source_name="Kafka Source"
    )

    data_stream = env.from_source(
        source=kafka_consumer2,
        watermark_strategy=watermark_strategy,
        source_name="Kafka Source 2"
    )

    # data_stream = env.add_source(kafka_consumer)

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
        conn = sqlite3.connect(f'{BASE_DIR}/sqlite.db') # path dogru degil ki
        cursor = conn.cursor()

    
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
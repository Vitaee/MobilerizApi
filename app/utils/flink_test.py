from pyflink.datastream import StreamExecutionEnvironment
from pyflink.common.watermark_strategy import WatermarkStrategy
from pyflink.datastream.connectors import KafkaSource, KafkaSink
from pyflink.common.serialization import SimpleStringSchema
import json
import aiohttp
import asyncio
from app.adapters.databases.sqlite_adapter import SQLiteAdapter

async def fetch_and_store(message):
    data = json.loads(message)
    action = data.get("action")
    if action == "product_requests":
        page = data.get("page")
        # Fetch data from external API
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://external.api/products?page={page}") as response:
                products = await response.json()
        # Store in SQLite
        sqlite_adapter = SQLiteAdapter()
        async with sqlite_adapter.get_db() as db:
            for product in products.get("data", []):
                # Transform and insert into SQLite
                pass  # Implement insertion logic

def main():
    env = StreamExecutionEnvironment.get_execution_environment()
    kafka_source = KafkaSource.builder() \
        .set_bootstrap_servers("localhost:29092") \
        .set_topics("product_requests") \
        .set_group_id("flink_group") \
        .set_value_only_deserializer(SimpleStringSchema()) \
        .build()
    
    #  .set_starting_offsets(OffsetsInitializer.earliest()) \

    env.from_source(kafka_source, WatermarkStrategy.no_watermarks(), "Kafka Source") \
        .map(lambda msg: asyncio.run(fetch_and_store(msg))) \
        .print()
    
    env.execute("Flink Kafka Consumer")

if __name__ == "__main__":
    main()
from pyflink.datastream import StreamExecutionEnvironment, TimeCharacteristic
from pyflink.datastream.connectors.kafka import KafkaSource, KafkaOffsetsInitializer
from pyflink.common.serialization import SimpleStringSchema
from pyflink.datastream.stream_execution_environment import StreamExecutionEnvironment, RuntimeExecutionMode
from pyflink.common import Configuration, WatermarkStrategy
from helpers import get_vendors_from_external_api, get_products_from_external_api
from pathlib import Path
import  os


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
                    .set_bootstrap_servers("localhost:29092").set_topics('vendor_requests') \
                    .set_starting_offsets(KafkaOffsetsInitializer.earliest()).set_value_only_deserializer(SimpleStringSchema()).build()
    
    watermark_strategy = WatermarkStrategy.no_watermarks()

    data_stream2 = env.from_source(
        source=kafka_consumer,
        watermark_strategy=watermark_strategy,
        source_name="Kafka Source"
    )

    data_stream = env.from_source(
        source=kafka_consumer2,
        watermark_strategy=watermark_strategy,
        source_name="Kafka Source 2"
    )

    
    data_stream.map(get_vendors_from_external_api)
    data_stream2.map(get_products_from_external_api)

    env.execute("Flink Kafka Consumer Job")

if __name__ == '__main__':
    main()
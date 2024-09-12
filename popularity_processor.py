from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors import FlinkKafkaConsumer
from pyflink.common.serialization import SimpleStringSchema
from pyflink.common.typeinfo import Types
from pyflink.datastream.functions import MapFunction, ReduceFunction
from pyflink.datastream.window import TumblingProcessingTimeWindows
from pyflink.common.time import Time
import json


class ParseEvent(MapFunction):
    def map(self, value):
        event = json.loads(value)
        return (event['content_id'], 1)


class CountReduce(ReduceFunction):
    def reduce(self, value1, value2):
        return (value1[0], value1[1] + value2[1])


def main():
    env = StreamExecutionEnvironment.get_execution_environment()

    kafka_props = {'bootstrap.servers': 'localhost:9092', 'group.id': 'popularity_processor'}
    kafka_consumer = FlinkKafkaConsumer('watch_events', SimpleStringSchema(), kafka_props)

    stream = env.add_source(kafka_consumer)

    popularity = stream \
        .map(ParseEvent(), output_type=Types.TUPLE([Types.STRING(), Types.INT()])) \
        .key_by(lambda x: x[0]) \
        .window(TumblingProcessingTimeWindows.of(Time.minutes(5))) \
        .reduce(CountReduce())

    popularity.print()

    env.execute("Popularity Processor")


if __name__ == "__main__":
    main()
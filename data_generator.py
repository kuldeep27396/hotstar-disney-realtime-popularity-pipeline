# high_volume_data_generator.py
import random
import json
from datetime import datetime
import time
import asyncio
import aiokafka

# Expanded list of content IDs to simulate a larger content library
CONTENT_IDS = [f'movie_{i}' for i in range(1, 501)] + \
              [f'show_{i}' for i in range(1, 201)] + \
              [f'live_{i}' for i in range(1, 51)]


async def generate_watch_event():
    return {
        'content_id': random.choice(CONTENT_IDS),
        'user_id': f'user_{random.randint(1, 1000000)}',  # Expanded user base
        'timestamp': datetime.now().isoformat(),
        'duration': random.randint(1, 7200)  # Watch duration in seconds (up to 2 hours)
    }


async def send_to_kafka(producer, topic, event):
    await producer.send_and_wait(topic, json.dumps(event).encode('utf-8'))


async def main():
    producer = aiokafka.AIOKafkaProducer(bootstrap_servers=['localhost:9092'])
    await producer.start()
    topic = 'hotstar_watch_events'

    try:
        while True:
            start_time = time.time()
            tasks = [send_to_kafka(producer, topic, await generate_watch_event()) for _ in
                     range(334)]  # ~20,000 per minute
            await asyncio.gather(*tasks)
            end_time = time.time()

            # If we completed faster than 1 second, wait for the remainder
            if end_time - start_time < 1:
                await asyncio.sleep(1 - (end_time - start_time))

            print(f"Generated and sent {len(tasks)} events")

    finally:
        await producer.stop()


if __name__ == "__main__":
    asyncio.run(main())
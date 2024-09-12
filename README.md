# Hotstar Disney Real-Time Content Popularity Pipeline

This project implements a high-volume, real-time content popularity tracking system for Hotstar Disney, using Apache Kafka for event streaming and Apache Flink for stream processing. It processes billions of watch events to determine content popularity across various shows, movies, and live events on the Hotstar Disney platform.

## Overview

In the fast-paced world of streaming entertainment, understanding what content is trending in real-time is crucial. This pipeline allows Hotstar Disney to:

- Track the popularity of content across different categories (movies, TV shows, live events).
- Process and analyze billions of watch events to provide accurate, real-time popularity metrics.
- Provide up-to-date recommendations to users based on current trending content.
- Inform content acquisition and promotion strategies based on real-time viewer preferences.

## Components

1. **High Volume Data Generator** (`high_volume_data_generator.py`): Simulates Hotstar Disney watch events at a rate of 20,000 events per minute and sends them to a Kafka topic.
2. **Popularity Processor** (`popularity_processor.py`): Uses Apache Flink to process watch events and calculate content popularity in real-time.
3. **Grafana**: An open-source analytics and interactive visualization web application used to visualize the popularity data.

## Prerequisites

- Python 3.7+
- Apache Kafka
- Apache Flink
- Docker (for running Kafka and Grafana)
- Grafana

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/hotstar-disney/hotstar-disney-realtime-popularity-pipeline.git
   cd hotstar-disney-realtime-popularity-pipeline
   ```

2. Create a virtual environment and install dependencies:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   pip install aiokafka pyflink
   ```

3. Start a Kafka cluster:
   ```
   docker run -d --name kafka -p 2181:2181 -p 9092:9092 --env ADVERTISED_HOST=localhost --env ADVERTISED_PORT=9092 spotify/kafka
   ```

4. Start Grafana:
   ```
   docker run -d --name=grafana -p 3000:3000 grafana/grafana
   ```

5. Configure Flink to expose metrics. Add the following to your Flink configuration:
   ```
   metrics.reporters: prom
   metrics.reporter.prom.class: org.apache.flink.metrics.prometheus.PrometheusReporter
   metrics.reporter.prom.port: 9250-9260
   ```

6. Configure Grafana:
   - Open Grafana at `http://localhost:3000` (default credentials: admin/admin)
   - Add a Prometheus data source pointing to your Flink metrics endpoint
   - Import or create dashboards to visualize Flink metrics

## Running the Pipeline

1. Start the high volume data generator:
   ```
   python high_volume_data_generator.py
   ```

2. In a new terminal, start the popularity processor:
   ```
   python popularity_processor.py
   ```

3. Open Grafana to view the real-time popularity metrics.

## Project Structure

```
hotstar-disney-realtime-popularity-pipeline/
│
├── high_volume_data_generator.py
├── popularity_processor.py
├── README.md
└── requirements.txt
```

## Future Improvements

- Integrate with Hotstar Disney's actual data sources for live data processing.
- Implement more sophisticated popularity algorithms considering factors like watch duration, user demographics, etc.
- Develop custom Grafana dashboards for Hotstar Disney-specific metrics.
- Implement proper data storage (e.g., writing to S3 or Hotstar's data lake).
- Add configuration management for easier setup across different environments.
- Implement more robust error handling and logging for production use.
- Scale the system to handle even higher volumes of streaming data.

## Contributing

Contributions from the Hotstar Disney team are welcome! Please feel free to submit a Pull Request or open an Issue for discussion.

## License

This project is proprietary and confidential to Hotstar Disney. Unauthorized copying, distribution, or use is strictly prohibited.
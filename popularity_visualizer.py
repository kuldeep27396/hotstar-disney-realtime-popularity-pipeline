import matplotlib.pyplot as plt
from collections import defaultdict
import time


def update_popularity(popularity_data, new_data):
    for content_id, count in new_data:
        popularity_data[content_id] += count
    return dict(sorted(popularity_data.items(), key=lambda x: x[1], reverse=True)[:5])


def visualize_popularity(popularity_data):
    plt.clf()
    plt.bar(popularity_data.keys(), popularity_data.values())
    plt.title("Top 5 Popular Content")
    plt.xlabel("Content ID")
    plt.ylabel("Watch Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.pause(0.1)


def main():
    popularity_data = defaultdict(int)
    plt.ion()

    while True:
        # In a real scenario, you would read this data from your Flink job output
        # For this example, we'll simulate some data
        new_data = [
            ('movie_1', 10),
            ('show_2', 15),
            ('live_1', 20),
            ('movie_2', 5),
            ('show_1', 8)
        ]

        top_5 = update_popularity(popularity_data, new_data)
        visualize_popularity(top_5)
        time.sleep(5)  # Update every 5 seconds


if __name__ == "__main__":
    main()
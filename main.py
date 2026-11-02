import csv
import os
import time

from arduino.app_utils import App, Bridge


# Persistent dataset
DATA_DIR = "/app/data"
CSV_FILE = os.path.join(DATA_DIR, "climate_data.csv")

os.makedirs(DATA_DIR, exist_ok=True)


latest_temperature = None
latest_humidity = None
latest_mq2 = None

sample_count = 0


def receive_sensor_data(temperature, humidity, mq2):

    global latest_temperature
    global latest_humidity
    global latest_mq2

    latest_temperature = float(temperature)
    latest_humidity = float(humidity)
    latest_mq2 = int(mq2)

    print(
        f"RECEIVED: "
        f"Temperature={latest_temperature:.2f} °C, "
        f"Humidity={latest_humidity:.2f} %, "
        f"MQ2={latest_mq2}",
        flush=True
    )


# Receive sensor data from Arduino MCU
Bridge.provide("sensor_data", receive_sensor_data)


# Create CSV only if it doesn't already exist
if not os.path.exists(CSV_FILE):

    with open(CSV_FILE, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            "timestamp",
            "temperature",
            "humidity",
            "mq2"
        ])

    print("Created new climate_data.csv", flush=True)

else:

    # Count existing data rows
    with open(CSV_FILE, "r", newline="") as file:
        existing_rows = sum(1 for row in file) - 1

    print(
        f"Existing dataset found: "
        f"{existing_rows} sensor readings",
        flush=True
    )


def loop():

    global sample_count

    if latest_temperature is not None:

        timestamp = time.strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        # "a" = APPEND, NOT overwrite
        with open(CSV_FILE, "a", newline="") as file:

            writer = csv.writer(file)

            writer.writerow([
                timestamp,
                latest_temperature,
                latest_humidity,
                latest_mq2
            ])

        sample_count += 1

        print(
            f"SAVED #{sample_count}: "
            f"{timestamp} | "
            f"T={latest_temperature:.2f} °C | "
            f"H={latest_humidity:.2f} % | "
            f"MQ2={latest_mq2}",
            flush=True
        )

    time.sleep(6)


App.run(user_loop=loop)

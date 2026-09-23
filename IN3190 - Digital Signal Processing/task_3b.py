import csv
import matplotlib.pyplot as plt
from datetime import datetime, timezone
import matplotlib.dates as mdates
from datetime import datetime, timezone
import matplotlib.dates as mdates
import numpy as np

station_indices = []
distances_km = []
arrival_times = []

with open("arrival_picks.csv", mode="r", newline="") as f:
    reader = csv.reader(f)
    header = next(reader)  # Skip header row

    for row in reader:
        station_indices.append(int(row[0]))
        distances_km.append(float(row[1]))
        arrival_times.append(float(row[2]))


# Hunga Tonga major explosion onset (UTC)
t_eruption = datetime(2022, 1, 15, 4, 15, 0, tzinfo=timezone.utc)

# Convert the float from the CSV back to a timezone-aware datetime object
t_arrival = mdates.num2date(arrival_times)

# Compute elapsed travel time in seconds
travel_time_seconds = (
    np.array([(t - t_eruption).total_seconds() for t in t_arrival]) / 3600
)
plt.scatter(travel_time_seconds, distances_km)

plt.show()

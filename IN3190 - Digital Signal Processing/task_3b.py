import csv
import matplotlib.pyplot as plt
from datetime import datetime, timezone
import matplotlib.dates as mdates
from datetime import datetime, timezone
import matplotlib.dates as mdates
import numpy as np
from scipy.optimize import curve_fit


# regression moddel for curve_fit
def model(t, celerity):
    return celerity * t


def plot_celerity():
    station_indices = []
    distances = []
    arrival_times = []

    with open("arrival_picks.csv", mode="r", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)  # Skip header row

        for row in reader:
            station_indices.append(int(row[0]))
            distances.append(float(row[1]) * 1000)
            arrival_times.append(float(row[2]))

    station_indices = np.array(station_indices)
    distances = np.array(distances)

    # Hunga Tonga major explosion onset (UTC)
    t_eruption = datetime(2022, 1, 15, 4, 15, 0, tzinfo=timezone.utc)
    travel_time_seconds = (arrival_times - mdates.date2num(t_eruption)) * 86400.0

    outliers = travel_time_seconds < 1

    plt.scatter(
        travel_time_seconds[~outliers],
        distances[~outliers],
        color="blue",
        marker=".",
        label="Valid picks",
    )
    plt.scatter(
        travel_time_seconds[outliers],
        distances[outliers],
        color="red",
        marker="x",
        label="Outliers",
    )

    celerity = curve_fit(model, travel_time_seconds[~outliers], distances[~outliers])[
        0
    ][0]
    print(f"estimated celerity:{celerity:.2f}m/s")
    t = np.linspace(0, np.max(travel_time_seconds))
    plt.plot(
        t,
        model(t, celerity),
        color="black",
        label=f"Celerity regression ({celerity:.2f}m/s)",
    )

    plt.xlabel("Travel Time (seconds)")
    plt.ylabel("Distance (m)")
    plt.legend()
    plt.show()
    plt.show()


if __name__ == "__main__":
    plot_celerity()

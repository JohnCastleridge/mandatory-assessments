import os
import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from task_2 import filter_all


def pick_arrival_times(start_idx=0, end_idx=None, filename="arrival_picks.csv"):
    filter_data = filter_all(return_raw=True)
    H1 = filter_data["H1"]
    H2 = filter_data["H2"]
    H3 = filter_data["H3"]
    raw_data = filter_data["raw_data"]
    times_collection = filter_data["times"]
    dist = filter_data["dist"]
    delta_t = filter_data["dt"]

    # this is ugly but the simplest way I came up with
    sorted_data = list(zip(H1, H2, H3, raw_data, times_collection, dist, delta_t))
    sorted_data.sort(key=lambda x: x[5])  # Sort by distance

    if end_idx is None:
        end_idx = len(sorted_data)

    # used AI since I did not know how to use
    # Initialize the CSV file with headers if it doesn't exist
    if not os.path.exists(filename):
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Station_Index", "Distance_km", "Arrival_Time_Num"])

    # Loop through the specified batch of stations
    for i, (h1, h2, h3, raw, times, d, dt) in enumerate(sorted_data[start_idx:end_idx]):
        actual_idx = start_idx + i

        fig, ax = plt.subplots(2, 2, figsize=(12, 8))
        fig.suptitle(
            f"Station {actual_idx} (Distance: {d:.2f} km)\nCLICK on the wave arrival!",
            fontsize=16,
        )

        # Downsample factor: plotting all points slows down the interactive clicker
        ds = 50

        ax[0, 0].plot(times[::ds], raw[::ds], color="black", linewidth=0.5)
        ax[0, 0].set_title("Raw Data", fontsize=14)

        ax[0, 1].plot(times[::ds], h1[::ds], color="blue", linewidth=0.5)
        ax[0, 1].set_title("Filtered Data (h1[n] - Lowpass)", fontsize=14)

        ax[1, 0].plot(times[::ds], h2[::ds], color="red", linewidth=0.5)
        ax[1, 0].set_title("Filtered Data (h2[n] - Bandpass)", fontsize=14)

        ax[1, 1].plot(times[::ds], h3[::ds], color="green", linewidth=0.5)
        ax[1, 1].set_title("Filtered Data (h3[n] - Highpass)", fontsize=14)

        # Format axes for all subplots
        for axis in ax.flat:
            axis.set_xlabel("UTC Time")
            axis.set_ylabel("Amplitude")
            axis.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))

        plt.tight_layout()
        plt.subplots_adjust(top=0.88)

        # the folloing is fully written by AI
        # --- THE INTERACTIVE PICKING ENGINE ---

        # 1. Pause execution and wait for 1 mouse click (timeout=-1 means wait forever)
        click_data = plt.ginput(1, timeout=-1)

        # 2. Extract data and save if a click occurred
        if click_data:
            # ginput returns a list of tuples: [(x, y)]. We only want the x (time) value.
            picked_time = click_data[0][0]

            # 3. Append immediately to the file (Checkpointing)
            with open(filename, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([actual_idx, d, picked_time])

            print(f"Saved pick for Station {actual_idx}: Distance {d:.1f} km")

        # 4. Close the figure programmatically so the loop advances to the next station
        plt.close(fig)


pick_arrival_times(start_idx=0)

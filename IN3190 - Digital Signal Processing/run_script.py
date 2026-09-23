from task_1 import parse, plot_map, circle_distance
from task_2 import plot_impulse_responses, plot_DTFT, plot_section_plot
from task_3b import plot_celerity
from filters import h1, h2, h3

# Plots from task 1:
# data_collection, times_collection, lats, lons, dt = parse()
# n_files = len(lats)
# Hunga Tonga location
# tonga_latlon = [-20.550, -175.385]  # latitude and longitude
# Map
# plot_map(lats, lons, tonga_latlon)
# dists_km = circle_distance(n_files, lats, lons, tonga_latlon)
# fs = 1 / dt[0]  # Sampling frequency, Hz
# print("Sampling frequency is {:.2f}Hz".format(fs))


# Plots from task 2:
plot_impulse_responses(h1, h2, h3)
plot_DTFT(h1, h2, h3)
plot_section_plot()

# Plots from task 3:
plot_celerity()

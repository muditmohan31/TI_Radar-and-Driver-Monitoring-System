import os

import pandas as pd
import matplotlib.pyplot as plt

#
# def on_xlim_change(event_ax1):
#     if event_ax1.name == 'xlim':
#         ax2.set_xlim(event_ax1.get_xlim())
#
#
# def on_ylim_change(event_ax1):
#     if event_ax1.name == 'ylim':
#         ax2.set_ylim(event_ax1.get_ylim())


current_path = os.getcwd()

# Read CSV fileq
df = pd.read_csv(os.path.join(current_path, '1721297156-887109_sa_1955_cc_f_45_wg_00000_0001-0000_10_0000000.csv'))
fig, (ax1) = plt.subplots(1,1)
fig, (ax2) = plt.subplots(1,1)
fig, (ax3) = plt.subplots(1,1)

# length_df = len(df['gyrx'])
# print(length_df)
# Plot acceleration and flag on the same graph

# Plot acceleration
ax1.plot(df['counter'], df['gyrx'], label="gyrox")

# Plot flag as a square wave where flag is 1
ax2.plot(df['counter'], df['gyry'], color='red', label="gravy")

ax3.plot(df['counter'], df['gyrz'], color='green', label="gravz")


ax1.set_xlabel("")
ax1.set_ylabel("gyrx")
ax1.set_title("X")
ax1.grid(True)
ax1.set_ylim(-20, 20)

ax2.set_xlabel("")
ax2.set_ylabel("gyry")
ax2.set_title("Y")
ax2.grid(True)
ax2.set_ylim(-20, 20)  # Set y-axis range


ax3.set_xlabel("")
ax3.set_ylabel("gyrz")
ax3.set_title("Z")
ax3.grid(True)
ax3.set_ylim(-10, 10)  # Set y-axis range

plt.tight_layout()  # Adjust layout for subplots
#
# # Connect the events
# ax1.callbacks.connect('xlim_changed', on_xlim_change)
# ax1.callbacks.connect('ylim_changed', on_ylim_change)
#
# # Display the plot
plt.show()

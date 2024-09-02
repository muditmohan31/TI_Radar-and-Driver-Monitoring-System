# import os
#
# import pandas as pd
# import matplotlib.pyplot as plt
#
#
# def on_xlim_change(event_ax1):
#     if event_ax1.name == 'xlim':
#         ax2.set_xlim(event_ax1.get_xlim())
#
#
# def on_ylim_change(event_ax1):
#     if event_ax1.name == 'ylim':
#         ax2.set_ylim(event_ax1.get_ylim())
#
#
# current_path = os.getcwd()
#
# # Read CSV fileq
# df = pd.read_csv(os.path.join(current_path, 'cleaned_file.csv'))
# fig, (ax1) = plt.subplots(1,1)
# fig, (ax2) = plt.subplots(1,1)
# # Plot acceleration and flag on the same graph
#
# # Plot acceleration
# ax1.plot(df['outBreathWfm'], label="Breathe")
#
# # Plot flag as a square wave where flag is 1
# ax2.plot(df['outHeartWfm'], color='red', label="Heart")
#
# ax1.set_xlabel("Frames")
# ax1.set_ylabel("Phase(radians) ")
# ax1.set_title("Breathe Rate")
# ax1.grid(True)
# ax2.set_xlabel("Frames")
# ax2.set_ylabel("BPM")
# ax2.set_title("Heart Rate")
# ax2.grid(True)
# plt.tight_layout()  # Adjust layout for subplots
#
# # Connect the events
# ax1.callbacks.connect('xlim_changed', on_xlim_change)
# ax1.callbacks.connect('ylim_changed', on_ylim_change)
#
# # Display the plot
# plt.show()
import os
import pandas as pd
import matplotlib.pyplot as plt

def on_xlim_change(event_ax1):
    if event_ax1.name == 'xlim':
        ax2.set_xlim(event_ax1.get_xlim())

def on_ylim_change(event_ax1):
    if event_ax1.name == 'ylim':
        ax2.set_ylim(event_ax1.get_ylim())

current_path = os.getcwd()

# Read CSV file
df = pd.read_csv(os.path.join(current_path, 'sameer_radar.csv'))

# Calculate statistics
mean_breathe = df['outBreathWfm'].mean()
median_breathe = df['outBreathWfm'].median()
mode_breathe = df['outBreathWfm'].mode()[0]

mean_heart = df['outHeartWfm'].mean()
median_heart = df['outHeartWfm'].median()
mode_heart = df['outHeartWfm'].mode()[0]

fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

# Plot breathe wave
ax1.plot(df['outBreathWfm'], label="Breathe")
ax1.axhline(mean_breathe, color='g', linestyle='--', label='Mean')
ax1.axhline(median_breathe, color='b', linestyle='-.', label='Median')
ax1.axhline(mode_breathe, color='m', linestyle=':', label='Mode')
ax1.set_xlabel("Frames")
ax1.set_ylabel("Phase (radians)")
ax1.set_title("Breathe Rate")
ax1.grid(True)
ax1.legend()

# Plot heart wave
ax2.plot(df['outHeartWfm'], color='red', label="Heart")
ax2.axhline(mean_heart, color='g', linestyle='--', label='Mean')
ax2.axhline(median_heart, color='b', linestyle='-.', label='Median')
ax2.axhline(mode_heart, color='m', linestyle=':', label='Mode')
ax2.set_xlabel("Frames")
ax2.set_ylabel("BPM")
ax2.set_title("Heart Rate")
ax2.grid(True)
ax2.legend()

plt.tight_layout()  # Adjust layout for subplots

# Connect the events
ax1.callbacks.connect('xlim_changed', on_xlim_change)
ax1.callbacks.connect('ylim_changed', on_ylim_change)

# Display the plot
plt.show()

#!/usr/bin/env python3

import os
import matplotlib.pyplot as plt
import numpy as np

# Function to read data from a file
def read_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        data = []
        for line in lines:
            # Assuming format: x Name{j}: {integer}
            parts = line.strip().split()
            y, integer = parts[1].replace(':', ''), int(parts[2])
            data.append({"y": y, "int": integer})
        return data

# Read data from all files
all_data = []
for i in range(10):
    file_path = f"pkg-c-{i}.txt"
    data = read_file(file_path)
    all_data.append({f"File {i + 1}": {entry["y"]: entry["int"] for entry in data}})

# Create a list of names (y's)
for data in all_data:
    for entry in data.values()['y']:
        print(entry)
names = set(all_data[0]["y"].values())
names = list(set(entry["y"] for file_data in all_data for entry in file_data.values()))

# Create a 2D array to store the integers for each name in each file
integers_matrix = np.zeros((len(names), 10))

# Fill the array with the integer values
for i, name in enumerate(names):
    for j, file_data in enumerate(all_data):
        integers_matrix[i, j] = file_data[f"File {j + 1}"].get(name, 0)

# Create a heatmap
plt.imshow(integers_matrix, cmap="viridis", interpolation="nearest")

# Customize the plot
plt.xticks(np.arange(10), [f"File {i}" for i in range(1, 11)])
plt.yticks(np.arange(len(names)), names)
plt.xlabel("Files")
plt.ylabel("Names")
plt.title("Heatmap of Integers for Each Name Across Files")
plt.colorbar(label="Integers")

# Show the plot
plt.show()

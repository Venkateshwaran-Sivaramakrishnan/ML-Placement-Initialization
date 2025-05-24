import numpy as np

# Load the .npy file
data = np.load("cluster_tensor_data.npy", allow_pickle=True)

# Print the first entry
first_entry = data[0]
print("First entry in cluster_tensor_data.npy:")
for key, value in first_entry.items():
    print(f"{key}: {value}")
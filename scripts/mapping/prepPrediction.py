import numpy as np

# Load the npy file (list of dictionaries)
cluster_tensor_data = np.load("cluster_tensor_data.npy", allow_pickle=True)

# Convert to a Python list (optional but recommended for iteration)
cluster_tensor_data = cluster_tensor_data.tolist()

# Example: Print each entry (can be filtered or formatted as needed)
for entry in cluster_tensor_data:
    #print(f"Level: {entry['level']}, Cluster ID: {entry['cluster_id']}")
    #print(f"Node List: {entry['node_list']}")
    #print(f"T:\n{entry['T']}")
    #print(f"S:\n{entry['S']}")
    #print(f"A:\n{entry['A']}")
    #print("=" * 50)

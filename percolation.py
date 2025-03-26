import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Union–find data structure with path compression and union by rank.
def find(x, parent):
    if parent[x] != x:
        parent[x] = find(parent[x], parent)
    return parent[x]

def union(x, y, parent, rank):
    rootx = find(x, parent)
    rooty = find(y, parent)
    if rootx == rooty:
        return
    if rank[rootx] < rank[rooty]:
        parent[rootx] = rooty
    else:
        parent[rooty] = rootx
        if rank[rootx] == rank[rooty]:
            rank[rootx] += 1

# Bond Percolation on a L x L lattice using union–find
def generate_bond_percolation(p, L=300):
    n = L * L  

    parent = list(range(n))
    rank = [0] * n

    # Generate random horizontal and vertical bonds.
    horizontal_bonds = np.random.rand(L, L - 1) < p

    vertical_bonds = np.random.rand(L - 1, L) < p

    # Loop over each site and perform unions with neighbors if the bond is open.
    for i in range(L):
        for j in range(L):
            index = i * L + j
            # Check right neighbor.
            if j < L - 1 and horizontal_bonds[i, j]:
                neighbor_index = i * L + (j + 1)
                union(index, neighbor_index, parent, rank)
            # Check bottom neighbor.
            if i < L - 1 and vertical_bonds[i, j]:
                neighbor_index = (i + 1) * L + j
                union(index, neighbor_index, parent, rank)

    # Determine the cluster label for each site.
    labels = np.array([find(x, parent) for x in range(n)])
    # Map unique cluster identifiers to sequential integers.
    unique_roots, new_labels = np.unique(labels, return_inverse=True)
    new_labels = new_labels.reshape((L, L))
    num_clusters = len(unique_roots)

    # Assign a random color to each cluster.
    colors = np.random.rand(num_clusters, 3)
    rgb_image = colors[new_labels]
    return rgb_image

def main():
    L = 500           # Lattice size (L x L)
    initial_p = 0.5       # Start at the bond percolation threshold (~0.5 for a square lattice)

    # Generate the initial percolation image.
    rgb = generate_bond_percolation(initial_p, L)

    # Set up the Matplotlib figure and axis with a larger, square figure.
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect('equal')  # Ensure the plot remains square
    plt.subplots_adjust(bottom=0.25)  # Make room for the slider

    # Display the percolation image.
    im = ax.imshow(rgb, interpolation='none')
    ax.set_title(f"Bond Percolation Simulation (p = {initial_p:.2f})")
    ax.axis('off')  # Hide axis ticks

    # Create the slider for adjusting p.
    slider_ax = plt.axes([0.25, 0.1, 0.65, 0.03])
    p_slider = Slider(slider_ax, "Probability", 0.0, 1.0, valinit=initial_p)

    def update(val):
        """Update the percolation simulation when the slider changes."""
        p = p_slider.val
        new_rgb = generate_bond_percolation(p, L)
        im.set_data(new_rgb)
        ax.set_title(f"Bond Percolation Simulation (p = {p:.2f})")
        fig.canvas.draw_idle()

    p_slider.on_changed(update)
    plt.show()


if __name__ == "__main__":
    main()
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def read_input():
    lines = sys.stdin.read().split()
    idx = 0

    # Read center P of Polygon A
    center_a = np.array([float(lines[idx]), float(lines[idx + 1])])
    idx += 2

    # Read number of vertices n of Polygon A
    n = int(lines[idx])
    idx += 1

    # Read vertices of Polygon A
    polygon_a_vertices = []
    for _ in range(n):
        x = float(lines[idx])
        y = float(lines[idx + 1])
        polygon_a_vertices.append([x, y])
        idx += 2
    polygon_a_vertices = np.array(polygon_a_vertices)

    # Read center Q of Polygon B
    center_b = np.array([float(lines[idx]), float(lines[idx + 1])])
    idx += 2

    # Read number of vertices m of Polygon B
    m = int(lines[idx])
    idx += 1

    # Read vertices of Polygon B
    polygon_b_vertices = []
    for _ in range(m):
        x = float(lines[idx])
        y = float(lines[idx + 1])
        polygon_b_vertices.append([x, y])
        idx += 2
    polygon_b_vertices = np.array(polygon_b_vertices)

    return center_a, polygon_a_vertices, center_b, polygon_b_vertices

def main():
    # Read input according to the specified format
    center_a, polygon_a_vertices, center_b, polygon_b_vertices = read_input()

    # Store the initial center of Polygon B
    initial_center_b = center_b.copy()

    # Calculate the initial offset and radius
    initial_offset = initial_center_b - center_a
    radius = np.linalg.norm(initial_offset)
    initial_angle = np.arctan2(initial_offset[1], initial_offset[0])

    # Setup the plot
    fig, ax = plt.subplots()
    ax.set_aspect('equal')

    # Adjust the plot limits
    all_vertices = np.vstack((polygon_a_vertices, polygon_b_vertices))
    x_min, x_max = np.min(all_vertices[:, 0]) - 5, np.max(all_vertices[:, 0]) + 5
    y_min, y_max = np.min(all_vertices[:, 1]) - 5, np.max(all_vertices[:, 1]) + 5
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)

    # Plot Polygon A
    polygon_a = plt.Polygon(polygon_a_vertices, closed=True, fill=None, edgecolor='blue', label='Polygon A')
    ax.add_patch(polygon_a)
    # Plot center of Polygon A
    ax.plot(center_a[0], center_a[1], 'bo')

    # Plot initial Polygon B
    polygon_b_patch = plt.Polygon(polygon_b_vertices, closed=True, fill=None, edgecolor='red', label='Polygon B')
    ax.add_patch(polygon_b_patch)
    # Plot center of Polygon B
    center_b_plot, = ax.plot([initial_center_b[0]], [initial_center_b[1]], 'ro')

    # Initialize paths for each vertex of Polygon B
    num_vertices_b = polygon_b_vertices.shape[0]
    vertex_paths = []
    colors = ['green', 'orange', 'purple', 'brown', 'pink', 'cyan', 'magenta', 'yellow']
    for i in range(num_vertices_b):
        line, = ax.plot([], [], linestyle='--', linewidth=1, color=colors[i])
        vertex_paths.append({'line': line, 'x': [], 'y': []})

    # Animation function
    def animate(i):
        angle = np.radians(i) + initial_angle  # Update angle for current frame
        # Calculate new center position for Polygon B
        new_center_b = center_a + radius * np.array([np.cos(angle), np.sin(angle)])
        # Calculate the translation vector
        translation = new_center_b - initial_center_b
        # Translate Polygon B
        translated_vertices = polygon_b_vertices + translation
        polygon_b_patch.set_xy(translated_vertices)
        # Update the center point plot
        center_b_plot.set_data([new_center_b[0]], [new_center_b[1]])

        # Update the paths for each vertex
        for idx in range(num_vertices_b):
            x, y = translated_vertices[idx]
            vertex_paths[idx]['x'].append(x)
            vertex_paths[idx]['y'].append(y)
            vertex_paths[idx]['line'].set_data(vertex_paths[idx]['x'], vertex_paths[idx]['y'])

        return [polygon_b_patch, center_b_plot] + [vp['line'] for vp in vertex_paths]

    # Animate Polygon B moving around center of Polygon A
    ani = animation.FuncAnimation(
        fig, animate, frames=360, interval=20, blit=True, repeat=True
    )

    plt.legend()
    plt.show()

if __name__ == '__main__':
    main()

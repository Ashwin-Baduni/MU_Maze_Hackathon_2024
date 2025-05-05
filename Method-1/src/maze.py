"""
The maze is represented as a graph. Here we write a high performance graph
class.
"""

import tkinter as tk
import pickle
import random

class MazeGraph:
    def __init__(self):
        self.n_nodes = 0
        self.n_edges = 0

        self.nodes = []
        self.edges = []

        self.start_node = 0
        self.end_node = 0

    def randomize_maze(self, num_nodes, num_edges):
        # Generate random nodes
        for _ in range(num_nodes):
            x = random.uniform(0, 10)  # Adjust the range according to your needs
            y = random.uniform(0, 10)  # Adjust the range according to your needs
            self.add_node((x, y))

        # Generate random edges
        for _ in range(num_edges):
            node_a = random.randint(0, self.n_nodes - 1)
            node_b = random.randint(0, self.n_nodes - 1)
            if node_a != node_b:
                length = random.uniform(1, 10)  # Adjust the range according to your needs
                self.add_edge(node_a, node_b, length)

        # Set random start and end nodes
        self.set_start_node(random.randint(0, self.n_nodes - 1))
        self.set_end_node(random.randint(0, self.n_nodes - 1))

    def set_start_node(self, node_id):
        self.start_node = node_id

    def set_end_node(self, node_id):
        self.end_node = node_id

    def add_node(self, coordinate):
        # TODO: Check for extraneous nodes
        self.nodes.append(coordinate)
        self.n_nodes += 1
        return self.n_nodes - 1

    def add_edge(self, node_a, node_b, length):
        # TODO: Check for extraneous edges
        # Trying to check direction (verical or horizontal) by comparing node coordinates
        if self.nodes[node_a][0] == self.nodes[node_b][0]:
            direction = 'v'
        else:
            direction = 'h'
        self.edges.append((node_a, node_b, length, direction))
        self.n_edges += 1
        return self.n_edges - 1
    
    def get_nodes(self, node_id):
        return self.nodes[node_id]
    
    def get_node_from_coordinates(self, coordinates):
        return self.nodes.index(coordinates) if coordinates in self.nodes else -1

    def get_edge(self, edge_id):
        return self.edges[edge_id]
    
    def get_distance(self, node_a, node_b):
        for edge in self.edges:
            if (edge[0] == node_a and edge[1] == node_b) or (edge[0] == node_b and edge[1] == node_a):
                return edge[2]
        return -1

    def get_neighbours(self, node_id):
        neighbours = []
        
        for edge in self.edges:
            if edge[0] == node_id and not edge[1] in neighbours:
                neighbours.append(edge[1])
            if edge[1] == node_id and not edge[0] in neighbours:
                neighbours.append(edge[0])

        return neighbours

    def save_to_file(self, filepath):
        # Use pickle to serialize the graph object
        with open(filepath, 'wb') as file:
            pickle.dump(self, file)

    def load_from_file(self, filepath):
        # Use pickle to deserialize the graph object
        with open(filepath, 'rb') as file:
            graph = pickle.load(file)
        
        # Copy the deserialized graph object to self
        self.n_nodes = graph.n_nodes
        self.n_edges = graph.n_edges
        self.nodes = graph.nodes
        self.edges = graph.edges
        self.start_node = graph.start_node
        self.end_node = graph.end_node

    def __str__(self):
        return f"Number of nodes: {self.n_nodes}\nNumber of edges: {self.n_edges}\nNodes: {self.nodes}\nEdges: {self.edges}\nStart node: {self.start_node}\nEnd node: {self.end_node}"

    def draw(self, scale_factor = 100):
        # Use tkinter to draw the graph

        # Create a new tkinter window
        window = tk.Tk()
        window.title("Maze Graph")

        # Calculate canvas dimensions based on node coordinates
        min_x = min(scale_factor * coordinate[0] for coordinate in self.nodes)
        max_x = max(scale_factor * coordinate[0] for coordinate in self.nodes)
        min_y = min(scale_factor * coordinate[1] for coordinate in self.nodes)
        max_y = max(scale_factor * coordinate[1] for coordinate in self.nodes)
        canvas_width = max_x - min_x + 100
        canvas_height = max_y - min_y + 100

        # Create a canvas to draw the graph
        canvas = tk.Canvas(window, width=canvas_width, height=canvas_height)
        canvas.pack()

        # Clear canvas
        canvas.delete("all")

        # Draw nodes
        for node_id, coordinate in enumerate(self.nodes):
            x, y = coordinate
            scaled_x = scale_factor * x - min_x + 50  # Add some padding
            scaled_y = scale_factor * y - min_y + 50  # Add some padding

            # Check if scaled coordinates are within canvas boundaries
            if 0 <= scaled_x <= canvas_width and 0 <= scaled_y <= canvas_height:
                canvas.create_oval(scaled_x - 5, scaled_y - 5, scaled_x + 5, scaled_y + 5, fill="blue")
                canvas.create_text(scaled_x - 5, scaled_y - 15, text=str(node_id), fill="black")

        # Draw edges
        for edge in self.edges:
            node_a, node_b, length, direction = edge
            x1, y1 = self.nodes[node_a]
            x2, y2 = self.nodes[node_b]

            scaled_x1 = scale_factor * x1 - min_x + 50
            scaled_y1 = scale_factor * y1 - min_y + 50
            scaled_x2 = scale_factor * x2 - min_x + 50
            scaled_y2 = scale_factor * y2 - min_y + 50

            # Check if both nodes of the edge are within canvas boundaries
            if (0 <= scaled_x1 <= canvas_width and 0 <= scaled_y1 <= canvas_height
                    and 0 <= scaled_x2 <= canvas_width and 0 <= scaled_y2 <= canvas_height):
                if direction == 'v':
                    canvas.create_line(scaled_x1, scaled_y1, scaled_x2, scaled_y2, fill="black")
                else:
                    canvas.create_line(scaled_x1, scaled_y1, scaled_x2, scaled_y2, fill="red")

                # Calculate label position (midpoint)
                label_x = (scaled_x1 + scaled_x2) / 2
                label_y = (scaled_y1 + scaled_y2) / 2
                canvas.create_text(label_x - 5, label_y - 10, text=str(length), fill="green")



        # Start the tkinter event loop
        window.mainloop()

        


"""
Sample usage:

from maze import MazeGraph

# Create a new graph
graph = MazeGraph()

# Add nodes to the graph
node1 = graph.add_node((0, 0))
node2 = graph.add_node((0, 1))

# Add edges to the graph
edge1 = graph.add_edge(node1, node2, 1)

# Save the graph to a file
graph.save_to_file('graph.pkl')

# Load the graph from a file
new_graph = MazeGraph()
new_graph.load_from_file('graph.pkl')

# Print the nodes and edges of the new graph
print(new_graph)
"""
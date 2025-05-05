"""
Vanilla A* will not work here, as it only optimizes for
the shortest path. We need to minimize the number of turns 
as well.
"""

from queue import PriorityQueue
from src.maze import MazeGraph

class PathFinder:

    def __init__(self, maze_graph):
        self.maze_graph = maze_graph

    def base_heuristic(self, node_a, node_b):
        node_a = self.maze_graph.get_nodes(node_a)
        node_b = self.maze_graph.get_nodes(node_b)
        return abs(node_a[0] - node_b[0]) + abs(node_a[1] - node_b[1])

    def a_star_heuristic(self, node_id):
        return self.base_heuristic(node_id, self.maze_graph.end_node)

    def modified_a_star(self):
        
        def select_best_node(boundary_nodes, came_from, distances, heuristic_distances):
            best_node = None
            best_distance = float('inf')
            for boundary_node in boundary_nodes:
                distance = distances[boundary_node] + heuristic_distances[boundary_node]
                if distance < best_distance:
                    best_distance = distance
                    best_node = boundary_node
            return best_node
                
        def reconstruct_path(came_from, current_node):
            path = []
            while current_node:
                path.append(current_node)
                current_node = came_from[current_node]
            path.reverse()
            return path
        
        boundary_nodes = [self.maze_graph.start_node]
        came_from = {self.maze_graph.start_node: None}
        distances = {self.maze_graph.start_node: 0}
        heuristic_distances = {self.maze_graph.start_node: 
                               self.a_star_heuristic(self.maze_graph.start_node)}

        while len(boundary_nodes) != 0:
            current_node = select_best_node(boundary_nodes, came_from, distances, heuristic_distances)

            if current_node == self.maze_graph.end_node:
                return reconstruct_path(came_from, current_node)
            
            boundary_nodes.remove(current_node)

            for neighbour in self.maze_graph.get_neighbours(current_node):
                distance = distances[current_node] + self.maze_graph.get_distance(current_node, neighbour)
                if neighbour not in distances or distance < distances[neighbour]:
                    distances[neighbour] = distance
                    came_from[neighbour] = current_node
                    heuristic_distances[neighbour] = self.a_star_heuristic(neighbour)
                    boundary_nodes.append(neighbour)

        print("No path found")
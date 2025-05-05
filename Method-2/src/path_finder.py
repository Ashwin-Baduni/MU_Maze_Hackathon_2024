from maze_image import MazeImage
from numba import jit
from heapq import heappop, heappush

class PathFinder:

    def __init__(self, maze_image: MazeImage):
        self.image = maze_image.image

        self.start = self.coordinate_to_point_id(maze_image.start_pixel_coordinates[0],
                                                 maze_image.start_pixel_coordinates[1])
        self.end = self.coordinate_to_point_id(maze_image.end_pixel_coordinates[0],
                                               maze_image.end_pixel_coordinates[1])
        
        self.solution = None


    def coordinate_to_point_id(self, x, y):
        return y * self.image.shape[1] + x
    
    def point_id_to_coordinate(self, id):
        y = int(id / self.image.shape[1])
        return (id - y * self.image.shape[1], y)
    
    def get_point_neighbors(self, id):
        x, y = self.point_id_to_coordinate(id)

        neighbors = []

        # Checking if all the neighbors of a particular pixel are 
        # in the image bounds and whether they are white or not.

        def is_in_maze(x, y):
            if x >= 0 and x < self.image.shape[1] and y >= 0 and y < self.image.shape[0]:
                if self.image[y, x] == 255:
                    return True
                return False
            return False

        if is_in_maze(x, y - 1):
            neighbors.append(self.coordinate_to_point_id(x, y - 1))
        if is_in_maze(x, y + 1):
            neighbors.append(self.coordinate_to_point_id(x, y + 1))
        if is_in_maze(x - 1, y):
            neighbors.append(self.coordinate_to_point_id(x - 1, y))
        if is_in_maze(x + 1, y):
            neighbors.append(self.coordinate_to_point_id(x + 1, y)) 
        
        return neighbors

    def modified_a_star(self):
            
        def a_star_heuristic(id):
            x, y = self.point_id_to_coordinate(id)
            end_x, end_y = self.point_id_to_coordinate(self.end)
            return abs(end_x - x) + abs(end_y - y)

        def reconstruct_path(came_from, id):
            path = []
            while id:
                path.append(id)
                id = came_from[id]
            path.reverse()
            return path
        
        frontier = [(0, self.start)]  # Priority queue with tuples (f_score, node)
        came_from = {self.start: None}
        distances = {self.start: 0}   


        while frontier:
            _, current_node = heappop(frontier)

            if current_node == self.end:
                solution_path = reconstruct_path(came_from, current_node)
                solution = [self.point_id_to_coordinate(point) for point in solution_path]
                return solution, distances
            
            for neighbor in self.get_point_neighbors(current_node):
                distance = distances[current_node] + 1
                if neighbor not in distances or distance < distances[neighbor]:
                    distances[neighbor] = distance
                    came_from[neighbor] = current_node
                    priority = distance + a_star_heuristic(neighbor)
                    heappush(frontier, (priority, neighbor))
            
        print("No Path Found!")
        return []

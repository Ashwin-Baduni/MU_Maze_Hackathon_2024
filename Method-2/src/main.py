

"""
# Loading image, processing it and saving it for reference.
maze_image = MazeImage("../sample-images/maze4.png")
maze_image.save("../sample-images/maze4_processed.png")
#maze_image.start_pixel_coordinates = (13, 6)
#maze_image.end_pixel_coordinates = (475, 260)
print("Shape of image:", maze_image.image.shape)

# Running the path finder algorithm to get a list of coordinates that make up the path.
path_finder = PathFinder(maze_image)
id = path_finder.coordinate_to_point_id(45, 30)
print("Id of the point is", id)
print("Coordinates of the point is", path_finder.point_id_to_coordinate(id))
print("It's neighbors are:", [path_finder.point_id_to_coordinate(x) for x in path_finder.get_point_neighbors(id)])

path = path_finder.modified_a_star()
maze_image.save_solved_image(path, "../sample-images/pretty_solution4.png")

for point in path:
    x, y = point
    #print(x, y)
    maze_image.image[y, x] = 120

maze_image.save("../sample-images/solution4.png")"""

# Write an argument parser to take the png file as input and output the solution as a png file.
from maze_image import MazeImage
from path_finder import PathFinder
import argparse
import os
import math


parser = argparse.ArgumentParser(description="Solve a maze given a png file.")
parser.add_argument("input", help="The input png file.")
parser.add_argument("output", help="The output png file.")
parser.add_argument("turnfile", help="The output text file for turns.")
args = parser.parse_args()

input_file = args.input
output_file = args.output
turn_file = args.turnfile

# Checking for invalid arguments
if not os.path.isfile(input_file):
    print("Invalid input file.")
    exit()

if not output_file.endswith(".png"):
    print("Output file must be a png file.")
    exit()

if not turn_file.endswith(".txt"):
    print("Turn file must be a txt file.")
    exit()

maze_image = MazeImage(input_file)
path_finder = PathFinder(maze_image)
path, distances = path_finder.modified_a_star()
maze_image.save_solved_image(path, output_file)
#maze_image.save_solved_debug_image(path, distances, output_file)

# Calculating the number of left and right turns in the path and writing
# the exact number of turns to the turn text file.



global_prev_coord = None
global_curr_coord = None
global_next_coord = None

def calculate_direction(prev_coord, curr_coord, next_coord):
    if curr_coord[0] != prev_coord[0]:
        slope1 = (curr_coord[1] - prev_coord[1]) / (curr_coord[0] - prev_coord[0])
    else:
        slope1 = float('inf')  # Handle vertical line segment

    if next_coord[0] != curr_coord[0]:
        slope2 = (next_coord[1] - curr_coord[1]) / (next_coord[0] - curr_coord[0])
    else:
        slope2 = float('inf')  # Handle vertical line segment

    # Compare slopes to determine direction
    if slope1 < slope2:
        return "Right"
    elif slope1 > slope2:
        return "Left"
    else:
        return "Straight"
    

def count_turns_with_order(coordinates):
    global global_prev_coord, global_curr_coord, global_next_coord  
    turn_order = []
    left_turns = 0
    right_turns = 0
    
    for i in range(1, len(coordinates) - 1):
        prev_coord = coordinates[i - 1]
        curr_coord = coordinates[i]
        next_coord = coordinates[i + 1]
        
        direction = calculate_direction(prev_coord, curr_coord, next_coord)
        
        if direction != "Straight":
            # If the distance between the global next and the current previous coordinates is greater than a threshold we ignore this and that preivous turn,
            # as it is likely a noise.
            if global_prev_coord is not None and global_next_coord is not None:
                distance = math.sqrt((prev_coord[0] - global_next_coord[0])**2 + (prev_coord[1] - global_next_coord[1])**2)
                if distance < 5:
                #    if turn_order[-1] == "Left":
                #        left_turns -= 1
                #    elif turn_order[-1] == "Right":
                #        right_turns -= 1
                #    turn_order.pop()
                    continue

            if direction == "Left":
                left_turns += 1
            elif direction == "Right":
                right_turns += 1
            
            global_prev_coord = prev_coord 
            global_curr_coord = curr_coord
            global_next_coord = next_coord
            
            turn_order.append(direction)
    
    # Getting rid of the first turn 
    if turn_order[0] == "Left":
        left_turns -= 1
        # Removing frmo turn order list
        turn_order.pop(0)
    elif turn_order[0] == "Right":
        right_turns -= 1
        # Removing frmo turn order list
        turn_order.pop(0)
        
        

    
    return turn_order, left_turns, right_turns


# Count turns with order
turn_order, left_turns, right_turns = count_turns_with_order(path)

# Write to file
with open(turn_file, "w") as file:
    file.write(f"Left turns: {left_turns}\n")
    file.write(f"Right turns: {right_turns}\n")
    file.write(f"Total turns: {left_turns + right_turns}\n")
    file.write("Turn order:\n")
    for turn in turn_order:
        file.write(turn + "\n")

print("Turn counts and order have been written to", turn_file)








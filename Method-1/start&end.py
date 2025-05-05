import cv2
import numpy as np

# Read the binary image
binary_image = cv2.imread('res.png', cv2.IMREAD_GRAYSCALE)

# Find contours in the binary image
contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Sort contours by area in descending order
contours = sorted(contours, key=cv2.contourArea, reverse=True)

# Assume the outermost contour is the maze boundary
maze_boundary = contours[0]

# Find the bounding rectangle of the maze boundary
x, y, w, h = cv2.boundingRect(maze_boundary)

# Load the original image
original_image = cv2.imread('lol.png')

# Define color thresholds for yellow and blue
lower_yellow = np.array([20, 100, 100])
upper_yellow = np.array([30, 255, 255])
lower_blue = np.array([110, 50, 50])
upper_blue = np.array([130, 255, 255])

# Convert the image to HSV color space
hsv_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2HSV)

# Mask for yellow and blue regions
yellow_mask = cv2.inRange(hsv_image, lower_yellow, upper_yellow)
blue_mask = cv2.inRange(hsv_image, lower_blue, upper_blue)

# Find contours in the yellow and blue masks
yellow_contours, _ = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
blue_contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Find the extreme left point of the yellow region
yellow_left_point = tuple(yellow_contours[0][yellow_contours[0][:, :, 0].argmin()][0]) if yellow_contours else None

# Find the extreme right point of the blue region
blue_right_point = tuple(blue_contours[0][blue_contours[0][:, :, 0].argmax()][0]) if blue_contours else None

# Write the coordinates of start and end points to a text file
with open('start_end_points.txt', 'w') as file:
    file.write(f"Start Point: {yellow_left_point}\n")
    file.write(f"End Point: {blue_right_point}\n")

# Draw the start and end points on the original image
image_with_points = original_image.copy()
if yellow_left_point:
    cv2.circle(image_with_points, yellow_left_point, 5, (0, 255, 0), -1)  # Green for start point
if blue_right_point:
    cv2.circle(image_with_points, blue_right_point, 5, (0, 0, 255), -1)  # Red for end point

# Save the image with start and end points marked
cv2.imwrite('maze_with_points.png', image_with_points)

# Display the image with start and end points marked
cv2.imshow('Maze with Start and End Points', image_with_points)
cv2.waitKey(0)
cv2.destroyAllWindows()

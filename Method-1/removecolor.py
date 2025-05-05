import cv2
import numpy as np

# Load the image
image = cv2.imread('lol.png')

# Convert image to HSV color space
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Define range of yellow color in HSV
lower_yellow = np.array([20, 100, 100])
upper_yellow = np.array([30, 255, 255])

# Define range of blue color in HSV
lower_blue = np.array([90, 50, 50])
upper_blue = np.array([130, 255, 255])

# Threshold the HSV image to get only yellow and blue colors
yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

# Combine masks
mask = yellow_mask + blue_mask

# Morphological operations
kernel = np.ones((5,5), np.uint8)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

# Replace yellow and blue regions with white color
image[np.where(mask==255)] = [255, 255, 255]

# Save the result as PNG
cv2.imwrite('result.png', image)

# Display the result
cv2.imshow('Result', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

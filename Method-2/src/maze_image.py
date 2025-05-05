import cv2
import cv2 as cv
import numpy as np

class MazeImage:
    def __init__(self, path, scaling_factor = 1, kernal_size = 3):
        self.image = cv.imread(path)
        self.original_image = self.image

        self.scaling_factor = scaling_factor
        self.kernal_size = kernal_size

        self.start_pixel_coordinates = None
        self.end_pixel_coordinates = None

        self.preprocess()

        self.solution_pixels = None


    def preprocess(self):

        image = self.image
        #print("First pixel:", image[844][1584])
        image = cv2.resize(image, (0, 0), fx=self.scaling_factor, fy=self.scaling_factor)


        true_yellow = [0, 255, 255]
        true_blue = [255, 0, 0]

        # Check for first occurance of true yellow in image
        """for y in range(image.shape[0]):
            for x in range(image.shape[1]):
                if np.array_equal(image[y, x], true_yellow):
                    self.start_pixel_coordinates = (x, y)
                    break
            if self.start_pixel_coordinates:
                break"""
        
        # Iterate through the image pixels
        for y in range(image.shape[0]):
            for x in range(image.shape[1]-1, -1, -1):  # Iterate from right to left along the columns
                if np.array_equal(image[y, x], true_yellow):
                    # Update the coordinates if a yellow pixel is found
                    self.start_pixel_coordinates = (x, y)
                    break
            if self.start_pixel_coordinates:  # Break the outer loop if the pixel is found
                break

        
        # Check for last occurace of true blue in image
        for y in range(image.shape[0] - 1, -1, -1):
            for x in range(image.shape[1] - 1, -1, -1):
                if np.array_equal(image[y, x], true_blue):
                    self.end_pixel_coordinates = (x, y)
            if self.end_pixel_coordinates:
                break

        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Define the lower and upper bounds for green, blue, and yellow in HSV
        lower_green = np.array([40, 40, 40])
        upper_green = np.array([70, 255, 255])

        lower_blue = np.array([90, 50, 50])
        upper_blue = np.array([130, 255, 255])

        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([30, 255, 255])

        # Create masks for green, blue, and yellow
        mask_green = cv2.inRange(hsv_image, lower_green, upper_green)
        mask_blue = cv2.inRange(hsv_image, lower_blue, upper_blue)
        mask_yellow = cv2.inRange(hsv_image, lower_yellow, upper_yellow)

        # Combine masks for blue and yellow
        mask_blue_yellow = cv2.bitwise_or(mask_blue, mask_yellow)

        # Invert the green mask
        mask_green = cv2.bitwise_not(mask_green)

        # Combine the green mask with the blue and yellow mask
        final_mask = cv2.bitwise_or(mask_green, mask_blue_yellow)

        # Apply morphological operations to clean up the binary image
        kernel = np.ones((5, 5), np.uint8)
        final_mask = cv2.erode(final_mask, kernel, iterations=1)
        final_mask = cv2.dilate(final_mask, kernel, iterations=1)

        # Apply the mask to the original image
        result = cv2.bitwise_and(image, image, mask=final_mask)

        # Convert yellow and blue regions to white (255)
        result[mask_blue_yellow > 0] = (255, 255, 255)

        # Convert the result to binary (white is 255, everything else is 0)

    
        binary_result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

        # Apply a more aggressive threshold to ensure white is perfectly white (255)
        _, binary_result = cv2.threshold(binary_result, 250, 255, cv2.THRESH_BINARY)

        # Apply morphological operations to clean up the binary image
        kernel = np.ones((3, 3), np.uint8)
        binary_result = cv2.morphologyEx(binary_result, cv2.MORPH_CLOSE, kernel)

        # Apply a scaling factor to the binary image
        self.image = binary_result


    def coordinate_to_point_id(self, x, y):
        return y * self.image.shape[1] + x
    
    def point_id_to_coordinate(self, id):
        y = int(id / self.image.shape[1])
        return (id - y * self.image.shape[1], y)

    """
    def save_solved_image(self, path, file_path):
        mask = np.zeros((self.image.shape[0], self.image.shape[1], 3), dtype=np.uint8)
        for (x, y) in path:
            mask[y][x] = [0, 0, 255]
        mask = cv2.resize(mask, (0, 0), fx=1/self.scaling_factor, fy=1/self.scaling_factor)
        
        for x in range(self.original_image.shape[1]):
            for y in range(self.original_image.shape[0]):
                if mask[y][x][2] == 255:
                    self.original_image[y][x] = [0, 0, 255]

        #self.original_image = self.superimpose_images(self.original_image, mask)
        cv2.imwrite(file_path, self.original_image)

    def save_solved_debug_image(self, path, distances, file_path):
        # Extracting all explored nodes and storing them in explored mask
        explored_mask = np.zeros((self.image.shape[0], self.image.shape[1]), dtype=np.uint8)
        for id in distances.keys():
            x, y = self.point_id_to_coordinate(int(id))
            explored_mask[y][x] = 255

        # Extracing path mask from path
        path_mask = np.zeros((self.image.shape[0], self.image.shape[1]), dtype=np.uint8)
        for (x, y) in path:
            path_mask[y][x] = 255
        
        # Resizing masks to original image size
        explored_mask = cv2.resize(explored_mask, (0, 0), fx=1/self.scaling_factor, fy=1/self.scaling_factor)
        path_mask = cv2.resize(path_mask, (0, 0), fx=1/self.scaling_factor, fy=1/self.scaling_factor)

        # Superimposing masks on original image
        for x in range(self.original_image.shape[1]):
            for y in range(self.original_image.shape[0]):
                if explored_mask[y][x] == 255:
                    self.original_image[y][x] = [255, 0, 0]
                if path_mask[y][x] == 255:
                    self.original_image[y][x] = [0, 0, 255]
    
        # Saving the image
        cv2.imwrite(file_path, self.original_image)"""



    def save_solved_image(self, path, file_path):
        mask = np.zeros((self.image.shape[0], self.image.shape[1], 3), dtype=np.uint8)
        for (x, y) in path:
            mask[y, x] = [0, 0, 255]
        mask = cv2.resize(mask, (0, 0), fx=1/self.scaling_factor, fy=1/self.scaling_factor)

        self.original_image[np.where(mask[:, :, 2] == 255)] = [0, 0, 255]

        cv2.imwrite(file_path, self.original_image)

    def save_solved_debug_image(self, path, distances, file_path):
        # Extracting all explored nodes and storing them in explored mask
        explored_mask = np.zeros((self.image.shape[0], self.image.shape[1]), dtype=np.uint8)
        for id, _ in distances.items():
            x, y = self.point_id_to_coordinate(int(id))
            explored_mask[y, x] = 255

        # Extracing path mask from path
        path_mask = np.zeros((self.image.shape[0], self.image.shape[1]), dtype=np.uint8)
        for (x, y) in path:
            path_mask[y, x] = 255

        # Resizing masks to original image size
        explored_mask = cv2.resize(explored_mask, (0, 0), fx=1/self.scaling_factor, fy=1/self.scaling_factor)
        path_mask = cv2.resize(path_mask, (0, 0), fx=1/self.scaling_factor, fy=1/self.scaling_factor)

        # Superimposing masks on original image
        self.original_image[np.where(explored_mask == 255)] = [255, 0, 0]
        self.original_image[np.where(path_mask == 255)] = [0, 0, 255]

        # Saving the image
        cv2.imwrite(file_path, self.original_image)
    

    def save(self, path):
        cv.imwrite(path, self.image)
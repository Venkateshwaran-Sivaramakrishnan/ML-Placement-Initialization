import numpy as np
import cv2

def draw_polygon_and_save(coords, filename="polygon.jpg", image_size=(128, 128)):
    """
    Draws a polygon from the given coordinates on a 128x128 image and saves as JPG.

    Args:
        coords (list or ndarray): List of (x, y) tuples or a NumPy array of shape (N, 2).
        filename (str): Name of the output JPG file.
        image_size (tuple): Size of the image (height, width), default is (128, 128).
    """
    # Create a blank black image
    img = np.zeros((image_size[0], image_size[1], 3), dtype=np.uint8)

    # Ensure coords are in the correct shape
    pts = np.array(coords, dtype=np.int32)
    pts = pts.reshape((-1, 1, 2))  # Required shape for cv2.polylines or fillPoly

    # Draw the polygon outline (white)
    cv2.polylines(img, [pts], isClosed=True, color=(255, 255, 255), thickness=1)

    # Optionally fill the polygon (uncomment below)
    # cv2.fillPoly(img, [pts], color=(255, 255, 255))

    # Save the image
    cv2.imwrite(filename, img)

# Example usage:
draw_polygon_and_save([(10, 10), (10, 117), (117, 117), (117, 10)], "0.jpg")

import cv2
import numpy as np
from tkinter import Tk, filedialog

# Function to select an image file
def select_image():
    root = Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")])
    return file_path

# Mouse callback function to get position, color, and intensity
def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:  # Capture when the mouse moves
        # Get the color of the pixel (BGR)
        color = param[y, x]
        b, g, r = color

        # Convert BGR to grayscale (intensity)
        intensity = np.mean(color)

        # Print the results
        print(f"Position: ({x}, {y}) | Intensity: {intensity:.2f}")

# Main function
def main():
    # Select an image file
    image_path = select_image()

    if not image_path:
        print("No image selected.")
        return
    
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print("Failed to load image.")
        return

    # Create a window
    cv2.namedWindow('Image')

    # Set the mouse callback function
    cv2.setMouseCallback('Image', mouse_callback, param=image)

    # Display the image and wait for user input
    while True:
        cv2.imshow('Image', image)
        
        # Break the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

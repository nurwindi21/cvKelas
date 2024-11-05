from tkinter import Tk, filedialog
from PIL import Image
import numpy as np
import os
from scipy.ndimage import sobel

# Function to select an image file from a specific directory
def select_image(directory):
    root = Tk()
    root.withdraw()  # Hide the root window
    
    # Set initial directory for file dialog
    file_path = filedialog.askopenfilename(initialdir=directory, filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")])
    return file_path

# Function to apply edge detection using Sobel operator
def detect_edges(image_array):
    # Apply Sobel operator to detect edges
    sobel_x = sobel(image_array, axis=0)  # Horizontal edges
    sobel_y = sobel(image_array, axis=1)  # Vertical edges

    # Calculate the magnitude of the gradient
    edge_magnitude = np.hypot(sobel_x, sobel_y)

    # Normalize the edge magnitude to 0-255 and convert to uint8
    edge_magnitude = np.uint8(255 * (edge_magnitude / np.max(edge_magnitude)))

    return edge_magnitude

# Main function
def main():
    # Specify the directory from which to choose an image
    directory = "C:\OneDrive\Document\Petra\Sem5\COMVIS\Lab Kelas\Meet03\Bunga01.jpeg"  # Adjust this to your desired directory
    
    # Ensure the directory exists
    if not os.path.exists(directory):
        print(f"Directory does not exist: {directory}")
        return
    
    # Select an image file from the specified directory
    image_path = select_image(directory)
    
    if not image_path:
        print("No image selected.")
        return
    
    # Load the image
    image = Image.open(image_path).convert('L')  # Convert to grayscale
    image_array = np.array(image)
    
    # Detect edges
    edge_array = detect_edges(image_array)

    # Convert the edge array back to an image
    edge_image = Image.fromarray(edge_array)
    
    # Save the edge-detected image in the current working directory with a fixed name
    edge_image.save('EdgeDetectedImage.png')
    print("Image saved as: EdgeDetectedImage.png")

    # Display the edge-detected image using PIL
    edge_image.show()

if __name__ == "__main__":
    main()

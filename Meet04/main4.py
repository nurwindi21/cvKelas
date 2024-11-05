from tkinter import Tk, filedialog
from PIL import Image
import numpy as np
import os
from scipy.ndimage import sobel, gaussian_filter

# Function to select an image file from a specific directory
def select_image(directory):
    root = Tk()
    root.withdraw()  # Hide the root window
    
    # Set initial directory for file dialog
    file_path = filedialog.askopenfilename(initialdir=directory, filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")])
    return file_path

# Function to apply edge detection and highlight edges
def detect_and_highlight_edges(image_array):
    # Apply Gaussian smoothing to reduce noise and sensitivity
    smoothed_image = gaussian_filter(image_array, sigma=1)  # Adjust sigma for more or less smoothing

    # Apply Sobel operator to detect edges
    sobel_x = sobel(smoothed_image, axis=0, mode='reflect')  # Horizontal edges
    sobel_y = sobel(smoothed_image, axis=1, mode='reflect')  # Vertical edges

    # Calculate the magnitude of the gradient
    edge_magnitude = np.hypot(sobel_x, sobel_y)

    # Normalize the edge magnitude to 0-255
    edge_magnitude = (edge_magnitude / np.max(edge_magnitude)) * 255.0

    # Ensure all values are in the range 0-255
    edge_magnitude = np.clip(edge_magnitude, 0, 255)

    # Apply a higher threshold to make the kernel less sensitive
    threshold = 150  # Increase this value for less sensitivity
    edge_highlighted = np.where(edge_magnitude > threshold, 255, 0)

    # Convert to uint8
    edge_highlighted = np.uint8(edge_highlighted)

    return edge_highlighted

# Main function
def main():
    # Specify the directory from which to choose an image
    directory = "C:\\OneDrive\\Document\\Petra\\Sem5\\COMVIS\\Lab Kelas\\Meet03\\"  # Adjust this to your desired directory
    
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
    
    # Detect and highlight edges
    edge_highlighted_array = detect_and_highlight_edges(image_array)

    # Convert the highlighted edge array back to an image
    edge_highlighted_image = Image.fromarray(edge_highlighted_array)
    
    # Save the edge-detected image in the current working directory with a fixed name
    edge_highlighted_image.save('HighlightedEdgeImage.png')
    print("Image saved as: HighlightedEdgeImage.png")

    # Display the edge-detected image using PIL
    edge_highlighted_image.show()

if __name__ == "__main__":
    main()

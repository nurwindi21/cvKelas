from tkinter import Tk, filedialog
from PIL import Image
import numpy as np
import os
from scipy.ndimage import gaussian_filter, median_filter

# Function to select an image file from a specific directory
def select_image(directory):
    root = Tk()
    root.withdraw()  # Hide the root window

    # Set initial directory for file dialog
    file_path = filedialog.askopenfilename(initialdir=directory, filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")])
    return file_path

# Function to apply Gaussian smoothing manually
def apply_gaussian_smoothing(image_array):
    # Apply median filter first to reduce noise
    image_array = median_filter(image_array, size=3)  # Reducing noise while preserving edges
    
    # Define a larger 5x5 Gaussian kernel
    gaussian_kernel = np.array([[1, 4, 6, 4, 1],
                                [4, 16, 24, 16, 4],
                                [6, 24, 36, 24, 6],
                                [4, 16, 24, 16, 4],
                                [1, 4, 6, 4, 1]]) / 256  # Normalized to sum to 1

    # Apply Gaussian smoothing using a pre-built filter
    smoothed_image = gaussian_filter(image_array, sigma=2)  # sigma increased for stronger smoothing
    
    return smoothed_image

# Function to apply the Sobel operator manually
def apply_sobel_operator(image_array):
    # Define Sobel kernels for x and y directions
    sobel_x = np.array([[-1, 0, 1],
                        [-2, 0, 2],
                        [-1, 0, 1]])

    sobel_y = np.array([[1, 2, 1],
                        [0, 0, 0],
                        [-1, -2, -1]])

    # Pad the image to handle borders
    padded_image = np.pad(image_array, pad_width=1, mode='reflect')

    # Create empty arrays for the gradients
    gradient_x = np.zeros_like(image_array)
    gradient_y = np.zeros_like(image_array)

    # Apply Sobel operator in both x and y directions
    for i in range(gradient_x.shape[0]):
        for j in range(gradient_x.shape[1]):
            region = padded_image[i:i+3, j:j+3]  # Get the 3x3 region
            gradient_x[i, j] = np.sum(region * sobel_x)
            gradient_y[i, j] = np.sum(region * sobel_y)

    # Calculate the magnitude of the gradient
    edge_magnitude = np.hypot(gradient_x, gradient_y)

    # Normalize the edge magnitude to 0-255
    edge_magnitude = (edge_magnitude / np.max(edge_magnitude)) * 255.0

    # Ensure all values are in the range 0-255
    edge_magnitude = np.clip(edge_magnitude, 0, 255)

    return edge_magnitude

# Function to detect and highlight edges
def detect_and_highlight_edges(image_array):
    # Apply Gaussian smoothing with noise reduction
    smoothed_image = apply_gaussian_smoothing(image_array)

    # Apply Sobel operator
    edge_magnitude = apply_sobel_operator(smoothed_image)

    # Dynamic threshold based on the image's statistics
    threshold = np.percentile(edge_magnitude, 80)  # 80th percentile instead of a fixed value
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

from tkinter import Tk, filedialog
from PIL import Image
import numpy as np
import os

# Function to select an image file from a specific directory
def select_image(directory):
    root = Tk()
    root.withdraw()  # Hide the root window

    # Set initial directory for file dialog
    file_path = filedialog.askopenfilename(initialdir=directory, filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")])
    return file_path

# Function to apply Gaussian smoothing manually
def apply_gaussian_smoothing(image_array):
    # Define a 5x5 Gaussian kernel for more smoothing
    gaussian_kernel = np.array([[1, 4, 6, 4, 1],
                                [4, 16, 24, 16, 4],
                                [6, 24, 36, 24, 6],
                                [4, 16, 24, 16, 4],
                                [1, 4, 6, 4, 1]]) / 256  # Normalize to sum to 1

    # Pad the image to handle borders
    padded_image = np.pad(image_array, pad_width=2, mode='reflect')

    # Create an empty array for the smoothed image
    smoothed_image = np.zeros_like(image_array)

    # Convolve the image with the Gaussian kernel
    for i in range(smoothed_image.shape[0]):
        for j in range(smoothed_image.shape[1]):
            region = padded_image[i:i+5, j:j+5]  # Get the 5x5 region
            smoothed_image[i, j] = np.sum(region * gaussian_kernel)

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
    # Apply Gaussian smoothing
    smoothed_image = apply_gaussian_smoothing(image_array)

    # Apply Sobel operator
    edge_magnitude = apply_sobel_operator(smoothed_image)

    # Apply a threshold to reduce sensitivity
    threshold = 150  # Adjust for sensitivity
    edge_highlighted = np.where(edge_magnitude > threshold, edge_magnitude, 0)

    return np.uint8(edge_highlighted)

# Function to restore the image by blending the edges
def restore_image_with_edges(original_image_array, edge_array):
    # Normalize the edges to create a blending effect
    alpha = edge_array / 255.0  # Scale from 0 to 1 for blending

    # Blend the original image with the highlighted edges
    restored_image = np.uint8((1 - alpha) * original_image_array + alpha * 255)

    return restored_image

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

    # Restore the image with highlighted edges
    restored_image_array = restore_image_with_edges(image_array, edge_highlighted_array)

    # Convert the restored image array back to an image
    restored_image = Image.fromarray(restored_image_array)

    # Save the restored image in the current working directory with a fixed name
    restored_image.save('RestoredImageWithEdges.png')
    print("Image saved as: RestoredImageWithEdges.png")

    # Display the restored image using PIL
    restored_image.show()

if __name__ == "__main__":
    main()

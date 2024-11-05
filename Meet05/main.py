from PIL import Image, ImageFilter
import numpy as np
import matplotlib.pyplot as plt
from tkinter import filedialog
from tkinter import Tk

# Function to select an image using a file dialog
def select_image():
    root = Tk()
    root.withdraw()  # Hide the main tkinter window
    file_path = filedialog.askopenfilename()
    return file_path

# Load and convert image to grayscale
def load_image(image_path):
    return Image.open(image_path).convert('L')

# Apply Sobel edge detection
def sobel_edge_detection(image):
    # Convert image to numpy array
    img_array = np.array(image)

    # Sobel kernels for detecting edges
    sobel_x = np.array([[-1, 0, 1],
                        [-2, 0, 2],
                        [-1, 0, 1]])

    sobel_y = np.array([[-1, -2, -1],
                        [0,  0,  0],
                        [1,  2,  1]])

    # Apply convolution to detect edges
    grad_x = apply_convolution(img_array, sobel_x)
    grad_y = apply_convolution(img_array, sobel_y)

    # Calculate gradient magnitude
    gradient_magnitude = np.sqrt(grad_x ** 2 + grad_y ** 2)
    gradient_magnitude = (gradient_magnitude / np.max(gradient_magnitude)) * 255  # Normalize

    return Image.fromarray(gradient_magnitude.astype(np.uint8))

# Function to apply convolution
def apply_convolution(img, kernel):
    img_height, img_width = img.shape
    kernel_height, kernel_width = kernel.shape

    # Define the output array
    output = np.zeros(img.shape)

    # Apply convolution (ignoring the border)
    for i in range(1, img_height - 1):
        for j in range(1, img_width - 1):
            region = img[i-1:i+2, j-1:j+2]
            output[i, j] = np.sum(region * kernel)

    return output

# Display original and edge-detected images side by side
def display_images_side_by_side(img1, img2):
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    axes[0].imshow(img1, cmap='gray')
    axes[0].set_title('Original Image')
    axes[0].axis('off')

    axes[1].imshow(img2, cmap='gray')
    axes[1].set_title('Edge Detected Image')
    axes[1].axis('off')

    plt.show()

# Main function
def main():
    print("Select an image:")
    img_path = select_image()

    # Load the image
    img = load_image(img_path)

    # Apply Sobel edge detection
    edge_detected_img = sobel_edge_detection(img)

    # Display the original and edge-detected images side by side
    display_images_side_by_side(img, edge_detected_img)

# Run the program
if __name__ == "__main__":
    main()

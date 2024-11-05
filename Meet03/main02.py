from tkinter import Tk, filedialog
from PIL import Image, ImageOps
import numpy as np
import os

# Function to select an image file
def select_image():
    root = Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")])
    return file_path

# Function to apply a custom kernel manually
def apply_custom_kernel(image_array, kernel):
    height, width = image_array.shape
    kernel_size = kernel.shape[0]
    offset = kernel_size // 2
    blurred_array = np.zeros_like(image_array)

    # Iterate over every pixel in the image
    for i in range(offset, height - offset):
        for j in range(offset, width - offset):
            # Extract the region of interest
            region = image_array[i-offset:i+offset+1, j-offset:j+offset+1]
            # Apply the kernel to the region
            blurred_value = np.sum(region * kernel)
            # Clip the values to stay within [0, 255]
            blurred_array[i, j] = np.clip(blurred_value, 0, 255)

    return blurred_array

# Main function
def main():
    # Select an image file
    image_path = select_image()
    
    if not image_path:
        print("No image selected.")
        return
    
    # Load the image and convert to grayscale
    image = Image.open(image_path).convert('L')
    image_array = np.array(image)
    
    # Define a custom 3x3 blurring kernel
    kernel = np.array([
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1]
    ])/25  # Normalize the kernel
    
    # Apply the custom kernel
    blurred_array = apply_custom_kernel(image_array, kernel)

    # Convert the blurred array back to an image
    blurred_image = Image.fromarray(np.uint8(blurred_array))
    
    # Save and display the blurred image
    blurred_image.save('Blurred_Image.png')
    blurred_image.show()

if __name__ == "__main__":
    main()

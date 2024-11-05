from tkinter import Tk, filedialog
from PIL import Image, ImageOps
import numpy as np
import os

# Function to select an image file from a specific directory
def select_image(directory):
    root = Tk()
    root.withdraw()  # Hide the root window
    
    # Set initial directory for file dialog
    file_path = filedialog.askopenfilename(initialdir=directory, filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")])
    return file_path

# Function to apply box blur on the image array
def apply_box_blur(image_array, kernel_size=3):
    height, width = image_array.shape
    blurred_array = np.copy(image_array)

    # Offset to determine neighbors
    offset = kernel_size // 2

    # Loop through each pixel in the image array
    for i in range(offset, height - offset):
        for j in range(offset, width - offset):
            # Extract the kernel (neighboring pixels)
            kernel = image_array[i-offset:i+offset+1, j-offset:j+offset+1]
            # Calculate the average value of the kernel
            blurred_array[i, j] = np.mean(kernel)

    return blurred_array

# Main function
def main():
    # Specify the directory from which to choose an image
    directory = "C:\OneDrive\Document\Petra\Sem5\COMVIS\Lab Kelas\Meet03\Bunga01.jpeg"  # Change this to your desired directory
    
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
    
    # Apply box blur
    blurred_array = apply_box_blur(image_array, kernel_size=3)

    # Convert the blurred array back to an image
    blurred_image = Image.fromarray(np.uint8(blurred_array))
    blurred_image.save('Blurred06.png')

    # Display the blurred image using PIL
    blurred_image.show()

if __name__ == "__main__":
    main()

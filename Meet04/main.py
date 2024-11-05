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

# Function to apply gradient from dark to light
def apply_gradient(image_array):
    height, width = image_array.shape
    gradient_array = np.copy(image_array)
    
    for x in range(width):
        brightness = int(255 * (x / width))  # Calculate brightness from 0 to 255
        gradient_array[:, x] = brightness
    
    return gradient_array

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
    
    # Apply gradient
    gradient_array = apply_gradient(image_array)

    # Convert the gradient array back to an image
    gradient_image = Image.fromarray(np.uint8(gradient_array))
    
    # Save the gradient image in the current working directory with a fixed name
    gradient_image.save('GradientImage.png')
    print("Image saved as: GradientImage.png")

    # Display the gradient image using PIL
    gradient_image.show()

if __name__ == "__main__":
    main()

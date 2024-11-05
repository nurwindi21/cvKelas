from tkinter import Tk, filedialog
from PIL import Image, ImageOps
import numpy as np

def open_image():
    """Open a file dialog to select an image."""
    root = Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")])
    return file_path

def apply_blur_kernel(image_array):
    """Apply a 3x3 blurring kernel to a grayscale image array."""
    kernel = np.array([
        [1/9, 1/9, 1/9],
        [1/9, 1/9, 1/9],
        [1/9, 1/9, 1/9]hape
    blurred_array = np.zeros_like(image_array)

    # Apply the kernel to each pixel (except for the border pixels)
    for i in range(1, height-1):
        for j in range(1, width-1):
            # Extract 3x3 region around the current pixel
            region = image_array[i-1:i+2, j-1:j+2]
            # Apply the kernel
            blurred_value = np.sum(region * kernel)
            # Assign the blurred value to the new array
            blurred_array[i, j] = np.clip(blurred_value, 0, 255)

    return blurred_array

def main():
    # Open an image file
    mage()
    if not image_path:
        print("No image selected.")
        return

    # Load the image and convert to grayscale
    image = Image.open(image_path).convert('L')
    image_array = np.array(image)

    # Apply the blur effect
    blurred_array = apply_blur_kernel(image_array)

    # Convert the blurred array back to an image
    blurred_image = Image.fromarray(np.uint8(blurred_array))

    # Save and show the blurred image
    blurred_image.save('Blurred_Result.png')
    blurred_image.show()

if __name__ == "__main__":
    main()

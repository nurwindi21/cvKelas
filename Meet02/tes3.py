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

# Main function
def main():
    # Specify the directory from which to choose an image
    directory = "C:\OneDrive\Document\Petra\Sem5\COMVIS\Lab Kelasz\Meet02\itemputih.jpg"  # Change this to your desired directory
    
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

    


    # Get image dimensions
    height, width = image_array.shape
    print(f"Image Dimensions: Width = {width}px, Height = {height}px")


    flipped_array2 = np.copy(image_array)
    for i in range(height):
        for j in range(width):
            flipped_array2[i][j] = image_array[i][width - j -1]

    flipped_array2_image = Image.fromarray(flipped_array2)
    flipped_array2_image.save('flipped2.png')

    # row1_array2 = np.copy(image_array)
    # for i in range(height):
    #     for j in range(width):
    #         row1_array2[i][j] = image_array[i][width - j -1]

    # row1_image = Image.fromarray(row1_array2)
    # row1_image.save('flipped2.png')

    for j in range(width):
        print(f"{0}, {j} = {image_array[0][j]}")

    inverted_array = np.copy(image_array)
    for i in range(height):
        for j in range(width):
            inverted_array[i][j] = min(image_array[i][j] + 50, 255)

    inverted_array_image = Image.fromarray(inverted_array)
    inverted_array_image.save('brighter.png')

    # Flip the image vertically
    flipped_image = ImageOps.flip(image)
    
    # Convert the flipped image back to an array if needed
    flipped_array = np.array(flipped_image)

    flipped_image_from_array = Image.fromarray(flipped_array)
    flipped_image_from_array.save("output.png")

    # Display the flipped image using PIL
    flipped_image.show()

if __name__ == "__main__":
    main()

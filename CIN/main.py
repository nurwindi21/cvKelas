from PIL import Image
import numpy as np

def read_image(path):
    img = Image.open(path)
    img_array = np.array(img)
    height, width, channels = img_array.shape
    return img_array, height, width

def read_grayscale_image(path):
    img = Image.open(path).convert('L')
    img_array = np.array(img)
    height, width = img_array.shape
    return img_array, height, width

def save_image(img_array, path, show=False):
    img = Image.fromarray(img_array)
    img.save(path)
    if show:
        img.show()

def combine_images(path1, path2, output_path, show=False):
    img1 = Image.open(path1)
    img2 = Image.open(path2)

    # Adjust heights to be the same if needed
    if img1.height != img2.height:
        img1 = img1.resize((img1.width, img2.height))
        img2 = img2.resize((img2.width, img1.height))

    combined_width = img1.width + img2.width
    max_height = max(img1.height, img2.height)

    combined_img = Image.new("RGB", (combined_width, max_height))

    combined_img.paste(img1, (0, 0))
    combined_img.paste(img2, (img1.width, 0))

    combined_img.save(output_path)
    if show:
        combined_img.show()

# Read the image and prepare the filter
img_array, height, width = read_image('kucing03.jpeg')

kernel = np.ones((7, 7)) / 49
kernel_radius_x = kernel.shape[0] // 2
kernel_radius_y = kernel.shape[1] // 2

# Initialize the output image
output_array = np.copy(img_array)

# Apply the kernel to the left half of the image
for y in range(height):
    for x in range(width):
        new_pixel = np.zeros(3)
        for ky in range(-kernel_radius_y, kernel_radius_y + 1):
            for kx in range(-kernel_radius_x, kernel_radius_x + 1):
                neighbor_y = y + ky
                neighbor_x = x + kx
                if 0 <= neighbor_y < height and 0 <= neighbor_x < width:
                    new_pixel += img_array[neighbor_y, neighbor_x] * kernel[ky + kernel_radius_y, kx + kernel_radius_x]
        output_array[y, x] = new_pixel

save_image(output_array, 'filtered-kucing.jpg')
combine_images('kucing03.jpeg', 'filtered-kucing.jpg', 'combined.jpg', True)

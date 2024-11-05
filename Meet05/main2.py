from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from tkinter import filedialog
from tkinter import Tk
from scipy.ndimage import label, find_objects

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
    img_array = np.array(image)

    sobel_x = np.array([[-1, 0, 1],
                        [-2, 0, 2],
                        [-1, 0, 1]])

    sobel_y = np.array([[-1, -2, -1],
                        [0,  0,  0],
                        [1,  2,  1]])

    grad_x = apply_convolution(img_array, sobel_x)
    grad_y = apply_convolution(img_array, sobel_y)

    gradient_magnitude = np.sqrt(grad_x ** 2 + grad_y ** 2)
    gradient_magnitude = (gradient_magnitude / np.max(gradient_magnitude)) * 255

    return Image.fromarray(gradient_magnitude.astype(np.uint8))

# Function to apply convolution
def apply_convolution(img, kernel):
    img_height, img_width = img.shape
    output = np.zeros(img.shape)
    for i in range(1, img_height - 1):
        for j in range(1, img_width - 1):
            region = img[i-1:i+2, j-1:j+2]
            output[i, j] = np.sum(region * kernel)
    return output

# Threshold the image to binary (0 and 255)
def threshold_image(image):
    img_array = np.array(image)
    binary = img_array > 128  # Binarize using a threshold
    return binary.astype(np.uint8) * 255  # Convert back to 0-255 scale for visualization

# Find contours and count edges
def count_edges(binary_image):
    labeled_array, num_features = label(binary_image)  # Label connected components
    contours = find_objects(labeled_array)  # Find bounding boxes of components

    edges_count = []
    for contour in contours:
        if contour is not None:
            region = labeled_array[contour]
            # Use the perimeter of each contour to estimate the number of edges
            region_edges = estimate_edges(region)
            edges_count.append(region_edges)
    return edges_count

# Estimate the number of edges by approximating the contour shape
def estimate_edges(region):
    # A simplistic approach to count edges by counting the number of significant changes
    boundary_points = np.where(region > 0)
    points = np.array(list(zip(boundary_points[0], boundary_points[1])))

    if len(points) < 3:  # Not enough points to form a shape
        return 0

    from scipy.spatial import ConvexHull
    hull = ConvexHull(points)
    return len(hull.vertices)  # Number of edges

# Display original and edge-detected images
def display_images_and_result(img1, img2, edge_count):
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    axes[0].imshow(img1, cmap='gray')
    axes[0].set_title('Original Image')
    axes[0].axis('off')

    axes[1].imshow(img2, cmap='gray')
    axes[1].set_title(f'Edge Detected Image\nEdges Detected: {edge_count}')
    axes[1].axis('off')

    plt.show()

# Main function
def main():
    print("Select an image:")
    img_path = select_image()

    img = load_image(img_path)

    # Detect edges using Sobel
    edge_detected_img = sobel_edge_detection(img)

    # Convert to binary for contour detection
    binary_img = threshold_image(edge_detected_img)

    # Count edges in the image
    edges_count = count_edges(binary_img)

    # Display results
    total_edges = sum(edges_count)
    display_images_and_result(img, edge_detected_img, total_edges)
    print(f"Total edges detected: {total_edges}")

# Run the program
if __name__ == "__main__":
    main()

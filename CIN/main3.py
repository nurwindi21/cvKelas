import cv2
import numpy as np
import matplotlib.pyplot as plt

def apply_fourier_transform(image):
    """Applies the Fourier Transform to an image."""
    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply the Fourier Transform
    f_transform = np.fft.fft2(gray_image)
    f_shifted = np.fft.fftshift(f_transform)
    
    return f_shifted

def high_pass_filter(f_transform, cutoff):
    """Applies a high-pass filter to the Fourier transformed image."""
    rows, cols = f_transform.shape
    crow, ccol = rows // 2, cols // 2
    
    # Create a mask with a high-pass filter
    mask = np.ones((rows, cols), np.uint8)
    mask[crow - cutoff:crow + cutoff, ccol - cutoff:ccol + cutoff] = 0
    
    # Apply the mask and inverse Fourier Transform
    f_high_pass = f_transform * mask
    return f_high_pass

def low_pass_filter(f_transform, cutoff):
    """Applies a low-pass filter to the Fourier transformed image."""
    rows, cols = f_transform.shape
    crow, ccol = rows // 2, cols // 2
    
    # Create a mask with a low-pass filter
    mask = np.zeros((rows, cols), np.uint8)
    mask[crow - cutoff:crow + cutoff, ccol - cutoff:ccol + cutoff] = 1
    
    # Apply the mask and inverse Fourier Transform
    f_low_pass = f_transform * mask
    return f_low_pass

def apply_inverse_fourier_transform(f_filtered):
    """Applies the inverse Fourier Transform to a filtered image."""
    f_ishifted = np.fft.ifftshift(f_filtered)
    img_back = np.fft.ifft2(f_ishifted)
    img_back = np.abs(img_back)
    
    return img_back

def display_images(original, high_pass_result, low_pass_result):
    """Displays the original, high-pass filtered, and low-pass filtered images."""
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 3, 1)
    plt.imshow(original, cmap='gray')
    plt.title('Original Image')
    plt.axis('off')

    plt.subplot(1, 3, 2)
    plt.imshow(high_pass_result, cmap='gray')
    plt.title('High-Pass Filtered Image')
    plt.axis('off')

    plt.subplot(1, 3, 3)
    plt.imshow(low_pass_result, cmap='gray')
    plt.title('Low-Pass Filtered Image')
    plt.axis('off')

    plt.show()

def main():
    # Load the image
    image = cv2.imread('kucing03.jpeg')
    
    # Apply Fourier Transform
    f_transform = apply_fourier_transform(image)
    
    # Apply High-Pass Filter
    high_pass_filtered = high_pass_filter(f_transform, cutoff=1)
    high_pass_result = apply_inverse_fourier_transform(high_pass_filtered)

    # Apply Low-Pass Filter
    low_pass_filtered = low_pass_filter(f_transform, cutoff=30)
    low_pass_result = apply_inverse_fourier_transform(low_pass_filtered)
    
    # Display results
    display_images(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), high_pass_result, low_pass_result)

if __name__ == "__main__":
    main()

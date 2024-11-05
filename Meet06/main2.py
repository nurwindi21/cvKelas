import cv2
import numpy as np
import matplotlib.pyplot as plt

# Fungsi untuk menemukan dan menggambar titik fitur (keypoints) menggunakan ORB
def find_keypoints_and_descriptors(image):
    orb = cv2.ORB_create()
    keypoints, descriptors = orb.detectAndCompute(image, None)
    return keypoints, descriptors

# Fungsi untuk menyelaraskan gambar menggunakan RANSAC
def align_images(image1, image2):
    # Temukan keypoints dan descriptors di kedua gambar
    kp1, des1 = find_keypoints_and_descriptors(image1)
    kp2, des2 = find_keypoints_and_descriptors(image2)
    
    # BFMatcher untuk mencocokkan keypoints antara dua gambar
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)
    matches = sorted(matches, key=lambda x: x.distance)
    
    # Ambil keypoints terbaik dari kedua gambar
    src_pts = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
    
    # Gunakan RANSAC untuk menemukan homografi dan menyelaraskan gambar
    H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    
    # Warping gambar
    height, width = image2.shape[:2]
    warped_image1 = cv2.warpPerspective(image1, H, (width + image1.shape[1], height))
    warped_image1[0:image2.shape[0], 0:image2.shape[1]] = image2
    return warped_image1

# Fungsi untuk menyatukan 3 gambar menjadi panorama
def create_panorama(image1, image2, image3):
    # Align gambar pertama dengan yang kedua
    panorama1 = align_images(image1, image2)
    
    # Align hasil panorama dengan gambar ketiga
    panorama = align_images(panorama1, image3)
    
    return panorama

# Fungsi untuk menampilkan gambar panorama
def show_image(image, title='Panorama Image'):
    plt.figure(figsize=(10, 5))
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title(title)
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    # Load gambar
    image1 = cv2.imread('s1.jpg')
    image2 = cv2.imread('s2.jpg')
    image3 = cv2.imread('s3.jpg')
    
    # Buat panorama
    panorama = create_panorama(image1, image2, image3)
    
    # Tampilkan hasil panorama
    show_image(panorama)
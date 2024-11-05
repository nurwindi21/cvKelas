import numpy as np
import cv2
from matplotlib import pyplot as plt

# Load the image and initialize the mask
img = cv2.imread('./tugas/dog.jpg')
mask = np.zeros(img.shape[:2], np.uint8)

# Models for grabCut
bgdModel = np.zeros((1, 65), np.float64)
fgdModel = np.zeros((1, 65), np.float64)

# Define the rectangle around the object and apply grabCut
rect = cv2.selectROI(img)
cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)

# Create mask where background is set to 0 and foreground is 1
mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

# Only the white object on a black background
white_object = np.where(mask2[:, :, np.newaxis] == 1, 255, 0).astype('uint8')

# Extracted object on its original background
extracted_object = img * mask2[:, :, np.newaxis]

# Load the forest background and resize it to match the original image size
background = cv2.imread('./tugas/hutan.jpg')
background = cv2.resize(background, (img.shape[1], img.shape[0]))

# Combine the extracted object with the forest background
combined_img = background * (1 - mask2[:, :, np.newaxis]) + extracted_object

# Display the images
plt.subplot(142), plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title(""), plt.xticks([]), plt.yticks([])

plt.subplot(143), plt.imshow(cv2.cvtColor(extracted_object, cv2.COLOR_BGR2RGB))
plt.title(""), plt.xticks([]), plt.yticks([])

plt.subplot(141), plt.imshow(cv2.cvtColor(white_object, cv2.COLOR_BGR2RGB))
plt.title(""), plt.xticks([]), plt.yticks([])

plt.subplot(144), plt.imshow(cv2.cvtColor(combined_img, cv2.COLOR_BGR2RGB))
plt.title(""), plt.xticks([]), plt.yticks([])

plt.show()

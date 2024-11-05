import cv2
import matplotlib.pyplot as plt
import numpy as np

I = cv2.imread('sakti.png')                                         # load image I (BGR format)
I = cv2.cvtColor(I, cv2.COLOR_BGR2RGB)/255                         # convert to RGB and normalize
plt.imshow(I), plt.axis('off')                                     # plot I
plt.show();
alpha_ex = cv2.imread('sakti_alpha.png', cv2.IMREAD_GRAYSCALE)/255  # load exact alpha and normalize
plt.imshow(alpha_ex, cmap='gray'), plt.axis('off')                 # plot alpha
plt.show();
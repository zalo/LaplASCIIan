import numpy as np
import cv2
import math

laplacian = False
density = 5
font_size_x = 8
blur = 1 # must be odd

# Load the original image
oimg = cv2.imread("image.jpg")
oimg = cv2.resize(oimg, (1080, int(oimg.shape[0] *(1080/oimg.shape[1]))))
oimg = cv2.cvtColor(oimg, cv2.COLOR_BGR2GRAY)
img = cv2.GaussianBlur(oimg, (5, 5), 0)

img = cv2.bilateralFilter(img, 5, 20, 20)
img = cv2.Laplacian(img, cv2.CV_8U)
img = cv2.bilateralFilter(img, 5, 200, 200)
#img = cv2.medianBlur(img, 9)

#img = cv2.GaussianBlur(img, (5, 5), 0)
img = cv2.normalize(img, img, 255, 0, cv2.NORM_MINMAX)
img = img.astype(np.float) * (density / 255)

finalImage = np.zeros(img.shape, dtype=np.uint8)

# Specify the font to create
asciiCharacters = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
font_size_y = int(font_size_x * 1.5)

asciiAtlas     = np.zeros((len(asciiCharacters), font_size_y, font_size_x), dtype=np.uint8)
laplacianAtlas = np.zeros(asciiAtlas.shape, dtype=np.uint8)
for i in range(len(asciiCharacters)):
  cv2.putText(asciiAtlas[i], asciiCharacters[i], (int(font_size_x*0.2), font_size_x), cv2.FONT_HERSHEY_SIMPLEX, font_size_x/40, (255,255,255), 0, 0) #cv2.LINE_AA
  laplacianAtlas[i] = cv2.Laplacian(asciiAtlas[i], cv2.CV_8U) if laplacian else np.copy(asciiAtlas[i])
  laplacianAtlas[i] = cv2.GaussianBlur(laplacianAtlas[i], (3, 3), 0)
  laplacianAtlas[i] = laplacianAtlas[i].astype(np.float)
  cv2.normalize(laplacianAtlas[i], laplacianAtlas[i], 255, 0, cv2.NORM_MINMAX)

# Extract patches...
for y in range(int(img.shape[0] / font_size_y)):
  for x in range(int(img.shape[1] / font_size_x)):
    imgSlice = img[y * font_size_y : (y + 1) * font_size_y, x * font_size_x : (x + 1) * font_size_x]
    
    # Broadcast imgSlice to the font array size...
    alphabetSubtractions = np.abs((laplacianAtlas/255) - imgSlice)
    alphabetSimilarities = np.sum(alphabetSubtractions, axis=(1, 2))
    minIndex             = np.argmin(alphabetSimilarities)

    finalImage[y * font_size_y : (y + 1) * font_size_y, x * font_size_x : (x + 1) * font_size_x] = asciiAtlas[minIndex]

# Display finished images...
cv2.imshow("Original Image", oimg)
cv2.imshow("Original Image", img)
cv2.imshow("ASCII Atlas", laplacianAtlas[56])
cv2.imshow("ASCII Image", finalImage)
cv2.waitKey(0)
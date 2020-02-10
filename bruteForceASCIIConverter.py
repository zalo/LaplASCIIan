import numpy as np
import cv2
import pyperclip
from PIL import ImageFont, ImageDraw, Image

laplacian = True
density = 17
font_size_y = 18
blur = 5 # Must Be Odd

# Load the original image
oimg = cv2.imread("image.jpg")
oimg = cv2.resize(oimg, (720, int(oimg.shape[0] *(720/oimg.shape[1]))))
oimg = cv2.cvtColor(oimg, cv2.COLOR_BGR2GRAY)

# These settings also control the fidelity of the output image...
img = cv2.GaussianBlur(oimg, (blur, blur), 0)
img = cv2.bilateralFilter(img, blur, 20, 20)
img = cv2.Laplacian(img, cv2.CV_8U)
img = cv2.bilateralFilter(img, blur, 200, 200)

img = cv2.normalize(img, img, 255, 0, cv2.NORM_MINMAX)
img = img.astype(np.float) * (density / 255)

finalImage = np.zeros(img.shape, dtype=np.uint8)

# Specify the font to create
asciiCharacters = " !\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~" #0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz
font_size_x = int(font_size_y * 0.45)
consolas = ImageFont.truetype("./Consolas.ttf", int(font_size_y*0.8))

asciiAtlas     = np.zeros((len(asciiCharacters), font_size_y, font_size_x), dtype=np.uint8)
laplacianAtlas = np.zeros(asciiAtlas.shape, dtype=np.uint8)
for i in range(len(asciiCharacters)):
  # Make into PIL Image
  im_p = Image.fromarray(asciiAtlas[i])
  draw = ImageDraw.Draw(im_p)
  draw.text((0, 3), asciiCharacters[i], (255), font=consolas)
  asciiAtlas[i] = np.array(im_p)

  laplacianAtlas[i] = cv2.Laplacian(asciiAtlas[i], cv2.CV_8U) if laplacian else np.copy(asciiAtlas[i])
  laplacianAtlas[i] = cv2.GaussianBlur(laplacianAtlas[i], (3, 3), 0)
  laplacianAtlas[i] = laplacianAtlas[i].astype(np.float)
  cv2.normalize(laplacianAtlas[i], laplacianAtlas[i], 255, 0, cv2.NORM_MINMAX)

# Construct string...
outputArt = ''
for y in range(int(img.shape[0] / font_size_y)):
  for x in range(int(img.shape[1] / font_size_x)):
    imgSlice = img[y * font_size_y : (y + 1) * font_size_y, x * font_size_x : (x + 1) * font_size_x]
    
    # Broadcast imgSlice to the font array size...
    alphabetSubtractions = np.abs((laplacianAtlas/255) - imgSlice)
    alphabetSimilarities = np.sum(alphabetSubtractions, axis=(1, 2))
    minIndex             = np.argmin(alphabetSimilarities)

    finalImage[y * font_size_y : (y + 1) * font_size_y, x * font_size_x : (x + 1) * font_size_x] = asciiAtlas[minIndex]
    outputArt += asciiCharacters[minIndex]
  outputArt += '\r\n'

# Copy ASCII Art to clipboard
pyperclip.copy(outputArt)

# Display finished images...
cv2.imshow("Original Image", oimg)
cv2.imshow("Processed Image", img)
cv2.imshow("ASCII Atlas", laplacianAtlas[33])
cv2.imshow("ASCII Image", finalImage)
cv2.waitKey(0)
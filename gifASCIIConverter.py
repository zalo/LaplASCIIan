import numpy as np
import cv2
from PIL import ImageFont, ImageDraw, Image
import imageio
import codecs

laplacian = False
alphanumerics = False
density = 25
font_size_y = 20
blur = 5 # Must Be Odd

# Specify the font to create
asciiCharacters = " !\"'*+,-./:;=\^_`|~"
if alphanumerics:
  asciiCharacters += "?#$%&@0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz()[]]{}" #<> # SVG Incompatible...
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
  #laplacianAtlas[i] = cv2.GaussianBlur(laplacianAtlas[i], (3, 3), 0)
  laplacianAtlas[i] = laplacianAtlas[i].astype(np.float)
  cv2.normalize(laplacianAtlas[i], laplacianAtlas[i], 255, 0, cv2.NORM_MINMAX)

# Load the original image
im = imageio.mimread(imageio.core.urlopen('https://upload.wikimedia.org/wikipedia/commons/2/2c/Rotating_earth_%28large%29.gif').read(), '.gif')

index = 0
curImage = im[0]

asciiFrames = []

while (not ((cv2.waitKey(1) & 0xFF == ord('q')) or (index is len(im)-1))):
  # Take all indices that don't equal zero and composite them onto the current image (HACK)
  #mask = im[index] != 0
  #curImage[mask] = im[index][mask]
  curImage = im[index]

  # Convert To Gray
  oimg = cv2.cvtColor(curImage, cv2.COLOR_BGR2GRAY)

  # These settings also control the fidelity of the output image...
  img = cv2.GaussianBlur(oimg, (blur, blur), 0)
  img = cv2.bilateralFilter(img, blur, 20, 20)
  img = cv2.Laplacian(img, cv2.CV_8U)
  img = cv2.bilateralFilter(img, blur, 200, 200)
  img = cv2.normalize(img, img, 255, 0, cv2.NORM_MINMAX)
  img = img.astype(np.float) * (density / 255)

  finalImage = np.zeros(img.shape, dtype=np.uint8)

  # Construct a frame's string...
  outputArt = '  <text id="Frame-'+str(index)+'" font-family="monospace" visibility="hidden">\r\n'
  for y in range(int(img.shape[0] / font_size_y)):
    outputArt += '    <tspan dy="1.2em" x="0">'
    for x in range(int(img.shape[1] / font_size_x)):
      imgSlice = img[y * font_size_y : (y + 1) * font_size_y, x * font_size_x : (x + 1) * font_size_x]
      
      # Broadcast imgSlice to the font array size...
      alphabetSubtractions = np.abs((laplacianAtlas/255) - imgSlice)
      alphabetSimilarities = np.sum(alphabetSubtractions, axis=(1, 2))
      minIndex             = np.argmin(alphabetSimilarities)

      finalImage[y * font_size_y : (y + 1) * font_size_y, x * font_size_x : (x + 1) * font_size_x] = asciiAtlas[minIndex]
      outputArt += asciiCharacters[minIndex]
    outputArt += '</tspan>\r\n'
  outputArt += '  </text>\r\n'

  # Append the ASCII Frame to the List...
  asciiFrames.append(outputArt)

  # Display finished images...
  cv2.imshow("Original Image", oimg)
  cv2.imshow("Processed Image", img)
  cv2.imshow("ASCII Image", finalImage)

  # Increment to the next frame
  index = (index+1) % len(im)

# Begin Constructing the Animated SVG

# Create the Header and skeleton structure
svgBody = '<?xml version="1.0" encoding="utf-8"?>\r\n<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="'+str(im[0].shape[1])+'" height="'+str(im[0].shape[0])+'">\r\n'

# Create the frames...
for frame in asciiFrames:
  svgBody += frame

# Create the CSS Instructions for flashing frames
svgBody += '  <style type="text/css">\r\n    @keyframes flash { 0%                   { visibility: visible; }\r\n                       '+str(100.0/len(asciiFrames))+'%  { visibility: hidden;  } }\r\n'

frameTime = 0.03333
animationTime = frameTime * len(asciiFrames)
for frame in range(len(asciiFrames)):
  svgBody += '    #Frame-'+str(frame)+' { animation: flash '+str(animationTime)+'s linear infinite ' + str(frameTime * frame) + 's;   }\r\n'

svgBody += '  </style>\r\n</svg>'

# Finish it up!
svgFile = codecs.open("output.svg","w", "utf-8") 
svgFile.write(svgBody) 
svgFile.close()

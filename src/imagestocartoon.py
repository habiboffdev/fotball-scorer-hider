import cv2
import glob
from pathlib import Path
import os
import numpy as np

class Cartoonizer: 
    """Cartoonizer effect 
    Creates a sketchy black and white style for football videos that masks player 
    identities but keeps the action visible.
    """
    def __init__(self): 
        pass
  
    def render(self, img_path): 
        # Load and downsize the image a bit
        img_rgb = cv2.imread(img_path)
        img_rgb = cv2.resize(img_rgb, (int(img_rgb.shape[1]/1.5), int(img_rgb.shape[0]/1.5)))
        
        # Work with grayscale
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        
        # Smooth the image but keep edges sharp
        smoothed = cv2.bilateralFilter(img_gray, 9, 75, 75)
        
        # Find edges in the image
        edges = cv2.Canny(smoothed, threshold1=20, threshold2=60)
        
        # Make the edges a bit thicker
        kernel = np.ones((2, 2), np.uint8)
        edges = cv2.dilate(edges, kernel, iterations=1)
        
        # Flip the edge mask
        edges_inv = 255 - edges
        
        # Create the base stylized image
        thresh = cv2.adaptiveThreshold(
            smoothed, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 11, 1
        )
        
        # Keep a copy for later
        base = thresh.copy()
        
        # Combine the stylized image with edge details
        result = cv2.bitwise_and(base, edges_inv)
        
        # Boost the contrast
        result = cv2.equalizeHist(result)
        
        # Back to color format for saving
        cartoonized = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)
        
        return cartoonized

# Test code (uncomment to use)
# canvas = Cartoonizer()
# folder = os.path.dirname(os.path.abspath(__file__))
# folder = os.path.join(folder, "images")
# folder = Path(folder)
# frames = sorted(glob.glob(str(folder / '*.jpg')))

# output = os.path.dirname(os.path.abspath(__file__))
# output = os.path.join(output, "output")
# output = Path(output)

# os.mkdir(output)
# for frame in frames:
#   print(frame)
#   cartoon = canvas.render(frame)
#   cv2.imwrite(str(output / Path(frame).name)+".png", cartoon)

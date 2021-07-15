import cv2
import numpy as np
import os
from pylsd import lsd
    

def green(img, pt1):
    T = 1.2 # Threshold described on article

    # Obtaining the rgb pixel of the image
    # given the point
    rgb = img[pt1[1]][pt1[0]]

    if (2*rgb[1]/(rgb[0]+rgb[2]+1) > T) and rgb[1] > rgb[0] and rgb[1] > rgb[2]: # sum +1 at the divisor to avoid division by 0
        return 1
    else:
        return 0

full_name = "0.png"
# Separa os diretórios do arquivo
folder, img_name = os.path.split(full_name)
# cv2.IMREAD_COLOR = 1
# Seta a image como sendo rgb tendo 3 canais
img = cv2.imread(full_name, cv2.IMREAD_COLOR)
# Transformando a imagem de RGB para grayscale images
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

segments = lsd(img_gray) # Retorna os segmentos de reta.



for i in range(segments.shape[0]):
    pt1 = (int(segments[i, 0]), int(segments[i, 1]))
    pt2 = (int(segments[i, 2]), int(segments[i, 3]))
    is_green1 = green(img, pt1)
    is_green2 = green(img, pt2)
    #import pdb; breakpoint()
    width = segments[i, 4]
    if is_green1 or is_green2:
        cv2.line(img, pt1, pt2, (0, 255, 0), int(np.ceil(width / 2))) # Red Lines
    else:
        cv2.line(img, pt1, pt2, (0, 0, 255), int(np.ceil(width / 2))) # Red Lines
    
"""
cv2.imshow('imagem',img)
cv2.waitKey(0)
cv2.destroyAllWindows() 
"""
cv2.imwrite(os.path.join(folder, 'cv2_' + img_name.split('.')[0] + '.jpg'), img)

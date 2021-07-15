import cv2
import numpy as np
import os
from pylsd import lsd

def calculate_angle(point1, point2):
    # Calculando o angulo utilizando arc tan
    angle = np.arctan2(point1[0]-point2[0],point1[1]-point2[1])

    return angle*180/np.pi # convertendo para graus e retornando
    
def calculate_length(img, point1, point2):
    # Obtaning the size of the diagonal
    xsqr = np.power(img.shape[0])
    ysqr = np.power(img.shape[1])
    diagonal = np.sqrt(xsqr + ysqr)
    # Obtaining the length of the segment
    x_line = np.power(abs(point1[0] - point2[0]), 2)
    y_line = np.power(abs(point1[1] - point2[1]), 2)
    length_line = np.sqrt(x_line + y_line)

    return length_line/diagonal

full_name = "309.png"
# Separa os diretórios do arquivo
folder, img_name = os.path.split(full_name)
# cv2.IMREAD_COLOR = 1
# Seta a image como sendo rgb tendo 3 canais
img = cv2.imread(full_name, cv2.IMREAD_COLOR)
# Transformando a imagem de RGB para grayscale images
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

quarter = img_gray.shape[0]/3

# Aplicando o metodo lsd
"""
scales = [0.1, 0.5, 0.9]
for scale in scales:
    segments = lsd(img_gray, scale=scale) # Retorna os segmentos de reta.

    for i in range(segments.shape[0]):
        pt1 = (int(segments[i, 0]), int(segments[i, 1]))
        pt2 = (int(segments[i, 2]), int(segments[i, 3]))
        width = segments[i, 4]
        cv2.line(img, pt1, pt2, (0, 0, 255), int(np.ceil(width / 2)))

    cv2.imwrite(os.path.join(folder, 'cv2_' +str(scale) + img_name.split('.')[0] + '.jpg'), img)
"""
segments = lsd(img_gray) # Retorna os segmentos de reta.

new_segment = [] # Storage the valids segments

for i in range(segments.shape[0]):
    pt1 = (int(segments[i, 0]), int(segments[i, 1]))
    pt2 = (int(segments[i, 2]), int(segments[i, 3]))
    calculate_angle(pt1, pt2)

    width = segments[i, 4]
    #cv2.line(img, pt1, pt2, (0, 0, 255), int(np.ceil(width / 2)))
    angle = calculate_angle(pt1, pt2)
    
    if (abs(angle) > 87 and abs(angle) < 93) or abs(angle) < 3 or abs(angle) > 177: # Pratically horizontal or vertical lines
        #cv2.line(img, pt1, pt2, (0, 255, 0), int(np.ceil(width / 2))) # Green lines
        continue
    elif quarter > pt1[1] or quarter > pt2[1]:
        continue
        #cv2.line(img, pt1, pt2, (255, 0, 0), int(np.ceil(width / 2))) # Green lines
    else:
        new_segment.append([pt1, pt2])
        #cv2.line(img, pt1, pt2, (0, 0, 255), int(np.ceil(width / 2))) # Red Lines

for segment in new_segment:
    #import pdb;breakpoint()
    cv2.line(img, segment[0], segment[1 ], (0, 0, 255), int(np.ceil(width / 2))) # Red Lines

"""
for i in range(new_segment.shape[0]):
    pt1 = (int(new_segment[i, 0]), int(new_segment[i, 1]))
    pt2 = (int(new_segment[i, 2]), int(new_segment[i, 3]))
    cv2.line(img, pt1, pt2, (0, 0, 255), int(np.ceil(width / 2))) # Red Lines
"""

"""
cv2.imshow('imagem',img)
cv2.waitKey(0)
cv2.destroyAllWindows() 
"""
cv2.imwrite(os.path.join(folder, 'cv2_' + img_name.split('.')[0] + '.jpg'), img)

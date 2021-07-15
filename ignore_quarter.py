import cv2
import numpy as np
import os
from pylsd import lsd

def calculate_angle(point1, point2):
    # Calculando o angulo utilizando arc tan
    angle = np.arctan2(point1[0]-point2[0],point1[1]-point2[1])

    return angle*180/np.pi # convertendo para graus e retornando
    
    

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

for i in range(segments.shape[0]):
    pt1 = (int(segments[i, 0]), int(segments[i, 1]))
    pt2 = (int(segments[i, 2]), int(segments[i, 3]))
    calculate_angle(pt1, pt2)
    #   import pdb; breakpoint()
    width = segments[i, 4]
    #cv2.line(img, pt1, pt2, (0, 0, 255), int(np.ceil(width / 2)))
    angle = calculate_angle(pt1, pt2)
    if (abs(angle) > 87 and abs(angle) < 93) or abs(angle) < 3 or abs(angle) > 177: # Pratically horizontal or vertical lines
        cv2.line(img, pt1, pt2, (0, 255, 0), int(np.ceil(width / 2))) # Green lines
    elif quarter > pt1[1] or quarter > pt2[1]:
        cv2.line(img, pt1, pt2, (255, 0, 0), int(np.ceil(width / 2))) # Green lines
    else:
        cv2.line(img, pt1, pt2, (0, 0, 255), int(np.ceil(width / 2))) # Red Lines
"""
cv2.imshow('imagem',img)
cv2.waitKey(0)
cv2.destroyAllWindows() 
"""
cv2.imwrite(os.path.join(folder, 'cv2_' + img_name.split('.')[0] + '.jpg'), img)

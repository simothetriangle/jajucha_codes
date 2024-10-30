NAME = 'main_data' #모델의 이름을 입력합니다 예시: '12'import jajucha2

import jajucha2
import torch
import numpy as np
import torchvision.transforms as transforms
from PIL import Image as Img
import cv2

transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
    ])

device = torch.device('cuda')
model = jajucha2.ai.get_model(NAME)
model.to(device)
model.eval()

steer = 0
speed = 0

def evt1 ():
    return 0

while True:
    image = jajucha2.camera.get_image('center')
    jajucha2.camera.show_image(image)

    #그리드 기반 주행 코드
    (V,L,R) ,grid = jajucha2.camera.gridFront(image)

    if(V[5] < 100):
        steer = -10
        speed = 5
    else:
        steer = 0
        speed = 5
        
    print(f"\r grid result {speed},{steer}", end="")

    #깊이기반 거리감지 주행
    depth = jajucha2.camera.get_depth() 
    jajucha2.camera.show_image(depth, 'depth')  
    height, width = depth.shape[:2]
    center_x, center_y = width // 2, height // 2
    region_size = 60
    start_x = center_x - region_size // 2  
    start_y = center_y - region_size // 2  
    center_region = depth[start_y:start_y + region_size, start_x:start_x + region_size]
    mean_value = np.mean(center_region)
    if(mean_value > 100):
        speed = 0

    print(f"\r depth result {speed},{steer}", end="")

    # 인공지능 기반 신호등 감지
    image = Img.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)) 
    image = transform(image)  
    image =image.unsqueeze(0).to(device)
    output = (model(image))
    max_index = torch.argmax(output)
    if(max_index == 1):
        speed = 0

    print(f"\r final result {speed},{steer}", end="")
    
    jajucha2.control.set_motor(steer,steer,speed)
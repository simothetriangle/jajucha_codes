NAME = 'resnet_epoch_4.pt'
#------
import jajucha2
import torch
import numpy as np
import torchvision.transforms as transforms
from PIL import Image as Img
import cv2
import time
#------
transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
    ])

device = torch.device('cuda')
model = jajucha2.ai.get_model(NAME)
model.to(device)
model.eval()

speed_or = 8
speed_cu = 5
steer_or = 9

steer_f = 0
speed_f = 0

chk_rl = 0
chk_lt = 0
lastR = 320
lastL = 320

chk_e1 = 0
ehk_e2 = 0
chk_e3 = 0
#------
def sumA(arr):
    Asum = 0
    cnt = 0
    while cnt < len(arr):
        Asum += arr[cnt]
        cnt += 1
    
    return Asum

def find_arr_range(arr, max_ran):
    arr_s = -1
    arr_f = -1
    h = 0
    
    cnt = 0
    while cnt < len(arr):
        if h == 0:
            if arr[cnt] < max_ran:
                arr_s = cnt
        elif h == 1:
            if arr[cnt] >= max_ran:
                arr_f = cnt
        cnt += 1
    
    return arr_s, arr_f

def evt1 ():
    return 0
#------
while True:
    #그리드 기반 자율주행 0: 직진 1: 오른쪽 2: 왼쪽
    image = jajucha2.camera.get_image()
    (V, L, R), grid = jajucha2.camera.gridFront(image)
    jajucha2.camera.show_image(grid)

    Lsum = sumA(L) - L[0]
    Rsum = sumA(R) - R[0]
    lV, hV = fin_arr_range(V ,170)
    
    if chk_lt == 0:
        if Lsum < Rsum and Rsum - Lsum > 70:
            steer_f = steer_or
            speed_f = speed_cu
        elif Lsum > Rsum and Lsum - Rsum > 70:
            steer_f = -steer_or
            speed_f = speed_cu
        else:
            steer_f = 0
            speed_f = speed_or

        if lastL < 30 and L[1] > lastL + 50 and R[1] < 50:
            chk_lt = 1
            steer_f = steer_or
            speed_f = speed_cu
        elif lastR < 30 and R[1] > lastR + 50 and L[1] < 50:
            chk_lt = 2
            steer_f = -steer_or
            speed_f = speed_cu
    elif chk_lt == 1:
        if lastL > L[1]:
            chk_lt = 0
            steer_f = 0
            speed_f = speed_or
        else:
            steer_f = steer_or
            speed_f = speed_cu
    else:
        if lastR > R[1]:
            chk_lt = 0
            steer_f = 0
            speed_f = speed_or
        else:
            steer_f = -steer_or
            speed_f = speed_cu

    lastR = R[1]
    lastL = L[1]
        
    print(f"\r grid result {speed_f}, {steer_f}")

    #깊이 기반 자율주행
    depth = jajucha2.camera.get_depth() 
    jajucha2.camera.show_image(depth, 'depth')  
    height, width = depth.shape[:2]

    side_gap = width // 4
    center_x, center_y = width // 2, height // 2
    lef_x, lef_y = center_x - side_gap, center_y
    rig_x, rig_y = center_x + side_gap, center_y
    region_size = 60
    
    start_cx = center_x - region_size // 2  
    start_cy = center_y - region_size // 2  
    cen_region = depth[start_cy:start_cy + region_size, start_cx:start_cx + region_size]

    start_lx = lef_x - region_size // 2  
    start_ly = lef_y - region_size // 2  
    lef_region = depth[start_ly:start_ly + region_size, start_lx:start_lx + region_size]

    start_rx = rig_x - region_size // 2  
    start_ry = rig_y - region_size // 2  
    rig_region = depth[start_ry:start_ry + region_size, start_rx:start_rx + region_size]
    
    cen_value = np.mean(cen_region)
    lef_value = np.mean(lef_region)
    rig_value = np.mean(rig_region)

    if cen_value > 191:
        speed_f = -3
        steer_f = 0
    elif cen_value > 127:
        if rig_value < 80 and R[1] > 280 and R[1] <= R[2]:
            speed_f = speed_cu
            steer_f = steer_or
        elif lef_value < 80 and L[1] > 280 and L[1] <= L[2]:
            speed_f = speed_cu
            steer_f = -steer_or
        else:
            speed_f = -3
            steer_f = 0

    print(f"\r depth result {speed_f}, {steer_f}")

    # 인공지능 기반 자율주행
    image = Img.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)) 
    image = transform(image)  
    image = image.unsqueeze(0).to(device)
    
    output = (model(image))
    max_index = torch.argmax(output)
    
    if max_index == 'r':
        speed_f = 0

    print(f"\r AI result {speed_f}, {steer_f}")
        
    #이벤트 감지기반 예외 탐지
    if(evt1() == 1):
        a = evt1()

    print(f"\r event result {speed_f}, {steer_f}")

    #종합 결과
    print(f"\r final result {speed_f}, {steer_f}\n")
    
    jajucha2.control.set_motor(steer_f, steer_f , speed_f)

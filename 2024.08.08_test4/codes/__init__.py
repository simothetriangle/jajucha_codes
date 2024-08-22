 #자주차 기본 동작코드
from control import Jajucha
import cv2

speedOrig = 55
speedTurn = 53

def Fevt_2(V, L, R): #evt_2 - line tracing
    #returns 1 - 30, 30 / 2 - 60, 60
    #exception1_RoverL or LoverR -> chk V -> chk LR
    sV_e2 = 0
    eV_e2 = 0

    #exc1 - chk RL over
    hEx1_e2 = 0
    if R[0] > R[1] or R[1] > R[2]:
        hEx1_e2 += 1
    if L[0] > L[1] or L[1] > L[2]:
        hEx1_e2 -= 1

    if hEx1_e2 != 0:
        print("exc1")
        return 2 if hEx1_e2 > 0 else 1
        

    #exc2 - chk mid_axis
    hEx2_e2 = 0
    for ni in range(4):
        Vcntlimit = ni*43 + 42
        
        hEx2_e2 = 0
        for ni in range(7):
            if(hEx2_e2 == 0):
                if(V[ni] >= Vcntlimit):
                    hEx2_e2 = 1
                    sV_e2 = ni
            elif(hEx2_e2 == 1):
                if(V[ni] < Vcntlimit):
                    hEx2_e2 = 2
                    eV_e2 = ni
        
        mid_axis = (sV_e2 + eV_e2) / 2
        if mid_axis != 3 and hEx2_e2 != 0 and mid_axis >= 1.5:
            print("exc2 " , mid_axis)
            return 1 if mid_axis < 3 else 2

    #chk V
    for ni in range(4):
        if ni > 1:
            hcntV_e2 = 2
        else: 
            hcntV_e2 = 3 
        for nj in range(hcntV_e2):
            hV_e2 = 0
            Vcntlim_Min = (3-ni)*43
            Vcntlim_Max = Vcntlim_Min + 42

            if V[ni] >= Vcntlim_Min and V[ni] < Vcntlim_Max:
                hV_e2 += 1
            if V[6-ni] >= Vcntlim_Min and V[6-ni] < Vcntlim_Max:
                hV_e2 -= 1

            if hV_e2 != 0:
                print("V")
                return 2 if hV_e2 > 0 else 1

    #chk LR 
    '''for ni in range(3):
        for nj in range(4):
            hLR_e2 = 0
            LRcntlim_Min = nj*80
            LRcntlim_Max = LRcntlim_Min + 79

            if L[2-ni] >= LRcntlim_Min and L[2-ni] < LRcntlim_Max:
                hLR_e2 += 1
            if R[2-ni] >= LRcntlim_Min and R[2-ni] < LRcntlim_Max:
                hLR_e2 -= 1
            
        if hLR_e2 != 0:
            print("LR")
            return 2 if hLR_e2 > 0 else 1
         '''
    return 0

def main_loop():
    qrgb,qdepth = jajucha.camera_init() #카메라 인스턴스 가져오기
    while True: 
        rgb = jajucha.image_get(qrgb) #RGB 이미지 가져오기
        (V,L,R), image = jajucha.gridFront(rgb)
        
        jajucha.image_send('V[0]'+" "+'V[1]'+" "+'V[2]'+" "+'V[3]'+" "+'V[4]'+" "+'V[5]'+" "+'V[6]')
        evt_2 = Fevt_2(V, L, R)
        

        if (evt_2 != 0):
            if (evt_2 == 1):
                jajucha.control(35, 35, speedTurn)
            elif (evt_2 == 2):
                jajucha.control(55, 55, speedTurn)
        else:
            jajucha.control(45,45,speedOrig) 
            
        jajucha.image_send(rgb) #이미지를 PC로 전송
if __name__ == "__main__":
    jajucha = Jajucha() #자주차 객체선언
    jajucha.control(45,45,50) #정지
    main_loop() #메인함수
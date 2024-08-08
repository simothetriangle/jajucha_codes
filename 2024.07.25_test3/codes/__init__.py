 #자주차 기본 동작코드
from control import Jajucha
import cv2


def Fevt_1(distance): #evt_1 - scan obstacles
    if(distance > 60):
            return 1
        else:
            return 0

def Fevt_2(V, L, R): #evt_2 - line tracing
    #exception1_RoverL or LoverR -> chk V -> chk LR
    sV_e2 = 0
    eV_e2 = 0

    #exc1 - chk RL over
    hEx1_e2 = 0
    if(R[0] > R[1] || R[1] > R[2]):
        hEx1_e2 += 1
    if(L[0] < L[1] || L[1] < L[2]):
        hEx1_e2 -= 1

    if(hEx1_e2 == 1):
        return 2
    elif(hEx1_e2 == -1):
        return 1
        

    #exc2 - chk mid_axis
    hEx2_e2 = 0
    for ni in range(4):
        Vcntlimit = ni*43 + 42

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
        if(mid_axis != 3):
            if(mid_axis < 3):
                return 2
            else:
                return 1

    #chk V
    for ni in range(3):
        for nj in range(4):
            hV_e2 = 0
            cntlim_Min = nj*43
            cntlim_Max = cntlim_Min + 42

            if(V[ni] >= cntlim_Min && V[ni] < cntlim_Max):
                hV_e2 += 1
            if(V[6-ni] >= cntlim_Min && V[6-ni] < cntlim_Max):
                hV_e2 -= 1

            if(hEx1_e2 == 1):
                return 2
            elif(hEx1_e2 == -1):
                return 1

    #chk LR <-- 수정 필요 (jajucha.control -> return, 각각 수치 변경)
    if(L[2] == R[2]):
            if(L[2]  < 320):
                return 1
            else:
                return 2
        elif(L[2] != R[2] and (L[2] < 160 or R[2] < 160)):
            if(L[2] - R[2] < 0):
                return 2
            else:
                return 1
        elif(L[1] != R[1] and (L[1] < 160 or R[1] < 160)):
            if(L[1] - R[1] < 0):
                return 2
            else:
                return 1
        elif(L[0] != R[0] and (L[0] < 160 or R[0] < 160)):
            if(L[0] - R[0] < 0):
                return 2
            else:
                return 1
        else:
            return 0


def main_loop():
    #set variables
    evt_1 = 0
    evt_2 = 0
    
    #get instance
    qrgb,qdepth = jajucha.camera_init()

    while True: 
        #instance load
        rgb = jajucha.image_get(qrgb)
        (V,L,R), image = jajucha.gridFront(rgb)
        depth = jajucha.image_get(qdepth)
        distance = jajucha.distance_get(depth)
        
        #Events
        print(distance)
        evt_1 = Fevt_1(distance)
        
        jajucha.image_send('V[0]'+" "+'V[1]'+" "+'V[2]'+" "+'V[3]'+" "+'V[4]'+" "+'V[5]'+" "+'V[6]');
        evt_2 = Fevt_2(V, L, R)
        


        #movement
        if (evt_1 != 0):
            if (evt_1 == 1):
                jajucha.control(45, 45, 50)
        elif (evt_2 != 0):
            if (evt_2 == 1):
                jajucha.control(30, 30, speedTurn)
            elif (evt_2 == 2):
                jajucha.control(60, 60, speedTurn)
        else:
            jajucha.control(45,45,speedOrig)


        jajucha.image_send(depth) #이미지를 PC로 전송
      
if __name__ == "__main__":
    jajucha = Jajucha() #자주차 객체선언
    jajucha.control(45, 45, 50) #정지
    main_loop() #메인함수

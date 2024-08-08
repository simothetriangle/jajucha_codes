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

    h_e2 = 0;
    for ni in range(4):
        Vcntlimit = ni*43 + 42

        for ni in range(7):
            if(h == 0):
                if(V[ni] >= Vcntlimit):
                    h_e2 = 1
                    sV_e2 = ni
            else:
                if(V[ni] < Vcntlimit):
                    h_e2 = 2
                    eV_e2 = ni
    
        if((sV_e2 + eV_e2) / 2 != 3):
            if((sV_e2 + eV_e2) / 2 < 3):
                return 2
            else:
                return 1




    """
    Vcntlimit = 171
    sV_e2 = 0
    eV_e2 = 0

    h_e2 = 0
    for ni in range(7):
        if(h == 0):
            if(V[ni] >= Vcntlimit):
                h_e2 = 1
                sV_e2 = ni
        else:
            if(V[ni] < Vcntlimit):
                h_e2 = 2
                eV_e2 = ni
        
    #
    if(R[0] > R[1] || R[1] > R[2]):
        #

    if(L[0] < L[1] || L[1] < L[2]):
        #

    if((sV_e2 + eV_e2) / 2 != 3): #check vertical nums
        if((sV_e2 + eV_e2) / 2 > 3):
            evt_2 = 1
        else:
            evt_2 = 2
    else: #check horizental nums
        if(L[2] == R[2]):
            if(L[2]  < 320):
                evt_2 = 1
            else:
                evt_2 = 2
        elif(L[2] != R[2] and (L[2] < 160 or R[2] < 160)):
            if(L[2] - R[2] < 0):
                evt_2 = 2
            else:
                evt_2 = 1
        elif(L[1] != R[1] and (L[1] < 150 or R[1] < 150)):
            if(L[1] - R[1] < 0):
                evt_2 = 2
            else:
                evt_2 = 1
        elif(L[0] != R[0] and (L[0] < 140 or R[0] < 140)):
            if(L[0] - R[0] < 0):
                evt_2 = 2
            else:
                evt_2 = 1
        else:
            evt_2 = 0
    """

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

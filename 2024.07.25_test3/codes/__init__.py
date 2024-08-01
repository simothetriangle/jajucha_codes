 #자주차 기본 동작코드
from control import Jajucha
import cv2



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
        #evt_1 - scan obstacles
        print(distance)

        if(distance > 60):
            evt_1 = 1
        else:
            evt_1 = 0
            

        #evt_2 - line tracing
        jajucha.image_send('V[0]'+" "+'V[1]'+" "+'V[2]'+" "+'V[3]'+" "+'V[4]'+" "+'V[5]'+" "+'V[6]');
        
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
        elif(L[1] != R[1] and (L[1] < 160 or R[1] < 160)):
            if(L[1] - R[1] < 0):
                evt_2 = 2
            else:
                evt_2 = 1
        elif(L[0] != R[0] and (L[0] < 160 or R[0] < 160)):
            if(L[0] - R[0] < 0):
                evt_2 = 2
            else:
                evt_2 = 1
        else:
            evt_2 = 0


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
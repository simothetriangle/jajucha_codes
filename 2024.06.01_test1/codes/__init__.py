 #자주차 기본 동작코드
from control import Jajucha
import cv2

speedOrig = 58
speedTurn = speedOrig - 3

def main_loop():
    qrgb,qdepth = jajucha.camera_init() #카메라 인스턴스 가져오기
    while True: 
        rgb = jajucha.image_get(qrgb) #RGB 이미지 가져오기
        (V,L,R), image = jajucha.gridFront(rgb)
        
        jajucha.image_send('V[0]'+" "+'V[1]'+" "+'V[2]'+" "+'V[3]'+" "+'V[4]'+" "+'V[5]'+" "+'V[6]');

        #Example
        if(L[2] == R[2]):
            if(L[2]  < 320):
                jajucha.control(30,30,speedTurn)
            else:
                jajucha.control(60,60,speedTurn)
        elif(L[2] != R[2] and (L[2] < 160 or R[2] < 160)):
            if(L[2] - R[2] < 0):
                jajucha.control(60,60,speedTurn)
            else:
                jajucha.control(30,30,speedTurn)
        elif(L[1] != R[1] and (L[1] < 160 or R[1] < 160)):
            if(L[1] - R[1] < 0):
                jajucha.control(60,60,speedTurn)
            else:
                jajucha.control(30,30,speedTurn)
        elif(L[0] != R[0] and (L[0] < 160 or R[0] < 160)):
            if(L[0] - R[0] < 0):
                jajucha.control(60,60,speedTurn)
            else:
                jajucha.control(30,30,speedTurn)
        else:
            jajucha.control(45,45,speedOrig)

        jajucha.image_send(rgb) #이미지를 PC로 전송
if __name__ == "__main__":
    jajucha = Jajucha() #자주차 객체선언
    jajucha.control(45,45,50) #정지
    main_loop() #메인함수
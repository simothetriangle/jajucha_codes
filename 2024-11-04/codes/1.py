#자주차 기본 동작코드
from control import Jajucha
import cv2

def main_loop(): 
    qrgb,qdepth = jajucha.camera_init() #카메라 인스턴스 가져오기
    while True: 
        rgb = jajucha.image_get(qrgb) #RGB 이미지 가져오기
        (V,L,R), image = jajucha.gridFront(rgb)

        #Example
        if(V[5] < 100):
            jajucha.control(30,30,60)
        else:
            jajucha.control(45,45,60)

        jajucha.image_send(rgb) #이미지를 PC로 전송
if __name__ == "__main__":
    jajucha = Jajucha() #자주차 객체선언
    jajucha.control(45,45,50) #정지
    main_loop() #메인함수
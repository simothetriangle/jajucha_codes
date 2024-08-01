 #자주차 기본 동작코드
from control import Jajucha
import cv2



def main_loop():
    #get instance
    qrgb,qdepth = jajucha.camera_init()
    while True: 
        rgb = jajucha.image_get(qrgb)
        (V,L,R), image = jajucha.gridFront(rgb)
        depth = jajucha.image_get(qdepth)
        distance = jajucha.distance_get(depth)
        
        #Line Tracing
        jajucha.image_send('V[0]'+" "+'V[1]'+" "+'V[2]'+" "+'V[3]'+" "+'V[4]'+" "+'V[5]'+" "+'V[6]');
        
        
        
        
        
        print(distance)
      
        #if(distance > 60):
            #jajucha.control(45,45,50)
        #else:
            #jajucha.control(45,45,60)

        jajucha.image_send(depth) #이미지를 PC로 전송
      
if __name__ == "__main__":
    jajucha = Jajucha() #자주차 객체선언
    jajucha.control(45,45,50) #정지
    main_loop() #메인함수
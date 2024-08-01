from control import Jajucha
import cv2

def main_loop():
    qrgb,qdepth = jajucha.camera_init() 
    while True: 
        rgb = jajucha.image_get(qrgb)
        canny = cv2.Canny(rgb,100,10)
        jajucha.image_send(canny)
      
if __name__ == "__main__":
    jajucha = Jajucha()
    jajucha.control(45,45,50)
    main_loop()
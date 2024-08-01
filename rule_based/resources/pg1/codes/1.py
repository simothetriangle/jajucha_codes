from control import Jajucha
import cv2

def main_loop():
    qrgb,qdepth = jajucha.camera_init() 
    while True: 
        rgb = jajucha.image_get(qrgb)
        jajucha.image_send(rgb)
      
if __name__ == "__main__":
    jajucha = Jajucha()
    jajucha.control(45,45,50)
    main_loop()
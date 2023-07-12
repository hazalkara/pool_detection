import cv2
import numpy as np
import socket,pickle,os
s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_SNDBUF,1000000)
server_ip = "192.168.0.10"
server_port = 6666


def gstreamer_pipeline( #CSI kamerasından alınan görüntü GST-streamer ile bazı video özellikleri döndürür
    capture_width=1920,   #kamera boyutu
    capture_height=1080,
    display_width=960,    #ekrandaki pencere boyutunu belirliyoruz
    display_height=540,   
    framerate=30,         #30 fps
    flip_method=0,        #kamera yönü belirleme(dik pozisyonda ya 0 ya 2 olacak)
):
    return (   #CSI kamerasından alınan görüntü GST-streamer ile bazı video özellikleri döndürür
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink drop=True"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

center=(0,0)
def blue_detect():
    window_title = "Blue Detect"
    
    
    video_capture = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)
    if video_capture.isOpened():
        try:
            cv2.namedWindow(window_title, cv2.WINDOW_AUTOSIZE)
            while True:
                ret, frame = video_capture.read()
                
                
                hsv =cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                lower_blue= np.array([75,100,100])
                upper_blue= np.array([130,255,255])
                
                blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
    
                blue = cv2.bitwise_and(frame, frame, mask=blue_mask)
    
                konturlar = cv2.findContours(blue_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

                if(len(konturlar) > 5):
        #en geniş alana sahip kontur
                    engeniskontur = max(konturlar,key=cv2.contourArea)
        #En büyük konturun capı ve merkez pixel koordinatları
                    ((x,y),radius) = cv2.minEnclosingCircle(engeniskontur)

                    if radius > 5:
            #cember cizdirme
                        cv2.circle(blue,(int(x), int(y)), int(radius),(0, 255, 255), 3)
                        width_frame=radius*2

                cv2.imshow("Mavi", blue)
                
                ret,buffer = cv2.imencode(".jpg",blue,[int(cv2.IMWRITE_JPEG_QUALITY),30])
                x_as_bytes = pickle.dumps(buffer)
                s.sendto((x_as_bytes),(server_ip,server_port))
        
                
                
                
                if cv2.getWindowProperty(window_title, cv2.WND_PROP_AUTOSIZE) >= 0:
                    cv2.imshow(window_title, frame)
                else:
                    break
                keyCode = cv2.waitKey(10) & 0xFF
                # Stop the program on the ESC key or 'q'
                if keyCode == 27 or keyCode == ord('q'):
                    break
        finally:
            video_capture.release()
            cv2.destroyAllWindows()
    else:
        print("Unable to open camera")


if __name__ == "__main__":
    blue_detect()

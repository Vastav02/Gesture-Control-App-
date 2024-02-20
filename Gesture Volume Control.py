import cv2
import time
import HandTrackingModule as htm
import math
import numpy as np

cap=cv2.VideoCapture(0)
cap.set(3,1280)#width of the cap
cap.set(4,720)#height of the cap

detector=htm.handDetector(detectionCon=0.7)

iTime=0
length=50
while True:
    success, img= cap.read()
    img=detector.findHands(img)
    lmList=detector.findPosition(img,draw=False)
    if len(lmList)>0:
        x1,y1=lmList[4][1],lmList[4][2]
        x2,y2=lmList[8][1],lmList[8][2]
        cx,cy=(x1+x2)//2,(y1+y2)//2
        
        cv2.circle(img,(x1,y1),9,(190,120,260),cv2.FILLED)
        cv2.circle(img,(x2,y2),9,(190,120,260),cv2.FILLED)
        cv2.line(img, (x1,y1),(x2,y2),(190,120,260),3)
        cv2.circle(img,(cx,cy),9,(190,120,260),cv2.FILLED)

        length=math.hypot(x2-x1,y2-y1)

        vol=np.interp(length,[50,300],[-65.25,0])
        
        if length<50:
            cv2.circle(img,(cx,cy),9,(255,255,0),cv2.FILLED)

    volBar=np.interp(length,[50,300],[400,150])
    volPer=int(np.interp(length,[50,300],[0,100]))
    cv2.rectangle(img,(50,int(volBar)),(85,400),(0,255,255),cv2.FILLED)
    cv2.rectangle(img,(50,150),(85,400),(0,220,160),3)
    cv2.putText(img,f"Vol: {volPer}%",(40,450),cv2.FONT_HERSHEY_COMPLEX,1,(0,220,160),1)
    
    cTime=time.time()
    fps=int(1/(cTime-iTime))
    iTime=cTime

    cv2.putText(img,f"fps: {fps}",(40,70),cv2.FONT_HERSHEY_COMPLEX,1,(0,220,160),2)
    
    cv2.imshow("Image",img)
    #cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

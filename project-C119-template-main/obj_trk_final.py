import cv2
import math
p1 = 530
p2 = 300
xs = []
ys = [] 
video = cv2.VideoCapture("footvolleyball.mp4")

# load tracker
tracker = cv2.TrackerCSRT_create()

# read th first frame on the video
Return, image = video.read()

# select the bounding box on the image
Bbox = cv2.selectROI("tracking", image, False)

tracker.init(image, Bbox)
def drawbox(image, Bbox):
    x,y,w,h = int(Bbox[0]), int(Bbox[1]), int(Bbox[2]), int(Bbox[3])
    cv2.rectangle(image,(x,y), ((x+w), (y+h)),(255,0,255), 3, 1)
def goaltrack(image,Bbox):
    x,y,w,h = int(Bbox[0]), int(Bbox[1]), int(Bbox[2]), int(Bbox[3])

    # get the center point of bounding box
    c1 = x + int(w/2)
    c2 = y + int(h/2)
    cv2.circle(image, (c1,c2),2,(0,255,0),3)
    cv2.circle(image, (p1,p2),2,(0,255,0),3)

    # calculate distance
    distance = math.sqrt(((c1 - p1)**2)+(c2-p2)**2)
    print(distance)
    if distance <= 20:
        cv2.putText(image,"goal",(300,90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    xs.append(c1)
    ys.append(c2)    
    for i in range(len(xs)-1):
        cv2.circle(image, (xs[i],ys[i]),2,(0, 255, 0), 2)

while True:
    check, image = video.read()

    #update the tracker on the image and the bounding box
    success, Bbox = tracker.update(image)
    if success:
        drawbox(image, Bbox)
    else:
        cv2.putText(image, "lost", (75,90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
    goaltrack(image, Bbox)
    cv2.imshow("result", image)
    key = cv2.waitKey(25)
    if key == 32:
        print("stop")
        break
video.release()
cv2.destroyAllWindows()     
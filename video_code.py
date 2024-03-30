import cv2
import face_recognition
import sys

def take_pictuer():
    print("Take photo")
    сар = cv2.VideoCapture(0)
    ret,frame=  сар.read()
    cv2.imwrite('Picture.jpg', frame)
    cv2.destroyAllWindows()
    сар. release()
    print("Face scan complete")

def analyze_user():
    print("Analyze face..")
    baseImg=face_recognition.load_image_file("example.jpg")
    baseImg=cv2.cvtColor(baseImg,cv2.COLOR_BGR2RGB)

    myface=face_recognition.face_locations(baseImg)[0]
    encodemyface= face_recognition.face_encodings(baseImg)[0]
    cv2.rectangle(baseImg,(myface[3],myface[0]),(myface[1],myface[2]),(255, 255, 0),2)

    #cv2.imshow("Find me",baseImg)
    #cv2.waitKey(0)

    sampleimg= face_recognition.load_image_file("Picture.jpg")
    sampleimg=cv2.cvtColor(sampleimg, cv2.COLOR_BGR2RGB)

    try:
        samplefacetest = face_recognition.face_locations(sampleimg)[0]
        encodesamplefacetest = face_recognition.face_encodings(sampleimg)[0]
    except IndexError as e:
        print("Index Error. Authentication Failed.")
        sys.exit()

    result= face_recognition.compare_faces([encodemyface],encodesamplefacetest)
    resultString = str(result)
    print (resultString)

    if resultString == "[True]":
        print ("User Authenticated. Welcome back sir!")
    else:
        print ("Authentication Failed. Good bye!")
#take_pictuer()
analyze_user()
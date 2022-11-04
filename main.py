import cv2 as cv
from carTracker import *
from datetime import datetime
import pyodbc
#abro una conexion a la base de datos
db='DB_tpi'
server='localhost'
cnxn = pyodbc.connect(r'Driver=SQL Server;Server='+server+';Database=DBStagingDev;Trusted_Connection=yes;')
cursor = cnxn.cursor()


datos=[]
# Objeto de seguimiento
tracker = EuclideanDistTracker()
path="road.mp4"
cap = cv.VideoCapture(path)

# Object detection from Stable camera
object_detector = cv.createBackgroundSubtractorMOG2(history=100, varThreshold=40)

while True:
    ret, frame = cap.read()
    height, width, _ = frame.shape

    # Extraer región de interés
    roi = frame[340: 720,500: 800]

    # Detección de objetos 
    mask = object_detector.apply(roi)
    _, mask = cv.threshold(mask, 254, 255, cv.THRESH_BINARY)
    contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    detections = []
    for cnt in contours:
        # Calcula el área y elimina los elementos pequeños
        area = cv.contourArea(cnt)
        if area > 100:
            x, y, w, h = cv.boundingRect(cnt)
            detections.append([x, y, w, h])

    # Seguimiento de objetos
    boxes_ids = tracker.update(detections)
    for box_id in boxes_ids:
        x, y, w, h, id = box_id
        cv.putText(roi, str(id), (x, y - 15), cv.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        cv.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 3)
        datos.append([id,x, y, w, h, str(datetime.now())])

    cv.imshow("roi", roi)
    cv.imshow("Frame", frame)
    cv.imshow("Mask", mask)

    key = cv.waitKey(30)
    if key == 27:
        break

cap.release()
cv.destroyAllWindows()
print('ides:')
for box_id in boxes_ids:
    print(box_id)

print('detecions:')
#for det in detections:
 #   print(det)
#guardo los elementos encontrados en la base de datos
for dato in datos:
    query="insert into roadDetection_hist values (%d,%d,%d,%d,%d,'%s')"%(dato[0],dato[1],dato[2],dato[3],dato[4],dato[5])
    print(query)
    cursor.execute(query)
    cnxn.commit()
print("se agregaron ",len(datos),"registros")
cnxn.close()


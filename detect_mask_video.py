
from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import time
import cv2
import os
from DBConnection import Db
import face_recognition
# image_path="C:\\Users\\lenovo\\PycharmProjects\\face-mask-detector\\photos\\"
known_faces = []
ids = []
type=[]
db=Db()
res=db.select("SELECT * FROM `staff`")
if len(res)>0:
    for k in res:
        stafftype=k["type"]
        if stafftype=="staff":
            ids.append(k['regid'])
            fname=k['image']
            fn=fname.split("/")
            fname=fn[len(fn)-1]
            img="C:\\Users\\HP\\PycharmProjects\\MES MASK VIOLATIONS\\untitled\\static\\staff\\"+fname
            print(img)
            b_img = face_recognition.load_image_file(img)
            print(b_img)
            b_imgs = face_recognition.face_encodings(b_img)[0]
            known_faces.append(b_imgs)
            type.append("staff")
        else:
            ids.append(k['regid'])
            fname = k['image']
            fn = fname.split("/")
            fname = fn[len(fn) - 1]
            img = "C:\\Users\\HP\\PycharmProjects\\MES MASK VIOLATIONS\\untitled\\static\\staff\\" + fname
            print(img)
            b_img = face_recognition.load_image_file(img)
            print(b_img)
            b_imgs = face_recognition.face_encodings(b_img)[0]
            known_faces.append(b_imgs)
            type.append("staff")



#
#
res1=db.select("SELECT * FROM familiar_person")
if len(res1)>0:
    for k in res1:
        ids.append(k['fp_id'])
        fname=k['fp_image']
        fn=fname.split("/")
        fname=fn[len(fn)-1]
        img = "C:\\Users\\HP\\PycharmProjects\\MES MASK VIOLATIONS\\untitled\\static\\familiar_persons\\" + fname
        print(img)
        b_img = face_recognition.load_image_file(img)
        print(b_img)
        b_imgs = face_recognition.face_encodings(b_img)[0]
        known_faces.append(b_imgs)
        type.append("familiar_person")


vs = VideoStream(src=0).start()
time.sleep(2.0)

while True:
    # grab the frame from the threaded video stream and resize it
    # to have a maximum width of 400 pixels
    frame = vs.read()
    frame = imutils.resize(frame, width=400)

    cv2.imwrite("a.jpg",frame)

    unknown_image = face_recognition.load_image_file("a.jpg")
    m = len(face_recognition.face_encodings(unknown_image))
    print("lllll ", m)
    db = Db()
    flg=0
    for a in range(m):
        s = face_recognition.face_encodings(unknown_image)[a]
        unknown_encoding = face_recognition.face_encodings(unknown_image)[a]
        results = face_recognition.compare_faces(known_faces, unknown_encoding, tolerance=0.50)
        print(str(results))
        for i in range(0, len(results)):
            if results[i] == True and type[i]=="staff":
                flg=1
                print("hiii")
                db2 = Db()
                rr = db2.selectOne("select * from s_attendance where a_date=curdate() and s_id='" + str(
                    ids[i]) + "' LIMIT 1")
                print(rr)
                if rr is None:
                    rs = db2.insert(
                        "insert into s_attendance(`a_date`,s_id,status,a_time,check_out) values(curdate(),'" + str(
                            ids[i]) + "','checkedin',curtime(),'')")
                    # print("rs==" + rs)
                    print("inserted......")
                else:
                    if rr['status'] == 'checkedin':
                        print("hlooo")
                        st_id = str(rr['s_id'])
                        if str(st_id) == str(ids[i]):
                            res1 = db2.update(
                                "update s_attendance set check_out=curtime(),status='checkedout' where s_id='" + str(
                                    ids[i]) + "' and `a_date`=curdate()")
                            print(res1)
                    else:
                        res4 = db2.update(
                            "update s_attendance set check_out=curtime(),status='present' where s_id='" + str(
                                ids[i]) + "' and `a_date`=curdate()")
                        print(res4)

            elif results[i] == True and type[i]=="familiar_person":
                flg=1
                print("Familiar")
                db2 = Db()
                rr = db2.selectOne("select * from alert where date=curdate() and f_id='" + str(
                    ids[i]) + "' LIMIT 1")
                print(rr)
                if rr is None:
                    rs = db2.insert(
                        "insert into alert(`date`,f_id,time) values(curdate(),'" + str(
                            ids[i]) + "',curtime())")
                    print("rs==" + rs)
                    print("inserted......")
                else:
                    res1 = db2.update(
                        "update alert set time=curtime() where f_id='" + str(
                            ids[i]) + "' and `date`=curdate()")

        if flg==0:
            from PIL import Image
            img=Image.open("C:\\Users\\HP\\PycharmProjects\\MES MASK VIOLATIONS\\face-mask-detector\\face-mask-detector\\a.jpg")
            dt = time.strftime("%Y%m%d-%H%M%S")
            img.save("C:\\Users\\HP\\PycharmProjects\\MES MASK VIOLATIONS\\untitled\\static\\visitor_img\\"+dt+".jpg")
            path="/static/visitor_img/"+dt+".jpg"
            db=Db()
            db.insert("insert into visitors_log(`v_date`,v_img,v_time) values(curdate(),'"+path+"', curtime())")



    cv2.imshow("Frame", frame)
    cv2.waitKey(23)

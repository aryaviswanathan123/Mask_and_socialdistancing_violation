from flask import Flask,render_template,request,session,jsonify
from dbconnection import Db

app = Flask(__name__)
app.secret_key="kkk"

staticpath="C:\\Users\\HP\\PycharmProjects\\untitled\\static\\"


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/login_post',methods=['post'])
def login_post():

       un = request.form['textfield']
       pw = request.form['textfield2']
       session["pass"]=pw
       q="SELECT * FROM login WHERE username='"+un+"' AND `password`='"+pw+"'"
       d=Db()
       res=d.selectOne(q)
       if res is not None:
           session["lid"]=res["login_id"]
           if res["type"]=="admin":
                return '''<script>alert('successfully logined!');window.location='/adminhome'</script>'''
           else:
               return '''<script>alert('Invalid username or password!');window.location='login'</script>'''
       else:
           return '''<script>alert('Invalid username or password!');window.location='login'</script>'''






@app.route('/adminhome')
def adminhome():

    return render_template("admin/adminhome.html")





@app.route('/changepassword')
def changepassword():
    return render_template("admin/changepassword.html")


@app.route('/changepassword_post',methods = ['post'])
def changepassword_post():
        old = request.form['textfield3']
        cn = request.form['textfield2']
        if(session["pass"]==old):
            qry="UPDATE login SET PASSWORD='"+cn+"' WHERE login_id='"+str(session["lid"])+"'"
            d=Db()
            res=d.update(qry)
            return '''<script>alert('password updated!');window.location='/login'</script>'''
        else:
            return '''<script>alert('error!');window.location='/changepassword'</script>'''





@app.route('/addnots')
def addnotes():
    return render_template("admin/addnots.html")

@app.route('/addnots_post', methods=['post'])
def addnots_post():

        af = request.form['textarea']

        qry="INSERT INTO `notifications`(`notification`,`not_date`,`not_time`)VALUES('"+af+"',curdate(),curtime())"
        d=Db()
        d.insert(qry)
        return '''<script>alert('successfully added!');window.location='addnots'</script>'''



@app.route('/stfm')
def stfm():
    return render_template("admin/staff_management.html")
@app.route('/stfm_post',methods=['post'])
def stfm_post():

        nm = request.form['textfield']
        hn = request.form['textfield2']
        pl= request.form['textfield0']
        po = request.form['textfield3']
        pi = request.form['textfield4']
        em = request.form['textfield5']
        ph = request.form['textfield6']
        im = request.files['fileField']
        im.save(staticpath+"staff\\"+im.filename)
        url="/static/staff/"+im.filename
        ty = request.form['type']
        import random
        passw=str(random.randint(0000,9999))
        d = Db()
        q="INSERT INTO `login`(`username`,`password`,`type`)VALUES('"+em+"','"+passw+"' ,'staff')"
        lid=d.insert(q)

        qry = "INSERT INTO `staff`(`login_id`,`name`,`hname`,`place`,`pin`,`post`,`phone_no`,`image`,`email`,`type`)" \
              "VALUES('"+str(lid)+"','"+nm+"','"+hn+"','"+pl+"','"+pi+"','"+po+"','"+ph+"','"+url+"','"+em+"','"+ty+"')"

        d.insert(qry)
        return '''<script>alert('successfully registered!');window.location='stfm'</script>'''
















@app.route('/maskviolationreport')
def maskviolationreport():


        qry="SELECT `mask_violation`.*,staff.`name`,staff.`hname`,staff.`place`,staff.`pin`,staff.`post`,staff.`phone_no`,staff.`image`,staff.`email`,staff.`type` FROM `mask_violation` INNER JOIN `staff` ON staff.`login_id`=mask_violation.`login_id`"
        d=Db()
        res=d.select(qry)
        return render_template("admin/maskviolationreport.html",data=res)




@app.route('/nots')
def nots():
    qry="SELECT * FROM `notifications`"
    d=Db()
    res=d.select(qry)
    return render_template("admin/nots.html",data=res)




@app.route('/dltnots/<id>')
def dltnots(id):
    qry = "DELETE FROM `notifications` WHERE `not_id`='" + id + "'"
    d = Db()
    res = d.delete(qry)
    return '''<script>alert('successfully deleted!');window.location='/nots';</script>'''



@app.route('/edtnots/<id>')
def edtnots(id):
    qry = "SELECT * FROM `notifications` WHERE `not_id`='" + id + "'"
    d = Db()
    res = d.selectOne(qry)
    return render_template("admin/editnots.html", data=res)



@app.route('/edtnots_post',methods=['post'])
def edtnots_post():
    nfid=request.form['nid']
    nf=request.form['textarea']
    qry="UPDATE `notifications` SET `notification`='"+nf+"' , not_date=now() , not_time=curtime() WHERE `not_id`='"+nfid+"'"
    d = Db()
    res = d.update(qry)
    return '''<script>alert('successfully updated!');window.location='/nots'</script>'''






@app.route('/staff attendance')
def staffattendance():
         qry="SELECT `s_attendance`.*,`staff`.`name`,`staff`.`type` FROM `s_attendance` INNER JOIN `staff` ON `staff`.`login_id`=`s_attendance`.`s_id`"
         d=Db()
         res=d.select(qry)

         return render_template("admin/staff attendance.html",data=res)



@app.route('/atdnc_search_post',methods=['post'])
def atdnc_search_post():
    dtf=request.form['d1']
    dtt=request.form['d2']
    d=Db()
    qry="SELECT `s_attendance`.*,`staff`.`name`,`staff`.`type` FROM `s_attendance` INNER JOIN `staff` ON `staff`.`login_id`=`s_attendance`.`s_id` where s_attendance.a_date BETWEEN '"+dtf+"' and '"+dtt+"'"
    res=d.select(qry)
    return render_template("admin/staff attendance.html", data=res)








@app.route('/viewstaff')
def viewstaff():
    qry = "SELECT * FROM `staff`"
    d = Db()
    res = d.select(qry)
    return render_template("admin/view staff.html",data=res)



@app.route('/delstaff/<id>')
def delstaff(id):
    qry = "DELETE FROM `staff` WHERE `regid`='"+id+"'"
    d = Db()
    res = d.delete(qry)
    return '''<script>alert('successfully deleted!');window.location='/viewstaff'</script>'''



@app.route('/editstaff/<id>')
def editstaff(id):
    qry = "SELECT * FROM `staff` WHERE `regid`='"+id+"'"
    d = Db()
    res = d.selectOne(qry)


    return render_template("admin/editstaff.html",data=res)


@app.route('/editstaff_post',methods=['post'])
def editstaff_post():

    regid=request.form['sid']
    nm = request.form['textfield']
    hn = request.form['textfield2']
    pl = request.form['textfield0']
    po = request.form['textfield3']
    pi = request.form['textfield4']
    em = request.form['textfield5']
    ph = request.form['textfield6']
    im = request.files['fileField']
    im.save(staticpath + "staff\\" + im.filename)
    url = "/static/staff/" + im.filename
    ty = request.form['type']

    qry="UPDATE `staff` set `name`='"+nm+"', `hname`='"+hn+"',`place`='"+pl+"',`pin`='"+pi+"',`post`='"+po+"',`phone_no`='"+ph+"',`image`='"+url+"',`email`='"+em+"',`type`='"+ty+"' where regid='"+regid+"'"
    d=Db()
    res=d.update(qry)
    return '''<script>alert('successfully updated!');window.location='/viewstaff'</script>'''





@app.route('/vssearch_post',methods=['post'])
def vssearch_post():
    v=request.form['textfield2']
    qry = "SELECT * FROM `staff` where name like '%"+v+"%'"
    d = Db()
    res = d.select(qry)
    return render_template("admin/view staff.html", data=res)





@app.route('/vilog')
def vilog():
    qry="SELECT `visitors_log` .*,`staff`.`name`,`staff`.`image`,`staff`.`type` FROM `visitors_log` LEFT JOIN `staff` ON `staff`.`login_id`=`visitors_log`.`st_id`"
    d=Db()
    res=d.select(qry)
    return render_template("admin/visitor'slog.html",data=res)




@app.route('/index')
def index():
    return render_template("admin/index.html")




@app.route('/sdviolation')
def sdviolation():

    qry="SELECT * FROM `social_distance`"
    d=Db()
    res=d.select(qry)
    return render_template("admin/sdviolation.html",data=res)





@app.route('/sdv_search_post',methods=['post'])
def sdv_search_post():
    sdtf=request.form['d1']
    sdtt=request.form['d2']
    d=Db()
    qry="SELECT * FROM `social_distance`  where social_distance.sd_date BETWEEN '"+sdtf+"' and '"+sdtt+"'"
    res=d.select(qry)
    return render_template("admin/sdviolation.html", data=res)


#-----------------------------------android



@app.route('/and_login_post',methods=['post'])
def  and_login_post():

    un = request.form['usnm']
    pw = request.form['pswd']
    q="SELECT * FROM login WHERE username='"+un+"' AND `password`='"+pw+"'"
    d=Db()
    res=d.selectOne(q)
    if res is not None:

        if res["type"] == "staff":
            return jsonify(status="ok",login_id=res["login_id"])
        else:
            return jsonify(status="no")
    else:
            return jsonify(status="ok")



@app.route('/and_viewstf_post',methods=['post'])
def and_viewstf_post():
    # nm = request.form['textfield']
    # hn = request.form['textfield2']
    # pl = request.form['textfield0']
    # pi = request.form['textfield4']
    # em = request.form['textfield5']
    # ph = request.form['textfield6']
    # im = request.form['fileField']
    # import time, datetime
    from encodings.base64_codec import base64_decode
    # import base64

    # timestr = time.strftime("%Y%m%d-%H%M%S")
    # print(timestr)
    # a = base64.b64decode(im)
    # fh = open("static/staff/" + timestr + ".jpg", "wb")
    # path = "/static/staff/" + timestr + ".jpg"
    # fh.write(a)
    # fh.close()
    lid=request.form['lid']
    d = Db()
    qry = "SELECT * FROM `staff` WHERE login_id='"+lid+"' "
    res=d.selectOne(qry)
    return jsonify(status="ok", image=res['image'],name=res['name'],housename=res['hname'],place=res['place'],contact=res['phone_no'],email=res['email'],pin=res['pin'])








@app.route('/and_changepassword_post',methods = ['post'])
def and_changepassword_post():
    old = request.form['textfield3']
    cn = request.form['textfield2']
    lid = request.form['lid']
    d = Db()
    q="SELECT * FROM `login` WHERE PASSWORD='"+old+"'"
    res=d.selectOne(q)
    if res!=None:
        qry="UPDATE login SET PASSWORD='"+cn+"' WHERE login_id='"+str(["lid"])+"'"

        re=d.update(qry)
        return jsonify(status="ok")
    else:
        return jsonify(status="Invalid!")





@app.route('/and_addfamiliar_post',methods=['post'])
def and_addfamiliar_post():
    fn=request.form['afn']
    fe=request.form['afe']
    fp=request.form['afp']
    fr=request.form['afr']
    fi=request.form['afi']

    import time, datetime
    from encodings.base64_codec import base64_decode
    import base64

    timestr = time.strftime("%Y%m%d-%H%M%S")
    print(timestr)
    a = base64.b64decode(fi)
    fh = open("C:\\Users\\HP\\PycharmProjects\\untitled\\static\\familiar_persons" + timestr + ".jpg", "wb")
    path = "/static/familiar_person/" + timestr + ".jpg"
    fh.write(a)
    fh.close()
    d = Db()
    qry="INSERT INTO `familiar_person`(`fp_name`,`fp_image`,`fp_email`,`fp_ph`,`fp_relation`)VALUES('"+fn+"','"+fi+"','"+fe+"','"+fp+"','"+fr+"')"
    res=d.insert(qry)
    return jsonify(status="ok")




@app.route('/and_view_fam_psn_post',methods=['post'])
def and_view_fam_psn_post():
    d=Db()
    qry="SELECT * FROM `familiar_person`"
    res=d.select(qry)
    return jsonify(status="ok", users=res)







@app.route('/and_staff_sugs_post',methods=['post'])
def and_staff_sugs_post():
    # si=request.form['ssi']
    # sn=request.form['ssn']
    # sde=request.form['ssde']
    # sdt=request.form['ssdt']
    #
    # import time, datetime
    # from encodings.base64_codec import base64_decode
    # import base64
    #
    # timestr = time.strftime("%Y%m%d-%H%M%S")
    # print(timestr)
    # a = base64.b64decode(si)
    # fh = open("static/staff_suggtns/" + timestr + ".jpg", "wb")
    # path = "/static/staff_suggtns/" + timestr + ".jpg"
    # fh.write(a)
    # fh.close()

    d=Db()
    qry="SELECT `staff_sgtn`.*,`staff`.`name` FROM `staff_sgtn` INNER JOIN `staff` ON `staff`.`login_id`=`staff_sgtn`.`ssg_lid`"
    res=d.select(qry)
    return jsonify(status="ok",users=res)






@app.route('/and_mv_alert_post',methods=['post'])
def and_mv_alert_post():
    d = Db()
    qry = "SELECT `mask_violation`.*,`staff`.`name` FROM `mask_violation` INNER JOIN `staff` ON `staff`.`login_id`=`mask_violation`.`login_id`"
    res = d.select(qry)
    return jsonify(status="ok", users=res)




@app.route('/and_view_visitor_post',methods=['post'])
def and_view_visitor_post():
    d=Db()
    qry="SELECT `visitors_log`.*,`staff`.`name` FROM `visitors_log` INNER JOIN `staff` ON `staff`.`login_id`=`visitors_log`.`st_id`"
    res=d.select(qry)
    return jsonify(status="ok", users=res)







@app.route('/and_view_nots',methods=['post'])
def and_view_nots():
    d=Db()
    qry="SELECT * FROM `notifications`"
    res=d.select(qry)
    return jsonify(status="ok", users=res)




if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')

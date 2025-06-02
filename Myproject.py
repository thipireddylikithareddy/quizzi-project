
from flask import Flask, render_template, request, redirect, flash, url_for, session
import sqlite3
from datetime import *
from flask_session import Session

curdir = r"C:\Users\User\Downloads\QUIZZI-TEAM 4\PROJECT FILE"
app = Flask(__name__)
app.config["SECRET_KEy"] = "uytraw35467y8uoikkijh"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/register", methods=["POST","GET"])
def registeration():    
    fname = request.form['namef']
    username = request.form['emaile']
    prof = request.form['prof']
    password = request.form['passwordp']
    conpassword = request.form['passwordcon']
    con = sqlite3.connect(curdir + "\Project.db")
    cur = con.cursor()
    if cur.execute("SELECT username from Register WHERE username=:username",{"username":username}).fetchone():
        flash("username already exits, try another","danger")
        return redirect("register")
    else:
        if password == conpassword:
            cur.execute("INSERT INTO Register VALUES (?,?,?,?)",(fname,username,password,prof,))
            con.commit()
            con.close()
            flash("Registered Successfully!!","success")
            return redirect(url_for('login'))
        else:
            flash("Password doesn't match","danger")
            return render_template('register.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/login", methods=["POST","GET"])
def loginpage():
    username = request.form["user"]
    session["user"] = username
    password = request.form["password"]
    con = sqlite3.connect(curdir + "\Project.db")
    cur = con.cursor()
    user = cur.execute("SELECT username from Register WHERE username=:username",{"username":username}).fetchone()
    passw = cur.execute("SELECT password from Register WHERE username=:username",{"username":username}).fetchone()
    prof = cur.execute("SELECT prof from Register WHERE username=:username",{"username":username}).fetchone()
    con.commit()
    con.close()
    prof_data = ""
    pass_data = ""
    user_data = ""
    if user is None:
        flash("No such user","danger")
        return render_template("login.html")
    else:
        for a in prof:
            prof_data = prof_data + a
        for a in passw:
            pass_data = pass_data + a
        for a in user:
            user_data = user_data + a
        if password == pass_data:
            flash("Login Succesfull!!","success")
            if prof_data == "Teacher":
                return redirect(url_for('teacher',user = user_data))
            else:
                return redirect(url_for('student'))
        else:
            flash("Incorrect password","danger")
            return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user",None)
    return redirect('/')

@app.route("/teacher")
def teacher():
    username = session.get("user")
    con = sqlite3.connect(curdir + "\Project.db")
    cur = con.cursor()
    if cur.execute("SELECT name FROM classes WHERE username=:username",{"username":username}).fetchone():
        classes = cur.execute("SELECT name FROM classes WHERE username=:username",{"username":username}).fetchall()
        con.commit()
        con.close()
        return render_template("teacher.html",classes=classes)
    else:
        return render_template("teacher.html")

@app.route("/student")
def student():
    username = session.get("user")
    con = sqlite3.connect(curdir + "\Project.db")
    cur = con.cursor()
    classes = cur.execute("SELECT classname FROM studentinfo WHERE username=:username",{"username":username}).fetchall()
    con.commit()
    con.close()
    return render_template("student.html",classes=classes)

@app.route("/studjoin")
def studjoin():
    return render_template("studjoin.html")

@app.route("/classjoin", methods = ["POST","GET"])
def classjoin():
    classname = request.form["name"]
    #session["myclass"] = classname
    username = session.get("user")
    con = sqlite3.connect(curdir + "\Project.db")
    cur = con.cursor()
    classes = cur.execute("SELECT classname FROM studentinfo WHERE username=:username",{"username":username}).fetchall()
    tclasses = cur.execute("SELECT name FROM classes").fetchall()
    con.commit()
    con.close()
    n=len(classes)
    tn = len(tclasses)
    suc1 = False
    suc2 = False
    count = 0
    for j in range(n):
        if classname == classes[j][0]:
            suc1 = True
            flash("you already joined the class","danger")
            return render_template("student.html",classes=classes)
        else:
            pass
    for j in range(tn):   
        if classname != tclasses[j][0]:
            count = count + 1
            if count == tn:
                suc2 = True
                flash("No Such Class Found!","danger")
                return render_template("student.html",classes=classes)
        else:
            if suc1== False and suc2== False:
                con = sqlite3.connect(curdir + "\Project.db")
                cur = con.cursor()
                cur.execute("INSERT INTO studentinfo VALUES (?,?)",(classname,username,))
                con.commit()
                classes = cur.execute("SELECT classname FROM studentinfo WHERE username=:username",{"username":username}).fetchall()
                con.close()
                flash("joined class successfully","success")
                return render_template("student.html",classes=classes)
   
@app.route("/classopen",methods = ["POST","GET"])
def classopen():
    session["myclass"]= request.form["sclass"]
    return render_template("classopen.html")

@app.route("/quizdisplay")
def quizdisplay():
    classname=session.get("myclass")
    con = sqlite3.connect(curdir + "\Project.db")
    cur = con.cursor()
    quizzes=cur.execute("SELECT Quiz from Quizzes WHERE classname=:classname",{"classname":classname}).fetchall()
    con.commit()
    con.close()
    return render_template("classopen.html",quizzes=quizzes,name=classname)
     
@app.route("/studjoined")
def studjoined():
    return render_template("studjoined.html")

@app.route("/quizjoined", methods = ["POST","GET"])
def quizjoined():
    return render_template("quizjoined.html")

@app.route("/quizzattempt",methods =["POST","GET"])
def quizzattempt():
    quizname = request.form["name"]
    session["quizname"] = quizname
    username = session.get("user")
    classname = session.get("myclass")
    con = sqlite3.connect(curdir + "\Project.db")
    cur = con.cursor()
    qname = cur.execute("SELECT Quiz FROM Quizzes WHERE classname=:classname",{"classname":classname}).fetchall()
    aqname = cur.execute("SELECT quizname FROM Result WHERE username=:username AND quizname=:quizname",{"username":username,"quizname":quizname}).fetchall()
    l = len(qname)
    l1 = len(aqname)
    suc = False
    suc1= False
    count = 0
    for j in range(l):
        if quizname != qname[j][0]:
            count = count + 1
            if count == l:
                suc = True
                flash("No Such Quiz Found!","danger")
                return render_template("classopen.html")
    for j in range(l1):
        if quizname == aqname[j][0]:
            suc1 = True
            flash("Quiz already attempted!","danger")
            return render_template("classopen.html")
        
    if suc == False and suc1 == False:
                table = tuple(cur.execute("SELECT * FROM "+quizname))
                con.close()
                global q1,q1o1,q1o2,q1o3,q1o4,q2,q2o1,q2o2,q2o3,q2o4,q3,q3o1,q3o2,q3o3,q3o4,q4,q4o1,q4o2,q4o3,q4o4,q5,q5o1,q5o2,q5o3,q5o4
                global q1c,q2c,q3c,q4c,q5c
                q1,q1o1,q1o2,q1o3,q1o4,q1c = table[0][0],table[0][1],table[0][2],table[0][3],table[0][4],table[0][5]
                q2,q2o1,q2o2,q2o3,q2o4,q2c = table[1][0],table[1][1],table[1][2],table[1][3],table[1][4],table[1][5]
                q3,q3o1,q3o2,q3o3,q3o4,q3c = table[2][0],table[2][1],table[2][2],table[2][3],table[2][4],table[2][5]
                q4,q4o1,q4o2,q4o3,q4o4,q4c = table[3][0],table[3][1],table[3][2],table[3][3],table[3][4],table[3][5]
                q5,q5o1,q5o2,q5o3,q5o4,q5c = table[4][0],table[4][1],table[4][2],table[4][3],table[4][4],table[4][5]
                return render_template("studquiz.html",
                q1=q1,q1o1=q1o1,q1o2=q1o2,q1o3=q1o3,q1o4=q1o4,q1c=q1c,
                q2=q2,q2o1=q2o1,q2o2=q2o2,q2o3=q2o3,q2o4=q2o4,q2c=q2c,
                q3=q3,q3o1=q3o1,q3o2=q3o2,q3o3=q3o3,q3o4=q3o4,q3c=q3c,
                q4=q4,q4o1=q4o1,q4o2=q4o2,q4o3=q4o3,q4o4=q4o4,q4c=q4c,
                q5=q5,q5o1=q5o1,q5o2=q5o2,q5o3=q5o3,q5o4=q5o4,q5c=q5c,quizname=quizname)

    

@app.route("/atemptedquiz",methods=["POST","GET"])
def atemptedquiz():
    username=session.get("user")
    quizname=session.get("quizname")
    classname=session.get("myclass")
    q1s = request.form["q1"]
    session["q1"]=q1s
    q2s = request.form["q2"]
    session["q2"]=q2s
    q3s = request.form["q3"]
    session["q3"]=q3s
    q4s = request.form["q4"]
    session["q4"]=q4s
    q5s = request.form["q5"]
    session["q5"]=q5s
    con = sqlite3.connect(curdir + "\Project.db")
    cur = con.cursor()
    cur.execute("INSERT INTO attempted VALUES (?,?,?)",(username,quizname,classname,))
    con.commit()
    con.close()
    return redirect(url_for('submitquiz'))

   
@app.route("/quizadd", methods = ["POST","GET"])
def quizadd():
    ques1 = (request.form["q1"],request.form["q1o1"],request.form["q1o2"],request.form["q1o3"],request.form["q1o4"],request.form["q1c"])
    ques2 = (request.form["q2"],request.form["q2o1"],request.form["q2o2"],request.form["q2o3"],request.form["q2o4"],request.form["q2c"])
    ques3 = (request.form["q3"],request.form["q3o1"],request.form["q3o2"],request.form["q3o3"],request.form["q3o4"],request.form["q3c"])
    ques4 = (request.form["q4"],request.form["q4o1"],request.form["q4o2"],request.form["q4o3"],request.form["q4o4"],request.form["q4c"])
    ques5 = (request.form["q5"],request.form["q5o1"],request.form["q5o2"],request.form["q5o3"],request.form["q5o4"],request.form["q5c"])
    clist = [ques1,ques2,ques3,ques4,ques5]
    now = datetime.now()
    quiz = request.form["quizname"] + now.strftime("%d%m%Y%H%M%S")
    #cname = session.get("class")
    cname = request.form["classname"]
    con= sqlite3.connect(curdir + "\Project.db")
    cur = con.cursor()
    quizzes = cur.execute("SELECT Quiz FROM Quizzes").fetchall()
    con.commit()
    if quiz in quizzes:
        flash("Quiz name already exists","danger")
        return render_template("addquiz.html")
    else:
        cur.execute("INSERT INTO Quizzes VALUES (?,?)",(quiz,cname,))
        con.commit()
        cur.execute("CREATE TABLE " + quiz + "(ques text,op1 text,op2 text, op3 text,op4 text,cop text)")
        query1 = "INSERT INTO " + quiz + " (ques,op1,op2,op3,op4,cop) VALUES (?,?,?,?,?,?);"
        cur.executemany(query1,clist,)
        con.commit()
        con.close()
        flash("quiz added succesfully","success")
        return redirect("teacher")

@app.route("/previous1", methods = ["POST","GET"])
def previous1():
    username=session.get("user")
    classname=session.get("myclass")
    con= sqlite3.connect(curdir + "\Project.db")
    cur = con.cursor()
    quizzes = cur.execute("SELECT quizname FROM attempted WHERE classname=:classname AND username=:username",{"classname":classname,"username":username}).fetchall()
    con.commit()
    con.close()
    return render_template("previousquizes.html",quizzes=quizzes,username=username)

@app.route("/submitquiz", methods = ["POST","GET"])
def submitquiz():
    count = 0  
    username = session.get("user")
    quizname = session.get("quizname")
    q1s=session.get("q1")
    q2s=session.get("q2")
    q3s=session.get("q3")
    q4s=session.get("q4")
    q5s=session.get("q5")
    con = sqlite3.connect(curdir + "\Project.db")
    cur = con.cursor()
    clist = cur.execute("SELECT cop FROM "+ quizname).fetchall()
    q1c = clist[0][0]
    q2c = clist[1][0]
    q3c = clist[2][0]
    q4c = clist[3][0]
    q5c = clist[4][0]
    if q1s == q1c:
        count = count + 1
    if q2s == q2c:
        count = count + 1
    if q3s == q3c:
        count = count + 1
    if q4s == q4c:
        count = count + 1
    if q5s == q5c:
        count = count + 1
    con = sqlite3.connect(curdir + "\Project.db")
    cur = con.cursor()
    cur.execute("INSERT INTO Result VALUES (?,?,?)",(username,quizname,count,))
    con.commit()
    con.close()
    return render_template("submitquiz.html",
    q1s=q1s,q2s=q2s,q3s=q3s,q4s=q4s,q5s=q5s,
    q1=q1,q1o1=q1o1,q1o2=q1o2,q1o3=q1o3,q1o4=q1o4,q1c=q1c,
    q2=q2,q2o1=q2o1,q2o2=q2o2,q2o3=q2o3,q2o4=q2o4,q2c=q2c,
    q3=q3,q3o1=q3o1,q3o2=q3o2,q3o3=q3o3,q3o4=q3o4,q3c=q3c,
    q4=q4,q4o1=q4o1,q4o2=q4o2,q4o3=q4o3,q4o4=q4o4,q4c=q4c,
    q5=q5,q5o1=q5o1,q5o2=q5o2,q5o3=q5o3,q5o4=q5o4,q5c=q5c,
    score=count)

@app.route("/result",methods=["POST","GET"])
def studentresult():
    quizname=request.form["qname"]
    classname =session.get("myclass")
    con = sqlite3.connect(curdir + "\Project.db")
    cur = con.cursor()
    username = session.get("user")
    count = cur.execute("SELECT score FROM Result WHERE username=:username AND quizname=:quizname",{"username":username,"quizname":quizname}).fetchone()
    score = count[0][0]
    ques = cur.execute("SELECT ques FROM " + quizname).fetchall()
    cop = cur.execute("SELECT cop FROM " + quizname).fetchall()
    con.commit()
    con.close()
    return render_template("quizdisplay.html",quizname=quizname,username=username,score=score,ques=ques,cop=cop)

@app.route("/classs", methods=["POST","GET"])
def classs():
    #global my_class 
    #my_class = request.form["my_class"]
    session["class_my"] = request.form["my_class"]
    return render_template("quizadd.html")

@app.route("/addclass")
def addclass():
    return render_template("addclass.html")

@app.route("/classadd", methods = ["POST","GET"])
def classadded():
    name = request.form["name"]
    #session["class"] = name
    username = session.get("user")
    con = sqlite3.connect(curdir + "\Project.db")
    cur = con.cursor()
    classes = cur.execute("SELECT name FROM classes").fetchall()
    n=len(classes)
    suc = False
    for j in range(n):
        if name == classes[j][0]:
            flash("Class name already exists","danger")
            suc=True
            return render_template("teacher.html")
        else:
            pass
    if suc == False:
        cur.execute("INSERT INTO classes VALUES (?,?)",(name,username,))
        con.commit()
        flash("class added successfully","success")
        return render_template("addquiz.html")

@app.route("/addquiz", methods=["POST","GET"])
def addquiz():
    return render_template("addquiz.html")

@app.route("/prac")
def prac():
    return render_template("prac.html")

@app.route("/previous",methods = ["POST","GET"])
def previousQuiz():
    con = sqlite3.connect(curdir + "\Project.db")
    cur = con.cursor()
    classname = session.get("class_my")
    #classname = request.form["classname"]
    prevquiz = cur.execute("SELECT Quiz FROM Quizzes WHERE classname=:classname",{"classname":classname}).fetchall()
    return render_template("prevquiz.html",prevquiz = prevquiz)

@app.route("/tresult",methods=["POST","GET"])
def tresult():
    quizname = request.form["qname"]
    con = sqlite3.connect(curdir + "\Project.db")
    cur = con.cursor()
    username = cur.execute("SELECT username FROM Result WHERE quizname=:quizname",{"quizname":quizname}).fetchall()
    result = cur.execute("SELECT score FROM Result WHERE quizname=:quizname",{"quizname":quizname}).fetchall()
    l = len(username)
    return render_template("resultdisplay.html",username=username,result=result,l=l)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000,debug=True)


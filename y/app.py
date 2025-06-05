from flask import*
import mysql.connector
import uuid
import time
from datetime import datetime, timedelta
import random
import base64
from PIL import Image
import io




db=mysql.connector.connect(host="badtc9hbjyr3i3a8txwm-mysql.services.clever-cloud.com",database="badtc9hbjyr3i3a8txwm",user="uwyfce9gwkj7ctmo",password="hwlAfTMxHE0XSfWDXgy6")
cur=db.cursor(buffered=True)

app=Flask(__name__)



@app.route("/cookie")
def cookie():
    cc=request.cookies.get("userid")
    if cc:
        cur.execute("select userhandle from users where  userid=%s or cookies=%s",(cc,cc,))
        sel=cur.fetchone()
        if sel:
            sel=str(sel[0])

            cur.execute("select suspended from users where userhandle=%s",(sel,))
            auser=cur.fetchone()
            auser=str(auser[0])

            if auser !="f":
                return render_template("suspended.html")
            else:
                return redirect(url_for("home"))
        else:
            return redirect(url_for("page"))
    else:
        return redirect(url_for("page"))


@app.route("/checking user suspension")
def checksus():

    co=request.cookies.get("userid")
    abc=str(co)

    cur.execute("select suspended from users where cookies=%s or userid=%s",(abc,abc,))
    us=cur.fetchone()
    

    try :
        us=str(us[0])
        if us !="f":
            return render_template("suspended.html")
        else:
            return redirect(url_for("home"))
    except:
        return f"AN ERROR JUST OCCURED HERE CONTACT OUR TEAM ....ERR_CODE[USERID OR COOKIE NOT FOUND IN DB]{us} {abc}"
        

    return f"{us}"
    

    

@app.route("/")
def main():

   

    

   

    return render_template("loading.html")

   

   
@app.route("/search",methods=["POST","GET"])
def search():
    cur.execute("select name,userhandle,dp,verified from users where verified='t'")
    abc=cur.fetchall()

    lis=[]

    for nm,uh,dp,ver in abc:
        nm=str(nm)
        uh=str(uh)
        dp=str(dp)
        ver=str(ver[0])

        if ver=="t":
                ver=f'https://i.pinimg.com/originals/da/61/fa/da61fa152c102c46c16786b9f79402f8.gif'
        else:
                ver=f"https://www.pngplay.com/wp-content/uploads/5/Dot-Symbol-Free-PNG.png" 
            
           
            

        lis.append({"n":nm,"uh":uh,"dp":dp,"ve":ver})

    if request.method=="POST":
        userh=request.form["se"]
        userh = f"%{userh}%"
        
        
        cur.execute("select name,userhandle,dp,verified from users where userhandle like %s or name like %s",(userh,userh))
        abc=cur.fetchall()
        lis=[]
        for nm,uh,dp,ver in abc:
            nm=str(nm)
            uh=str(uh)
            dp=str(dp)
            ver=str(ver[0])
            if ver=="t":
                ver=f'https://i.pinimg.com/originals/da/61/fa/da61fa152c102c46c16786b9f79402f8.gif'
            else:
                ver=f"https://www.pngplay.com/wp-content/uploads/5/Dot-Symbol-Free-PNG.png" 
            
            lis.append({"n":nm,"uh":uh,"dp":dp,"ve":ver})
        return render_template("search.html",lis=lis)

        

    return render_template("search.html",lis=lis)
        
        
@app.route("/user-profile/<userh>")
def idofuser(userh):
    l=" "

    error=" "
    

    user=userh
   

    cur.execute("select name,userhandle,doj,verified,dp,background from users where userhandle=%s",(user,))
    data=cur.fetchall()

    if data:
        lis=[]
        for n,uh,doj,ver,dp,bg in data:
            n=str(n)
            uh=str(uh)
            doj=str(doj)
            v=str(ver[0])
            dp=str(dp)
            bg=str(bg)

            if v=="t":
                vv=f'https://i.pinimg.com/originals/da/61/fa/da61fa152c102c46c16786b9f79402f8.gif'
            else:
                vv=f"https://www.pngplay.com/wp-content/uploads/5/Dot-Symbol-Free-PNG.png"


            lis.append({"n":n,"uh":uh,"doj":doj,"v":vv,"dp":dp,"bg":bg})


    cur.execute("select name,userhandle,date,content,verification,image,dp from posts where userhandle=%s",(user,))
    da=cur.fetchall()

    if da:
        l=[]
        for n,uh,dt,cont,v,img,dp in da:
            
            
            n=str(n)
            uh=str(uh)
            dt=str(dt)
            cont=str(cont)
            v=str(v[0])
            dp=str(dp)


            if v=="t":
                vv=f'https://i.pinimg.com/originals/da/61/fa/da61fa152c102c46c16786b9f79402f8.gif'
            else:
                vv=f"https://www.pngplay.com/wp-content/uploads/5/Dot-Symbol-Free-PNG.png" 
            
           

            image_data = None
            if img is not None:
              try:
                binary_data = base64.b64decode(img)  
                Image.open(io.BytesIO(binary_data)).verify()  
                image_data = f"data:image/jpeg;base64,{img.decode('utf-8')}"  
              except Exception as e:
                print(f"Error loading image: {e}")
                image_data =f" "
            else:
                image_data =f"https://via.placeholder.com/1x1/000000/000000.png?text=%20"
                

            l.append({"n": n, "uh": uh, "dt": dt, "cont": cont, "vv": vv, "img": image_data,"dp":dp})
                
            

           

            
    else:
        pass



    return render_template("profile.html",lis=lis,l=l)
            
    
        
        



@app.route("/checking user suspension for search access")
def checksussear():

    co=request.cookies.get("userid")
    abc=str(co)

    cur.execute("select suspended from users where cookies=%s or userid=%s",(abc,abc,))
    us=cur.fetchone()
    

    try :
        us=str(us[0])
        if us !="f":
            return render_template("suspended.html")
        else:
            return redirect(url_for("search"))
    except:
        return f"AN ERROR JUST OCCURED HERE CONTACT OUR TEAM ....ERR_CODE[USERID OR COOKIE NOT FOUND IN DB]{us} {abc}"
        

    return f"{us}"
    

    

@app.route("/signin & signup")
def page():
    return render_template("main.html")
   


@app.route("/Home")
def home():


    image=" "
    

    cur.execute("select name,userhandle,date,content,verification,image,dp from posts")
    data=cur.fetchall()

    if data:
        lis=[]
        for n,uh,dt,c,v,img,dp in data:
            
            
            n=str(n)
            uh=str(uh)
            dt=str(dt)
            c=str(c)
            v=str(v[0])
            dp=str(dp)


            if v=="t":
                vv=f'https://i.pinimg.com/originals/da/61/fa/da61fa152c102c46c16786b9f79402f8.gif'
            else:
                vv=f"https://www.pngplay.com/wp-content/uploads/5/Dot-Symbol-Free-PNG.png" 
            
           

            image_data = None
            if img is not None:
              try:
                binary_data = base64.b64decode(img)  
                Image.open(io.BytesIO(binary_data)).verify()  
                image_data = f"data:image/jpeg;base64,{img.decode('utf-8')}"  
              except Exception as e:
                print(f"Error loading image: {e}")
                image_data =f" "
            else:
                image_data =f"https://via.placeholder.com/1x1/000000/000000.png?text=%20"

          

            lis.append({"n": n, "uh": uh, "dt": dt, "c": c, "vv": vv, "img": image_data,"dp":dp})
                
            

           

            
    else:
        pass







            
    return render_template("home.html",lis=lis,vv=vv)


@app.route("/signup",methods=["POST","GET"])
def signup():

    error=" "
    au= " "

    if request.method=="POST":
        n=request.form["name"]
        h=request.form["username"]
        p=request.form["password"]

        hand=str("@"+h)

        cur.execute("select userhandle from users where  userhandle=%s",(hand,))
        abc=cur.fetchone()

        
      

        if abc:
            error=" "
            return render_template("signup.html",er=error)
            
            
            
            
            
        else:
            cname=uuid.uuid4()
            c=str(cname)

            d = datetime.now().strftime('%Y-%m-%d')

            h=str("@"+h)

            img=f"https://static.vecteezy.com/system/resources/previews/009/292/244/non_2x/default-avatar-icon-of-social-media-user-vector.jpg"

            bg=f"https://img.freepik.com/free-photo/abstract-luxury-blur-dark-grey-black-gradient-used-as-background-studio-wall-display-your-products_1258-63996.jpg?semt=ais_items_boosted&w=740"
           

            
            data=cur.execute("insert into users (name,userhandle,doj,password,dp,background) values(%s,%s,%s,%s,%s,%s)",(n,h,d,p,img,bg))
            db.commit()

            return redirect(url_for("signin"))
        

    
    return render_template("signup.html")


@app.route("/signin",methods=["POST","GET"])
def signin():

    error=" "

    if request.method=="POST":
        name=request.form["username"]
        pas=request.form["password"]

        cname=uuid.uuid4()
        c=str(cname)

        name=str("@"+name)

        cur.execute("select * from users where userhandle=%s and password=%s",(name,pas,))
        a=cur.fetchall()

        if a:

            cur.execute("select userid from users where userhandle=%s",(name,))
            ce=cur.fetchone()
            ce=str(ce[0])
          

            if ce!="1o1":
                
                cie=str(ce)
                
                d = datetime.now().strftime('%Y-%m-%d')

                no='''<html><body><svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="red" class="bi bi-exclamation-triangle-fill" viewBox="0 0 16 16">
  <path d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5m.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2"/>
</svg>There was a login to your account <br> If it wasn't you then change your <a  href='/Reset-password'>password</a></body></html>'''

             
                cur.execute("insert into  notification (notifications, userhandle) values (%s, %s)", (no, name,))

                db.commit()

                expire_seconds = int(timedelta(days=365 * 10).total_seconds())

                abc=make_response(redirect(url_for("checksus")))
                abc.set_cookie("userid",cie,max_age=expire_seconds)
                return abc


            else:
                 cname=uuid.uuid4()
                 c=str(cname)

            

                 cur.execute("update  users set cookies=%s where userhandle=%s",(c,name))
                 db.commit()

                 d = datetime.now().strftime('%Y-%m-%d')

                 no='''<html><body><svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="red" class="bi bi-exclamation-triangle-fill" viewBox="0 0 16 16">
  <path d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5m.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2"/>
</svg>There was a login to your account <br> If it wasn't you then change your <a  href='/Reset-password'>password</a></body></html>'''




                 
                 cur.execute("INSERT INTO notification (notifications, userhandle) VALUES (%s, %s)", (no, name,))

                 db.commit()

                 expire_seconds = int(timedelta(days=365 * 10).total_seconds())

                 abc=make_response(redirect(url_for("checksus")))
                 abc.set_cookie("userid",c,max_age=expire_seconds)
                 return abc
            
            
                
            
        else:
            error=" "
            return render_template("signin.html",er=error)

            
            

        
        
    return render_template("signin.html")

@app.route("/Notifications")
def noti():

    i=" "

    c=request.cookies.get("userid")
    c=str(c)
    cur.execute("select userhandle from users where userid=%s or cookies=%s",(c,c,))
    
    abc=cur.fetchone()

    abc=abc[0]


   
    cur.execute("select notifications from notification where userhandle=%s",(abc,))
    noti=cur.fetchall()

    if noti:
        lis = []
        for v in noti:
            
            i=str(v[0])
            lis.append({"content":i})
        return render_template("notifications.html",lis=lis)
    else:
        nolis=" "
        return render_template("notifications.html",nolis=nolis)
        
        


    
    return render_template("notifications.html")


@app.route("/Add",methods=["POST","GET"])
def addpost():
    c=request.cookies.get("userid")
    c=str(c)



    if request.method=="POST":
        cur.execute("select userhandle,dp,verified,name from users where userid=%s or cookies=%s",(c,c,))
        handle=cur.fetchall()

        for uh,dp,v,n in handle:
            uh=str(uh)
            dp=str(dp)
            v=str(v[0])
            n=str(n)
            
        d = datetime.now().strftime('%Y-%m-%d')
        
        co=request.form["content"]
        i=request.files["img"]

        if i is not None:
              file_data = i.read()
              file = base64.b64encode(file_data).decode("utf-8")
              image=file
        else:
            image="  "

        

        co=str(co)

        cur.execute("insert into posts (dp,name,userhandle,date,content,verification,image) values(%s,%s,%s,%s,%s,%s,%s)",(dp,n,uh,d,co,v,image,))
        db.commit()

        return redirect(url_for("home"))


    return render_template("post.html")


@app.route("/Checking user status of suspension")
def add():

    co=request.cookies.get("userid")
    abc=str(co)

    cur.execute("select suspended from users where cookies=%s",(abc,))
    us=cur.fetchone()
    us=str(us[0])

    if us !="f":
        return render_template("suspended.html")
    else:
        return redirect(url_for("addpost"))
        

    return f"{us}"
    
        

@app.route("/Profile")
def profile():

    l=" "

    error=" "
    

    c=request.cookies.get("userid")
    c=str(c)
    cur.execute("select userhandle from users where userid=%s or cookies=%s",(c,c,))
    
    abc=cur.fetchone()

    user=abc[0]

    cur.execute("select name,userhandle,doj,verified,dp,background from users where userhandle=%s",(user,))
    data=cur.fetchall()

    if data:
        lis=[]
        for n,uh,doj,ver,dp,bg in data:
            n=str(n)
            uh=str(uh)
            doj=str(doj)
            v=str(ver[0])
            dp=str(dp)
            bg=str(bg)

            if v=="t":
                vv=f'https://i.pinimg.com/originals/da/61/fa/da61fa152c102c46c16786b9f79402f8.gif'
            else:
                vv=f"https://www.pngplay.com/wp-content/uploads/5/Dot-Symbol-Free-PNG.png"


            lis.append({"n":n,"uh":uh,"doj":doj,"v":vv,"dp":dp,"bg":bg})


    cur.execute("select name,userhandle,date,content,verification,image,dp from posts where userhandle=%s",(user,))
    da=cur.fetchall()

    if da:
        l=[]
        for n,uh,dt,cont,v,img,dp in da:
            
            
            n=str(n)
            uh=str(uh)
            dt=str(dt)
            cont=str(cont)
            v=str(v[0])
            dp=str(dp)


            if v=="t":
                vv=f'https://i.pinimg.com/originals/da/61/fa/da61fa152c102c46c16786b9f79402f8.gif'
            else:
                vv=f"https://www.pngplay.com/wp-content/uploads/5/Dot-Symbol-Free-PNG.png" 
            
           

            image_data = None
            if img is not None:
              try:
                binary_data = base64.b64decode(img)  
                Image.open(io.BytesIO(binary_data)).verify()  
                image_data = f"data:image/jpeg;base64,{img.decode('utf-8')}"  
              except Exception as e:
                print(f"Error loading image: {e}")
                image_data =f" "
            else:
                image_data =f"https://via.placeholder.com/1x1/000000/000000.png?text=%20"
                

            l.append({"n": n, "uh": uh, "dt": dt, "cont": cont, "vv": vv, "img": image_data,"dp":dp})
                
            

           

            
    else:
        pass



    return render_template("profile.html",lis=lis,l=l)
            
           

    
        
@app.route("/Forgot-password",methods=["POST","GET"])
def forgotpassword():

    er=None

    
    if request.method=="POST":
            abc=request.form["username"]
            bc="@"+abc

            try:
                noti='''<html><body><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-file-earmark-lock-fill" viewBox="0 0 16 16">
  <path d="M7 7a1 1 0 0 1 2 0v1H7zM6 9.3c0-.042.02-.107.105-.175A.64.64 0 0 1 6.5 9h3a.64.64 0 0 1 .395.125c.085.068.105.133.105.175v2.4c0 .042-.02.107-.105.175A.64.64 0 0 1 9.5 12h-3a.64.64 0 0 1-.395-.125C6.02 11.807 6 11.742 6 11.7z"/>
  <path d="M9.293 0H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V4.707A1 1 0 0 0 13.707 4L10 .293A1 1 0 0 0 9.293 0M9.5 3.5v-2l3 3h-2a1 1 0 0 1-1-1M10 7v1.076c.54.166 1 .597 1 1.224v2.4c0 .816-.781 1.3-1.5 1.3h-3c-.719 0-1.5-.484-1.5-1.3V9.3c0-.627.46-1.058 1-1.224V7a2 2 0 1 1 4 0"/>
</svg> There was a request to change your password <br> <p style='color:blue'><a  href='/Reset-password'> click here to change your password</a></p></body></html>'''

                cur.execute("select userhandle from users where userhandle=%s",(bc,))
                vb=cur.fetchall()

                if vb:
                    cur.execute("insert into notification(notifications,userhandle) values(%s,%s)",(noti,bc,))
                    a=db.commit()

               
                    return render_template("forgotmain.html")

                else:
                    er=" "
            except:
                er=" "
        
    return render_template("forgotform.html",er=er)


@app.route("/Appeal form",methods=["POST","GET"])
def appealform():
    c=request.cookies.get("userid")
    c=str(c)

    
    if request.method=="POST":
        e=request.form["email"]
        d=request.form["de"]


        cur.execute("select userhandle from users where cookies=%s",(c,))
        uh=cur.fetchone()
        uh=str(uh[0])

        idc=str(random.random())

        lis=["a","b","c","d"]
        lis2=["e","f","g","h"]

        one=lis[random.randrange(0,4)]
        two=lis2[random.randrange(0,4)]

        idc=str("#"+one+two+idc)


        cur.execute("insert into appeal (userhandle,id,email,description) values(%s,%s,%s,%s)",(uh,idc,e,d,))
        db.commit()

        return redirect(url_for("checkappeal"))

    
    return render_template("appealform.html")


@app.route("/appeal recieved")
def wegotappeal():

    c=request.cookies.get("userid")
    c=str(c)

    cur.execute("select userhandle from users where cookies=%s",(c,))
    abc=cur.fetchone()

    abc=str(abc[0])

    cur.execute("select id from appeal where userhandle=%s",(abc,))
    i=cur.fetchone()
    i=str(i[0])

    cur.execute("select status from appeal where userhandle=%s",(abc,))
    st=cur.fetchone()
    st=str(st[0])

    cur.execute("select email from appeal where userhandle=%s",(abc,))
    em=cur.fetchone()
    em=str(em[0])

    

    

   
    

    return render_template("appealgot.html",i=i,st=st,em=em)
    
@app.route("/checking appeal status")
def checkappeal():

    abc=None
    abd=None
    
    c=request.cookies.get("userid")
    c=str(c)

    cur.execute("select userhandle from users where cookies=%s",(c,))
    abc=cur.fetchone()

    abc=str(abc[0])

    cur.execute("select id from appeal where userhandle=%s",(abc,))
    abd=cur.fetchone()

   
    


    try:
        

       

        abd=str(abd[0])

        
        
        if abd:
            return redirect (url_for("wegotappeal"))
            #return f"{abd}"
            
        else:
             return redirect(url_for("appealform"))
              #return "we have a appeal from you already"
    except:
        return redirect(url_for("appealform"))
        #return f"{abd}"
    

    
        

    
    

    


@app.route("/Terms-of-use")
def terms():
    return render_template("terms.html")

@app.route("/Reset-password",methods=["POST","GET"])
def reset():
    cc=request.cookies.get("userid")
    if cc:
        cur.execute("select userhandle from users where  userid=%s or cookies=%s",(cc,cc,))
        sel=cur.fetchone()
        if sel:

            if request.method=="POST":
                pas=request.form["pass"]

                pas=str(pas)
                sel=str(sel[0])

                
               

                cur.execute("update users set password=%s where userhandle=%s",(pas,sel,))
                db.commit()

                

               

                
               

              

               
                return render_template("resetmain.html")
                
            
            
            return render_template("resetform.html")
        else:
            return redirect(url_for("page"))
    else:
        return redirect(url_for("page"))

@app.route("/Deleting cookies of the user ")
def delcookie():

    abv=make_response(redirect(url_for("signin")))
    abv.delete_cookie("userid")

    return abv
    


if __name__=="__main__":
    #app.run(host="192.168.29.241",debug=True,port=9121)
    app.run(host="0.0.0.0", debug=True, port=9121)#worldwide server access

    '''  lt --port 9121 --subdomain ydotcom ''' #used in cmd for worldwide access *NOTE=before this command run this app.py in idle python


    ''' curl https://ydotcom.loca.lt -Headers @{ "bypass-tunnel-reminder" = "true" } ''' #used in powershell to bypass password
    

    #app.run(debug=True)
    #app.config["server_name"]="y.com:9121"

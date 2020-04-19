from flask import Flask, render_template, request, redirect, session, url_for
import pyrebase

app = Flask(__name__)
app.secret_key="super secret"

# tengin við firebase realtime database á firebase.google.com ( db hjá danielsimongalvez@gmail.com )
config = {
    # hér kemur tengingin þín við Firebase gagnagrunninn ( realtime database )
    "apiKey": "AIzaSyB0eRPF6oiDbrXE3Gw8NwO4nCN0mWqiF5o",
    "authDomain": "verk5-facfc.firebaseapp.com",
    "databaseURL": "https://verk5-facfc.firebaseio.com",
    "projectId": "verk5-facfc",
    "storageBucket": "verk5-facfc.appspot.com",
    "messagingSenderId": "633842083010",
    "appId": "1:633842083010:web:0ccc6794b4740bd881475b",
    "measurementId": "G-LKD51D1D92"
}

fb = pyrebase.initialize_app(config)
db = fb.database()


# Test route til að sækja öll gögn úr db
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/info',methods=['GET','POST'])
def info():
    login=False
    if request.method=='POST':
        usr = request.form['username']
        pwd = request.form['psw']
        #gá hvort hægt se að login
        u = db.child("user").get().val()
        lst = list(u.items())
        for i in lst:
            if usr==i[1]['usr'] and pwd==i[1]['pwd']:
                login=True
                break
        if login:
            #hefur aðgang
            session['logged_in']=usr
            return redirect("/topsecret")
        else:
            #hefur ekki aðgang
            return render_template("nologin.html")
    else:
        return render_template("no_method.html")

@app.route('/register')
def register():
    return render_template("register.html")


@app.route('/doregister',methods=['GET','POST'])
def doregister():
    usernames=[]
    if request.method=='POST':
        usr=request.form['username']
        pwd=request.form['psw']

        #forum og athugum hvort notandi se til i grunni
        u=db.child("user").get().val()
        lst=list(u.items())
        for i in lst:   
            usernames.append(i[1]['usr'])

        if usr not in usernames:
            db.child("user").push({"usr":usr,"pwd":pwd})
            return render_template("registered.html")
        else:
            return render_template("userexsists.html")
    else:
        return render_template("no_method.html")

@app.route('/logout')
def logout():
    session.pop("logged_in",None)
    return render_template('index.html')

@app.route('/topsecret')
def topsecret():
    if 'logged_in' in session:
        return render_template("topsecret.html")
    else:
        return redirect('/')

if __name__ == "__main__":
	app.run(debug=True)









#    u = db.child("notandi").get().val()
#    lst = list(u.items())
#    print(lst[0][1]['notendanafn'])
#    return "Lesum úr grunni"



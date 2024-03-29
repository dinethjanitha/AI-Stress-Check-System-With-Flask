import os
from flask import Flask, render_template, Response , request , redirect , url_for , flash , make_response
import cv2
import numpy as np
from tensorflow.keras.models import load_model
import subprocess as sp
from flask_mysqldb import MySQL


app = Flask(__name__)

# Load the model from the emotion.h5 file
model = load_model('emotion2_model.h5')

# Load the face cascade classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

cap = None  # VideoCapture object
out = None  # VideoWriter object

recording_start_time = None
recording_duration = 60  # Recording duration in seconds
is_running = True

#databse connection 

last_emotion = {'Angry': 0, 'Disgust': 0, 'Fear':0,'Happy':0,'Sad':0,'Surprise':0,'Neutral':0}

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'userdb'
mysql = MySQL(app)






def detect_emotions():
    global cap, out, recording_start_time, is_running

    cap = cv2.VideoCapture(0)
    recording_start_time = cv2.getTickCount()  # Start the timer
    
    while cap.isOpened() and is_running:
        ret, frame = cap.read()

        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            face_image = frame[y:y + h, x:x + w]

            gray = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
            gray = cv2.resize(gray, (48, 48))  # Resize the image to match the input size of the model
            gray = gray.reshape(1, 48, 48, 1)  # Reshape for model input
            gray = gray / 255.0  # Normalize pixel values

            # Perform emotion recognition prediction
            emotion_prediction = model.predict(gray)
            emotion_label = emotion_labels[np.argmax(emotion_prediction)]
            emotion_level = np.max(emotion_prediction)

            # Draw a rectangle around the face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # Display the emotion label and level
            label_text = f"{emotion_label}: {emotion_level:.2f}"
            cv2.putText(frame, label_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

            print("you now mode is " + emotion_label)

            if(emotion_label == 'Angry'):
                last_emotion['Angry'] = last_emotion['Angry'] + emotion_level
            elif(emotion_label == 'Disgust'):
                last_emotion['Disgust'] = last_emotion['Disgust'] + emotion_level 
            elif(emotion_label == 'Fear'):
                last_emotion['Fear'] = last_emotion['Fear'] + emotion_level
            elif(emotion_label == 'Happy'):
                last_emotion['Happy'] = last_emotion['Happy'] + emotion_level
            elif(emotion_label == 'Neutral'):
                last_emotion['Neutral'] = last_emotion['Neutral'] + emotion_level
            elif(emotion_label == 'Sad'):
                last_emotion['Sad'] = last_emotion['Sad'] + emotion_level  
            else:
                last_emotion['Surprise'] = last_emotion['Surprise'] + emotion_level
            


        # Write the frame to the video file
        if out is not None:
            out.write(frame)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        

        
        # Check if recording duration has elapsed
        if (cv2.getTickCount() - recording_start_time) / cv2.getTickFrequency() >= recording_duration:
            is_running = False
            print(last_emotion['Angry'])
            print(last_emotion['Disgust'])
            print(last_emotion['Fear'])
            print(last_emotion['Happy'])
            print(last_emotion['Neutral'])
            print(last_emotion['Sad'])
            print(last_emotion['Surprise'])
            
            Angryne = last_emotion['Angry']
            Angryf = f'{Angryne:.3f}'
            global Angrynew
            Angrynew = float(Angryf)

            Disgustne = last_emotion['Disgust']
            Disgustf = f'{Disgustne:.3f}'
            global Disgustnew
            Disgustnew = float(Disgustf)

            Fearne = last_emotion['Fear']
            Fearf = f'{Fearne:.3f}'
            global Fearnew
            Fearnew = float(Fearf)

            Happyne = last_emotion['Happy']
            Happyf = f'{Happyne:.3f}'
            global Happynew
            Happynew = float(Happyf)

            Naturalne = last_emotion['Neutral']
            Naturalf = f'{Naturalne:.3f}'
            global Naturalnew
            Naturalnew = float(Naturalf)

            Sadne = last_emotion['Sad']
            Sadf = f'{Sadne:.3f}'
            global Sadnew
            Sadnew = float(Sadf)

            Surprisene = last_emotion['Surprise']
            Surprisef = f'{Surprisene:.3f}'
            global Surprisenew
            Surprisenew = float(Surprisef)

            print(Surprisenew)
            
            print(type(Surprisenew))
            
            print(Sadnew)

            print(type(Sadnew))

            
            print(Naturalnew)
            print(type(Naturalnew))


          

            
            

            
            break
   
    cv2.destroyAllWindows()
    if cap is not None:
        cap.release()
    if out is not None:
        out.release()



@app.route('/con')
def check_connection():
    
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT 1')
        cur.close()
        return 'Database connection is working.'
    except Exception as e:
        return f'Database connection error: {str(e)}'

@app.route('/video_feed')
def video_feed():
    return Response(detect_emotions(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/emotion')
def emotion():
    username = request.cookies.get('username')


    if username:
        return render_template('emotion.html' ,username= username)

    else:
        return redirect(url_for('login'))




@app.route('/login' , methods=  ['GET' , 'POST'])
def login():

    error = ""
    action = "Test PASS"
    if request.method == 'POST':
        if login_fuc(request.form['username'] , request.form['password']):
            response = make_response(redirect(url_for('welcome')))
            response.set_cookie('username', request.form['username'])
            global  username 
            username = request.cookies.get('username')
            return response
        else:
            error = "Username or Password incorrect"
    return render_template('login.html' , error=error)    

def login_fuc(username , password):

    cur = mysql.connection.cursor()
    cur.execute('SELECT username,password FROM userdata WHERE username = %s AND password = %s' ,(username,password))
    if cur.rowcount == 1:
        cur.close()
        return True
    else:
        cur.close()
        return False


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM userdata WHERE username = %s", (username,))
        result = cur.fetchone()

        if result:
            flash("Username Already Exists")
            return redirect('signup')

        email = request.form['email']
        password = request.form['password']
        
        if add_data(username, email, password):
            flash("Sign up successful! Please log in.")
            return redirect('login')
        else:
            flash("Error occurred while signing up. Please try again.")
            return redirect('signup')

    return render_template('signup.html')

def add_data(username, email, password):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO userdata (username, email, password) VALUES (%s, %s, %s)",
                (username, email, password))
    if cur.rowcount > 0:
        mysql.connection.commit()
        cur.close()
        return True
    else:
        cur.close()
        return False

   
        

@app.route('/logout')
def logout():
    responce = make_response(redirect(url_for("login")))
    responce.set_cookie('username', '', expires= 0)
    return responce

@app.route('/add_data')
def add_values():
      username = request.cookies.get('username')
      cur = mysql.connection.cursor()
      cur.execute("UPDATE userdata SET Angry = %s WHERE username = %s", (Angrynew, username))
      cur.execute("UPDATE userdata SET Disgust = %s WHERE username = %s", (Disgustnew, username))
      cur.execute("UPDATE userdata SET Fear = %s WHERE username = %s", (Fearnew, username))
      cur.execute("UPDATE userdata SET Happy = %s WHERE username = %s", (Happynew, username))
      cur.execute("UPDATE userdata SET Neutral = %s WHERE username = %s", (Naturalnew, username))
      cur.execute("UPDATE userdata SET Sad = %s WHERE username = %s", (Sadnew, username))
      cur.execute("UPDATE userdata SET Surprise = %s WHERE username = %s", (Surprisenew, username))
      mysql.connection.commit()
      cur.close()
    
      responce = make_response(redirect(url_for("emotion")))
      return responce

@app.route('/')
def welcome():
    username = request.cookies.get('username')
    return render_template('home.html' , username = username)
    


@app.route('/about')
def about():
    username = request.cookies.get('username')
    return render_template('About.html' , username = username)


@app.route('/breathing')
def breathing():
    username = request.cookies.get('username')
    return render_template('breathing.html' , username = username)

@app.route('/contact')
def contact():
    username = request.cookies.get('username')
    return render_template('contact.html' , username = username)

@app.route('/contactform')
def contactform():
    return render_template('contactform.html')

@app.route('/emodetect')
def emodetect():
    return render_template('breathing.html')

@app.route('/exersise')
def exersise():
    username = request.cookies.get('username')
    return render_template('exersise.html' , username = username)
@app.route('/game')
def game():
    return render_template('game.html')


@app.route('/getstart')
def getstart():
    return render_template('getstart.html')

@app.route('/listening')
def listening():
 
    username = request.cookies.get('username')


    if username:
        return render_template('listening.html')

    else:
        return redirect(url_for('login'))

    

@app.route('/stressmanagement')
def stressmanagement():
    username = request.cookies.get('username')
    return render_template('stressmanagement.html' , username = username)

@app.route('/heart')
def heart():
    return render_template('heart.html')

# admin page

@app.route('/admin')
def admin():
    adminusername = request.cookies.get('adminusername')


    if adminusername:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM userdata")
        data = cur.fetchall()
        cur.close()
    
        return render_template('admin.html', data=data , adminusername= adminusername) 


    else:
        return redirect(url_for('adminlogin'))
    
    
    
    

@app.route('/adminlogin' , methods=  ['GET' , 'POST'])
def adminlogin():
    error = ''
    if request.method == 'POST':
        if adminlogin(request.form['username'] , request.form['password']):
            response = make_response(redirect(url_for('admin')))
            response.set_cookie('adminusername', request.form['username'])
            return response
        else:
            error = "Incorrect username or password"
    return render_template('adminlogin.html' , error = error)

def adminlogin(username,password):
    cur = mysql.connection.cursor()
    cur.execute('SELECT username,password FROM admindb WHERE username = %s AND password = %s' ,(username,password))
    if cur.rowcount == 1:
        cur.close()
        return True
    else:
        cur.close()
        return False    

@app.route('/adminlogout')
def adminlogout():
    responce = make_response(redirect(url_for("adminlogin")))
    responce.set_cookie('adminusername', '', expires= 0)
    return responce

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.debug = True
    app.run()



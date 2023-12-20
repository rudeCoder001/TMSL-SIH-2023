from flask import *
from pyrebase import *
from algorithm import Algorithm
import requests
import time 
from datetime import timedelta
from flask_socketio import SocketIO, emit
from threading import Thread, Event
import os
from googleapiclient.discovery import build


app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_KEY'

#---------------initializeing application------------------------
app = Flask(__name__, template_folder='templates', static_folder='static')

#---------------configuring firebase----------------------------


firebaseConfig = {'apiKey': "AIzaSyAJA-UV_R0OHj06NK9LZa90pqTrNelopPc",
  'authDomain': "gyaan-connect-b7b08.firebaseapp.com",
  'projectId': "gyaan-connect-b7b08",
  'storageBucket': "gyaan-connect-b7b08.appspot.com",
  'messagingSenderId': "800780596390",
  'appId': "1:800780596390:web:4c4029a1f7d91eb3333067",
  'measurementId': "G-19P192XXE0",
  'databaseURL': ""}


app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
app.permanent_session_lifetime = timedelta(days=31)

firebase = initialize_app(firebaseConfig)

auth = firebase.auth()

#-------------------------security key (do not change/remove this code)---------------------------------------

app.secret_key = "SECRET_KEY"

#-----------------------page routes-----------------------------------------
#time calculation

def calculate_total_time():
    if 'user' in session and 'start_time' in session:
        elapsed_time = time.time() - session['start_time']
        total_time_spent = session.get('total_time_spent', 0) + elapsed_time
        session['total_time_spent'] = total_time_spent
      ##  print(f"Total Time Spent: {total_time_spent} seconds")
        session.pop('start_time', None)
        return total_time_spent
    
def youtube_search_topic(api_key, query, max_results=10):
        # Set up the YouTube Data API
        youtube = build('youtube', 'v3', developerKey=api_key)

        # Call the search.list method to retrieve search results
        search_response = youtube.search().list(
            q=query,
            type='video',
            part='id,snippet',
            maxResults=max_results
        ).execute()

        # Extract video details from the search results
        videos = []
        for search_result in search_response.get('items', []):
            video = {
                'title': search_result['snippet']['title'],
                'video_id': search_result['id']['videoId'],
                'url': f'https://www.youtube.com/watch?v={search_result["id"]["videoId"]}'
            }
            videos.append(video)

        return videos
        
#time calculation
@app.before_request
def before_request():
    if 'user' in session and 'start_time' not in session:
        session['start_time'] = time.time()
#time calculation
@app.teardown_request
def teardown_request(exception=None):
    calculate_total_time()




@app.route('/')
def home():
    
    if 'user' in session:

        #signed user
        
        user_id_token = session['user']["idToken"]
        try:
            auth.refresh(session['user']['refreshToken'])
            user = auth.get_account_info(user_id_token)['users'][0]
            first_name = user.get('displayName', '').split()[0] if 'displayName' in user else "!"
            button1id = "hello"
            video1 = "https://youtu.be/RJ733wzbNoA?si=IvSEKKoq30G3qidP"
            like1="1000"
            view1="10K"
            thumbnail1="Python tutorial for beginners"
            channel1="Code with Harry"
            cardimage1="https://i.ytimg.com/vi/fr1f84rg4Nw/hqdefault.jpg"
            title1 = "Python Full Course for free 🐍"

            button2id = "hello"
            video2 = "Python for beginners"
            title2 = "15 Minute Python Tutorial For Beginners In Hindi (Full &amp; Complete Python Crash Course)"
            like2="1000"
            view2="20K"
            thumbnail2="DSA Foundation Course"
            channel2="PW"
            cardimage2="https://i.ytimg.com/vi/_uQrJ0TkZlc/hqdefault.jpg"
            print(video2)
            return render_template('index.html', first_name=first_name, video2=video2, button2id=button2id,
                                   title2=title2, video1=video1, button1id=button1id, title1=title1,like1=like1,like2=like2,channel1=channel1,view1=view1,thumbnail1=thumbnail1,view2=view2,thumbnail2=thumbnail2,channel2=channel2,cardimage1=cardimage1,cardimage2=cardimage2)
        except Exception as e:
            print(f"Error getting account info: {e}")
            # Handle the error, for now, redirect to the login page
            return redirect('/login')
    else:
        #unsigned user
        return render_template('index2.html')






@app.route('/signup', methods = ['GET','POST'])

def signup():

    if request.method == 'POST':

        newname = request.form['newname']
        newemail = request.form['newemail']
        newpassword = request.form['newpassword']
        is_teacher = 'flag' in request.form

        try:
            
            user = auth.create_user_with_email_and_password(newemail, newpassword)

            auth.update_profile(user["idToken"], display_name = newname)

            
            if is_teacher==True :

                if request.method == 'POST':

                
                    inputUsername = request.form.get('inputUsername') 
                    inputFirstname =  request.form.get('inputFirstname')
                    inputLastname = request.form.get('inputLastname')
                    inputexpertise =request.form.get('inputexpertise')
                    inputwebsite = request.form.get('inputwebsite')
                    inputgithub = request.form.get('inputgithub')
                    inputtwitter = request.form.get('inputtwitter')
                    inputfacebook = request.form.get('inputfacebook')
                    inputinstagram = request.form.get('inputinstagram')
                    inputOrgName = request.form.get('inputOrgName')
                    inputExperience = request.form.get('inputExperience')
                    selectGender = request.form.get('selectGender')
                    inputLocation = request.form.get('inputLocation')
                    inputEmailAddress = request.form.get('inputEmailAddress')
                    inputPhone = request.form.get('inputPhone')
                    inputBirthday = request.form.get('inputBirthday')
                    selectLang = request.form.get('selectLang')

                    

                return(render_template('teacher_login.html',inputUsername = inputUsername , inputFirstname =  inputFirstname,inputLastname = inputLastname,inputexpertise =inputexpertise,inputwebsite = inputwebsite,inputgithub = inputgithub,inputtwitter = inputtwitter,inputfacebook = inputfacebook,inputinstagram = inputinstagram,inputOrgName = inputOrgName,inputExperience = inputExperience,selectGender = selectGender,inputLocation = inputLocation,inputEmailAddress = inputEmailAddress,inputPhone = inputPhone,inputBirthday = inputBirthday,selectLang = selectLang ))
            else:
                return(render_template('personal_details.html'))
           
            
        except Exception as e:
            
            message = json.loads(e.args[1])['error']['message']
            
            if message == "EMAIL_EXISTS":

                
                return render_template('login.html', signup_error = "Email already exists. Login with you registered email or register with a new one.", signup_display_error = True)
            
            
            else:

                return render_template('login.html', signup_error = "Something is not right. Please try again later or contact the administrator", signup_display_error = True)

            

    
    else:


        signup_error_message = "Something is not right. Please try again later or contact the administrator"
        return render_template('login.html', signup_error = signup_error_message, signup_display_error = True)


@app.route('/login', methods = ['GET','POST'])
def login():
    
    login_display_error = False
    print("login execution")

    if request.method == 'POST':
        
        email = request.form['email']
        password = request.form['password']

        
        try:
            
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = user
            return redirect('/')
        
        except Exception as e:
    
            login_error = "Invalid email or password. Please try again."
            return render_template('login.html', login_error = login_error, login_display_error = True)
        
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():


    print(calculate_total_time())
    session.pop('user', None)
    session.clear() 


    return redirect('/')




@app.route('/dashboard')

def dashboard():
    
    if 'user' in session:

        #signed user    
        
        user_id_token = session['user']["idToken"]
        
        auth.refresh(session['user']['refreshToken'])

        user = auth.get_account_info(user_id_token)['users'][0]
        
        first_name = "Utsav Tiwari"
        login_name="Utsav"
        login_email="kkk.@"
        login_phone="123456789"
        login_mobile="032145687"
        login_address="abcdefgh"
        gyx_credits=10
        login_full_name="Utsav Tiwari"
        login_address="Student"
        login_course="Btech"


        



        
        if "displayName" not in user:
            first_name = "!"
        else:
            first_name = user['displayName'].split()[0]

        return render_template('dashboard.html', first=first_name,login=login_name,login_email=login_email,login_phone=login_phone, login_mobile=login_mobile,login_address=login_address,gyx_credit=gyx_credits,login_full_name=login_full_name,login_course=login_course)


    else:

        return redirect('/login')


@app.route('/teachers_dashboard')

def teachers_dashboard():
    
    if 'user' in session:

        #signed user    
        
        user_id_token = session['user']["idToken"]
        
        auth.refresh(session['user']['refreshToken'])

        user = auth.get_account_info(user_id_token)['users'][0]
        
        teachers_name="Prof HC verma"
        teachers_website="aboututsav.netlify.app"
        teachers_github="github.com"
        teachers_twitter="twitter.com"
        teachers_instagram="instagram.com"
        teachers_facebook="facebook.com"


        teachers_login_name="Prof HC verma"
        teachers_login_phone="123456789"
        teachers_login_expertise="Physics "
        teachers_login_address="Kolkata"
        teachers_login_email="profverma@gmail.com"
        
        if "displayName" not in user:
            first_name = "!"
        else:
            first_name = user['displayName'].split()[0]

        return render_template('teachers_dashboard.html', first=first_name, teachers_github=teachers_github,teachers_facebook=teachers_facebook,teachers_instagram=teachers_instagram,teachers_twitter=teachers_twitter,teachers_website=teachers_website,teachers_name=teachers_name, teachers_login_name=teachers_login_name,teachers_login_phone=teachers_login_phone,teachers_login_expertise=teachers_login_expertise,teachers_login_address=teachers_login_address,teachers_login_email=teachers_login_email)


    else:

        return redirect('/login')
    

    





@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        try:
            auth.send_password_reset_email(email)
            message = "Success! Password reset link has been sent to your email"
            return render_template('login.html', message=message, display_alert=True)
        except Exception as e:
            message = json.loads(e.args[1])['error']['message']
            
            if message == "EMAIL_NOT_FOUND":


                return render_template('forgot_password.html', message = "Email does not exists. Enter your registered email id!", display_error = True)
            
            
            else:

                return render_template('forgot_password.html', message = "Something is not right. Please try again later or contact the administrator", display_error = True)
    else:
        return render_template('forgot_password.html')

@app.route('/livechat')
def livechat():
    if 'user' in session:

        #signed user    
        
        user_id_token = session['user']["idToken"]
        
        auth.refresh(session['user']['refreshToken'])

        user = auth.get_account_info(user_id_token)['users'][0]
        
        first_name = ""
        
        if "displayName" not in user:
            first_name = "!"
        else:
            first_name = user['displayName'].split()[0]

        return render_template('working.html', first_name=first_name)

    else:
        return render_template('working.html')
    



@app.route('/personal_details', methods = ['GET','POST'])
def personal_details():

    return render_template('personal_details.html')

@app.route('/searchQuery', methods = ['GET','POST'])
def searchQuery():
    if request.method == 'POST':
        query = request.form["query"]
           
        api_key = 'AIzaSyAMtysCv1YSFqck6UOtdpZWYuZ1qzGGNWY'
        search_results = youtube_search_topic(api_key, query)

        for result in search_results:
            print(f'Title: {result["title"]}')
            print(f'Video ID: {result["video_id"]}')
            print(f'URL: {result["url"]}')
            print('\n')

    return render_template('index.html')



@app.route('/chatbot', methods = ["GET","POST"])
def chatbot():
    
    if 'user' in session:

        #signed user    
        
        user_id_token = session['user']["idToken"]
        
        auth.refresh(session['user']['refreshToken'])

        user = auth.get_account_info(user_id_token)['users'][0]
        
        first_name = ""
        
        if "displayName" not in user:
            first_name = "!"
        else:
            first_name = user['displayName'].split()[0]

        return render_template('chatbot.html', first_name=first_name)


    else:
        return render_template('chatbot.html')



@app.route('/working')
def working():
    if 'user' in session:

        #signed user    
        
        user_id_token = session['user']["idToken"]
        
        auth.refresh(session['user']['refreshToken'])

        user = auth.get_account_info(user_id_token)['users'][0]
        
        first_name = ""
        
        if "displayName" not in user:
            first_name = "!"
        else:
            first_name = user['displayName'].split()[0]

        return render_template('working.html', first_name=first_name)



        return redirect('working.html') 

@app.route("/teaher_login", methods = ['GET'])
def teacher_login():


    print(request.get_data())
    return render_template('teacher_login.html')

#time function
@app.route('/update_total_time', methods=['POST'])
def update_total_time():
    print( calculate_total_time())
    return jsonify(success=True)



'''@app.route('/livechat')
def livechat():
    if 'user' in session:
        user_id_token = session['user']["idToken"]
        auth.refresh(session['user']['refreshToken'])
        user = auth.get_account_info(user_id_token)['users'][0]
        first_name = "" if "displayName" not in user else user['displayName'].split()[0]

        return render_template('live_server.html', first_name=first_name)
    else:
        return redirect('/login')'''


if __name__ == '__main__':
    app.run(debug=True)
    
    
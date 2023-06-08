from flask import Flask, request, render_template, redirect, url_for, jsonify
import json
from random import randint
from twilio.rest import Client
import os

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    return redirect(url_for('login'))

@app.route("/home", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        telephone = request.form["telephone"]
        password = request.form["password"]
        account_file_path = f"{telephone}.json"
        try:
            with open(account_file_path, "r") as account_file:
                data = json.load(account_file)

                if data["password"] == password:
                    # Successful login
                    Fname = data["prenom"]
                    name = data["nom"]
                    tel= data["telephon"]
                    option = data['option']
                    bac_année = data["bac-year"]
                    p_année = int(bac_année[3])
                    
                    pre_année = bac_année[0:3]+f'{p_année -1}'
                    if option == "math" :
                        url = "http://www.bacweb.tn/sujet_corrige2021/sujet_math_principale.pdf"
                        math = "http://www.lovemaths.fr/revisbac.html"
                    if option == 'sc':
                        url = "http://www.bacweb.tn/sujet_corrige2021/sujet_sciences_principale.pdf"
                    if option == 'Technique':
                        url = "http://www.bacweb.tn/sujet_corrige2021/sujet_technique_principale.pdf"
                    if option == "lettre":
                        url = "http://www.bacweb.tn/sujet_corrige2021/sujet_lettre_principale.pdf"
                    if option == 'info': url = "http://www.bacweb.tn/sujet_corrige2021/sujet_info_principale.pdf"
                    if option == 'eco' : url = "http://www.bacweb.tn/sujet_corrige2021/sujet_eco_gestion_principale.pdf"
                    if option == 'sport' : url = "http://www.bacweb.tn/sujet_corrige2021/sujet_sport_principale.pdf"
                    
                    return render_template('home.html',math=math,Fname=Fname,name=name,tel=tel,option=option,bac_année=bac_année,pre_année=pre_année,url=url)
        except FileNotFoundError:
            pass
        
        # Incorrect telephone number or password
        return render_template('login.html')
    else:
        return render_template('login.html')




@app.route('/login', methods=["GET", "POST"])
def sign():
    if request.method == "GET":
        return render_template('Sign_up.html')
    elif request.method == "POST":
        symbol = ['/','-','?','$','&']
        nom = request.form['nomed']
        prenom = request.form['prenom']
        tel = request.form['telephone']
        option = request.form['bac']
        bac_years = request.form['bac-year']
        password = request.form['password']
        confirm = request.form["confirm-password"]
        if password != confirm:
            invalid_password = "Le mot de passe n'est pas correct."
            return render_template('Sign_up.html',invalid_pass=invalid_password)
        elif len(password) <= 8 :
            invalid = "Le mot de passe est trop court."
            return render_template('Sign_up.html',invalid=invalid)
        else:
            valid = password
        user = randint(1000,9999999)
        account_file_path = f"{tel}.json"
        data = {
            "password": valid,
            "prenom": nom,
            "nom": prenom,
            "telephon": tel,
            "option": option,
            "bac-year": bac_years
        }
        with open(account_file_path,"w") as account :
            json.dump(data, account)
        return redirect(url_for('login'))
@app.route('/saved', methods=['GET', 'POST'])
def saved():
    if request.method == 'POST':
        telephone = request.form['telephone_user']
        account_file_path = f"{telephone}.json"

        
        events = []
        for i in range(1, 16):
            event = request.form.get(f'event{i}')
            date = request.form.get(f'date{i}')
            time = request.form.get(f'time{i}')

            
            if event and date and time:
                event_data = {
                    'event': event,
                    'date': date,
                    'time': time
                }
                events.append(event_data)
        
       
        try:
            with open(account_file_path, 'r') as account_file:
                data = json.load(account_file)
        except FileNotFoundError:
            
            data = {}


        data['events'] = events
        Fname = data["prenom"]
        Fname = (Fname[0]).upper() + Fname[1:]
        name = data["nom"]
        tel= data["telephon"]
        option = data['option']
        bac_année = data["bac-year"]
        p_année = int(bac_année[3])
                    
        pre_année = bac_année[0:3]+f'{p_année -1}'
        if option == "math" :
            url = "http://www.bacweb.tn/sujet_corrige2021/sujet_math_principale.pdf"
        math = "http://www.lovemaths.fr/revisbac.html"
        if option == 'sc':
            url = "http://www.bacweb.tn/sujet_corrige2021/sujet_sciences_principale.pdf"
        if option == 'Technique':
            url = "http://www.bacweb.tn/sujet_corrige2021/sujet_technique_principale.pdf"
        if option == "lettre":
            url = "http://www.bacweb.tn/sujet_corrige2021/sujet_lettre_principale.pdf"
        if option == 'info': url = "http://www.bacweb.tn/sujet_corrige2021/sujet_info_principale.pdf"
        if option == 'eco' : url = "http://www.bacweb.tn/sujet_corrige2021/sujet_eco_gestion_principale.pdf"
        if option == 'sport' : url = "http://www.bacweb.tn/sujet_corrige2021/sujet_sport_principale.pdf"
        with open(account_file_path, 'w') as account_file:
            json.dump(data, account_file)
        with open(account_file_path, 'r') as account_file:
            data = json.load(account_file)
        
        return render_template('home.html',math=math,Fname=Fname
                               ,name=name,tel=tel,option=option
                               ,bac_année=bac_année,
                               pre_année=pre_année,
                               url=url)
    

        

@app.route('/recent', methods=['GET', 'POST'])
def recent():
    if request.method == 'POST':
        telephone = request.form['tel_user']
        account_file_path = f"{telephone}.json"
        
        try:
            with open(account_file_path, 'r') as account_file:
                data = json.load(account_file)
                events = data.get('events', [])
                user_name = data['prenom']
                user_name = (user_name[0]).upper()+user_name[1:]
        except FileNotFoundError:
            events = []
        
        return render_template('save_page.html', events=events, enumerate=enumerate,user_name=user_name)
    else:
        # Code for handling GET request
        
        return render_template('login.html')
    
    

@app.route("/Pomodoro_Technique",methods = ["GET","POST"])
def Pomodoro():
    if request.method == "POST":
        return render_template("chronometre.html")
    else: return render_template("chronometre.html")


if __name__== '__main__':
    app.run(debug=True,host="127.1.1.1", port=5501)

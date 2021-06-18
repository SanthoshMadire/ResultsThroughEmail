from email import message
from types import MethodType
from flask import Flask,render_template,request,redirect, url_for
from flask_mail import Mail,Message
import csv,smtplib, ssl
import pandas as pd
from email.message import EmailMessage

app=Flask(__name__)
mail=Mail(app)

@app.route('/')
def index():
    return render_template("home.html")


@app.route('/login', methods=['POST'])
def login():
    error = None
    if request.method == 'POST':
        username=request.form["username"]
        password=request.form["password"]
        if  username!= 'admin' or password != 'admin@cvr123':
            error = 'Invalid Credentials. Please try again.\n!!!ADMIN ACCESS ONLY!!!'
            return render_template('home.html', error=error)  
        else:  
            return render_template('login.html',username=username)  

@app.route('/sendmail',methods=['GET', 'POST'])
def getcsv():
    if request.method == 'POST':
       subject='Hi {name}, your marks  are {total}'
       body= '{sub1} = {s1}\n{sub2} = {s2}\n{sub3} = {s3}\n{sub4} = {s4}\n{sub5} = {s5}'
       message = f'Subject: {subject}\n\n{body}'
       from_address = 'resultsthroughemail@gmail.com'
       password = '6305077750'
       context = ssl.create_default_context()
       with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
          server.login(from_address, password)
          f= request.files['datacsv']    
          
          with open(f.filename) as file:
              reader = csv.reader(file)
              next(reader)  # Skip header row
              for ID,NAME,BRANCH,SECTION,SUB1,S1,SUB2,S2,SUB3,S3,SUB4,S4,SUB5,S5,TOTAL,STATUS,EMAIL in reader:
                   server.sendmail(from_address,EMAIL,message.format(name=NAME,total=TOTAL,sub1=SUB1,s1=S1,sub2=SUB2,s2=S2,sub3=SUB3,s3=S3,sub4=SUB4,s4=S4,sub5=SUB5,s5=S5),)
       f=request.files['datacsv']
       results=[]
       with open(f.filename) as file:
           csvfile=csv.reader(file)
           for row in csvfile:
               results.append(row)
       results=pd.DataFrame(results)
       return render_template('details.html',results=results.to_html(header=False,index=False))
     
@app.route('/logout',methods=['GET', 'POST'])
def logout():
    return redirect(url_for('index'))


if __name__=="__main__":
    app.run(debug=True)

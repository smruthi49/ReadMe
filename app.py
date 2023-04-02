from flask import Flask,request,render_template,url_for,session,redirect 
import pymysql,re,pandas as pd
from books import Books
app=Flask(__name__,template_folder="templates",static_folder="static")

app.secret_key = 'cia2'
b = Books()
df=pd.read_csv("bookdata.csv")

@app.route('/')
def main():
    msg=' '
    return render_template("index.html",msg=' ')

@app.route('/home')
def home():
    if 'loggedin' in session:
        topbooks=df.sort_values(by=['Rating_score'],ascending=False)['Book_Title'].head(10).tolist()
        toplist=idlist=[b.get_index_from_title(i) for i in topbooks]
        tthh=[[df.Book_Title.iloc[i],df.Author_Name.iloc[i],df.url.iloc[i]] for i in toplist]
        msg="TOP 10 BOOKS"
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'],tthh=tthh,msg=msg)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/login',methods=['GET','POST'])
def login():
    msg=''
    username=request.form.get("username")
    password=request.form.get("password")
    print(username,password)

    connection=pymysql.connect(host='localhost',
                         user='root',
                         password='root',
                         db='dbms',)
    if request.method == 'POST' and username and password:
        
        with connection:
            with connection.cursor() as cursor:
                
                # Read a single record
                sql = "SELECT * FROM `accounts` WHERE `username`=%s and `password`=%s"
                cursor.execute(sql, (username,password))
                #connection.commit()
                result = cursor.fetchone()
                print(result,"hi")

                if result:
                    session['loggedin']=True
                    session['id']=result[0]
                    session['username']=result[1]
                    msg='Logging in'
                    return redirect(url_for('home'))
                else:
                    msg='Incorrect username/password'

    return render_template('index.html', msg=msg)

@app.route('/register',methods=['GET','POST'])
def register():
    msg=''
    

    connection=pymysql.connect(host='localhost',
                         user='root',
                         password='root',
                         db='dbms',)
    
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username=request.form.get("username")
        password=request.form.get("password")
        email=request.form.get("email")

        with connection:
            with connection.cursor() as cursor:
                sql="SELECT * FROM accounts WHERE username=%s"
                cursor.execute(sql,username)
                account=cursor.fetchone()
                
                if account:
                    msg="Account already exists"
                elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                    msg = 'Invalid email address!'
                elif not re.match(r'[A-Za-z0-9]+', username):
                    msg = 'Username must contain only characters and numbers!'
                elif not username or not password or not email:
                    msg = 'Please fill out the form!'
                else:
                    # Create a new record
                    query = "INSERT INTO accounts ( username,password,email) VALUES (%s, %s,%s)"
                    cursor.execute(query, (username,password,email))
                    connection.commit()
                    msg='Successfully Registered!'

    elif request.method=='POST':
        msg="Please fill out the form."

    
    return render_template("register.html",msg=msg)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_term = request.form['search_term']
        # do something with the search term, e.g. search a database
        term=b.get_recommendations(b.get_index_from_title(search_term),b.tf_cosine_sim)
        idlist=[b.get_index_from_title(i) for i in term]
        t=[[df.Book_Title.iloc[i],df.Author_Name.iloc[i],df.url.iloc[i]] for i in idlist]
        msg="RECOMMENDED FOR YOU"
        return render_template('home.html', username=session['username'],tthh=t,msg=msg)


if __name__=='__main__':
    #app.run(debug=True)
    app.run(port=4400,host='localhost',debug=True)
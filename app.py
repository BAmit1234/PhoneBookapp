from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL
from os import environ

app= Flask(__name__)

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='root'
app.config['MYSQL_DB']='database'
mysql = MySQL(app)



@app.route('/',methods=['GET','POST'])
def home():
    cur=mysql.connection.cursor()
    n=1
    p=n*10 -9
    k=n*10
    results=cur.execute("SELECT * FROM phonebook")
    result=cur.execute("SELECT * FROM phonebook limit %s, %s",(p,k,))
    n=n+1

    if result > 0:
        result1 = cur.fetchall()
        return render_template('home.html',result1=result1,result=result,results=results)  
    return render_template('home.html')



@app.route('/Add',methods=['GET','POST'])
def Add():
    if request.method =='POST':
        name = request.form['name']
        number= request.form['number']
        email = request.form['email']
        
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO phonebook (name, number, email ) VALUES(%s,%s,%s)",(name,number,email,))
        mysql.connection.commit()
        cur.close()
        return redirect('/')
    return render_template("Add.html")



@app.route('/update/<int:id>',methods=['GET','POST'])
def Update(id):
    if request.method=='POST':
        name = request.form['name']
        number= request.form['number']
        email = request.form['email']
        cur=mysql.connection.cursor()
        cur.execute("UPDATE phonebook SET name=%s WHERE id = %s",(name,id))
        cur.execute("UPDATE phonebook SET number=%s WHERE id = %s",(number,id))
        cur.execute("UPDATE phonebook SET email=%s WHERE id = %s",(email,id))
        mysql.connection.commit()
        cur.close()
        return redirect('/')
    return render_template("update.html")





@app.route('/delete/<int:id>',methods=['POST','GET'])
def Delete(id):
    if request.method=='POST':
        
        cur=mysql.connection.cursor()
        cur.execute("DELETE FROM phonebook WHERE id = %s",(id,))
        mysql.connection.commit()
        cur.close()
        return redirect('/')
    return render_template("remove.html")



@app.route('/search',methods=["POST","GET"])
def search():
    if request.method=="POST":
        name=request.form['name']
        email=request.form['email']
        cur=mysql.connection.cursor()
        cur.execute("SELECT * from phonebook WHERE name = %s OR email=%s",(name,email,))
        r=cur.fetchall()
        mysql.connection.commit()
        cur.close()
        return render_template("search.html",r=r)
 
        
        
    return render_template("search.html")
        
    


    
if __name__=='__main__':
    app.run(debug=True)
    

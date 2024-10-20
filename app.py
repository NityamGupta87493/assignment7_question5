from flask import Flask, render_template, request, redirect, session, flash
import mysql.connector
import secrets

app = Flask(__name__)
app.secret_key = str(secrets.token_hex(16))  # Needed to use sessions

# MySQL Database Configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="nityam123",
    database="iit_indore"
)
cursor = db.cursor()

# Route for Homepage (Login Page)
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userid = request.form['userid']
        password = request.form['password']

        cursor.execute("SELECT * FROM users WHERE userid=%s AND password=%s", (userid, password))
        user = cursor.fetchone()

        if user:
            session['userid'] = userid  # Store user session
            return redirect('/welcome')
        else:
            flash('Invalid credentials. Please try again.')
            return redirect('/')

    return render_template('login.html')

# Route for Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        userid = request.form['userid']
        password = request.form['password']
        mobile = request.form['mobile']

        try:
            cursor.execute("INSERT INTO users (userid, password, mobile_number) VALUES (%s, %s, %s)",
                           (userid, password, mobile))
            db.commit()
            flash('Registration successful. Please login.')
            return redirect('/')
        except mysql.connector.Error as err:
            flash('Error: UserID already exists.')
            return redirect('/register')

    return render_template('register.html')

# Route for Welcome Page
@app.route('/welcome')
def welcome():
    if 'userid' in session:
        return render_template('welcome.html')
    else:
        flash('Please log in first.')
        return redirect('/')

# Run the Application
if __name__ == '__main__':
    app.run(debug=True)

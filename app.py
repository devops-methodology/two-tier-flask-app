from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import os

app = Flask(__name__)

# Configure MySQL (you can leave dummy values for now)
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', 'password')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'mydb')

mysql = MySQL(app)

@app.route('/')
def index():
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT message FROM messages')
        messages = cur.fetchall()
        cur.close()
    except Exception as e:
        messages = [('MySQL not connected!',)]
    return render_template('index.html', messages=messages)

@app.route('/submit', methods=['POST'])
def submit():
    message = request.form['message']
    try:
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO messages (message) VALUES (%s)', (message,))
        mysql.connection.commit()
        cur.close()
    except Exception as e:
        return f"Error inserting into DB: {e}"
    return 'Message submitted successfully'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

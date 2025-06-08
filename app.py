from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
import os

app = Flask(__name__)

# MySQL Configuration from environment or fallback
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
    message = request.form.get('new_message')  # ✅ Match with HTML: name="new_message"

    if not message:
        return jsonify({'error': 'Message cannot be empty'}), 400

    try:
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO messages (message) VALUES (%s)', (message,))
        mysql.connection.commit()
        cur.close()
    except Exception as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500

    return jsonify({'message': message})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

from flask import Flask, render_template, request
import pymysql

app = Flask(__name__)

def get_db_connection():
    return pymysql.connect(host="localhost", database="sample database", user="root", password="")

@app.route('/process_query', methods=['GET', 'POST'])
def process_query():
    result = ""
    data = []

    if request.method == 'POST':
        operation = request.form['operation']
        db = get_db_connection()
        cursor = db.cursor()

        if operation == 'select':
            cursor.execute("SELECT id, nm, addr,phone,dob,doj,salary FROM employee")
            data = cursor.fetchall()
            result = "Fetched all records."

        elif operation == 'insert':
            id = int(request.form['id'])
            nm = request.form['nm']
            addr = request.form['addr']
            phone = request.form['phone']
            dob = request.form['dob']
            doj = request.form['doj']
            salary = int(request.form['salary'])

            qry = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(qry, (id, nm, addr, phone, dob, doj, salary))
            db.commit()
            result = "Record inserted."

        elif operation == 'update':
            id = int(request.form['id'])
            nm = request.form['nm']
            addr = request.form['addr']
            phone = request.form['phone']
            dob = request.form['dob']
            doj = request.form['doj']
            salary = int(request.form['salary'])

            qry = "UPDATE employee SET nm=%s, addr=%s, phone=%s, dob=%s, doj=%s, salary=%s WHERE id=%s"
            cursor.execute(qry, (nm, addr, phone, dob, doj, salary, id))
            db.commit()
            result = "Record updated."

        elif operation == 'delete':
            id = int(request.form['id'])
            cursor.execute("DELETE FROM employee WHERE id=%s", (id,))
            db.commit()
            result = "Record deleted."
        cursor.execute("SELECT id, nm, addr,phone,dob,doj,salary FROM employee")
        data = cursor.fetchall()
        db.close()

    return render_template("employee_table.html", data=data, result=result)

if __name__ == '__main__':
    app.run(debug=True)

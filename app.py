from flask import Flask
from flask import request
from flask import render_template
import sqlite3 as my

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add/")
def add():
    return render_template("add.html")

@app.route("/savedetails", methods=["POST", "GET"])
def saveDetails():
    msg = "msg"
    if request.method == "POST":
        try:
            name = request.form["name"]
            password = request.form["password"]
            with my.connect("employee.db") as con:
                cur = con.cursor()
                cur.execute("INSERT into Employees ( name, password) values (?,?)", (name, password))
                con.commit()
                msg = "Employee successfully Added"
        except my.Error as a:
             con.rollback()
             msg = "We can not add the employee to the list"
        finally:
            return render_template("success.html", msg=msg)
            con.close();


@app.route("/view/")
def view():
    con = my.connect("employee.db")
    con.row_factory = my.Row
    cur = con.cursor()
    cur.execute("select * from Employees")
    rows = cur.fetchall()
    return render_template("view.html", rows=rows)

@app.route("/select/", methods=["GET"])
def find():
    con = my.connect("employee.db")
    con.row_factory = my.Row
    cur.execute("select")

@app.route("/delete/")
def delete():
    return render_template("delete.html")


@app.route("/deleterecord", methods=["POST"])
def deleterecord():
    id = request.form["id"]
    with sqlite3.connect("employee.db") as con:
        try:
            cur = con.cursor()
            cur.execute("delete from Employees where id = ?", id)
            msg = "record successfully deleted"
        except:
            msg = "can't be deleted"
        finally:
            return render_template("delete_record.html", msg=msg)


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, jsonify
import sqlite3
from pathlib import Path

DB="tasks.db"
app=Flask(__name__)

def init_db():
    con=sqlite3.connect(DB)
    con.execute("CREATE TABLE IF NOT EXISTS tasks(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, completed INTEGER DEFAULT 0)")
    con.commit(); con.close()

def q(sql,args=(),fetch=False):
    con=sqlite3.connect(DB)
    cur=con.cursor(); cur.execute(sql,args)
    rows=cur.fetchall() if fetch else None
    con.commit(); con.close()
    return rows

@app.route("/")
def index():
    tasks=q("SELECT * FROM tasks ORDER BY id DESC",fetch=True)
    return render_template("index.html",tasks=tasks)

@app.post("/add")
def add():
    title=request.form["title"].strip()
    if title:
        q("INSERT INTO tasks(title) VALUES(?)",(title,))
    return redirect("/")

@app.get("/complete/<int:id>")
def complete(id):
    q("UPDATE tasks SET completed=1 WHERE id=?",(id,))
    return redirect("/")

@app.get("/delete/<int:id>")
def delete(id):
    q("DELETE FROM tasks WHERE id=?",(id,))
    return redirect("/")

@app.get("/health")
def health():
    return jsonify(status="healthy")

@app.get("/api/tasks")
def api():
    rows=q("SELECT id,title,completed FROM tasks",fetch=True)
    return jsonify([{"id":r[0],"title":r[1],"completed":bool(r[2])} for r in rows])

if __name__=="__main__":
    init_db()
    app.run(host="0.0.0.0",port=5000,debug=True)

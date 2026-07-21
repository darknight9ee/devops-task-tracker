from flask import Blueprint, render_template, request, redirect

from .database import db
from .models import Task

main = Blueprint("main", __name__)


@main.route("/")
def index():

    tasks = Task.query.order_by(Task.id.desc()).all()

    return render_template(
        "index.html",
        tasks=tasks
    )


@main.route("/add", methods=["POST"])
def add():

    title = request.form.get("title")

    if title:

        task = Task(title=title)

        db.session.add(task)

        db.session.commit()

    return redirect("/")


@main.route("/complete/<int:id>")
def complete(id):

    task = Task.query.get_or_404(id)

    task.completed = True

    db.session.commit()

    return redirect("/")


@main.route("/delete/<int:id>")
def delete(id):

    task = Task.query.get_or_404(id)

    db.session.delete(task)

    db.session.commit()

    return redirect("/")
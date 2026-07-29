from flask import Blueprint, render_template, request, redirect
from sqlalchemy import text

from .database import db
from .logger import logger
from .models import Task

main = Blueprint("main", __name__)


@main.route("/")
def index():

    tasks = Task.query.order_by(Task.id.desc()).all()

    total_tasks = len(tasks)

    completed_tasks = sum(task.completed for task in tasks)

    pending_tasks = total_tasks - completed_tasks

    return render_template(
        "index.html",
        tasks=tasks,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks
    )


@main.route("/add", methods=["POST"])
def add():

    title = request.form.get("title")

    if title:

        task = Task(title=title)

        db.session.add(task)

        db.session.commit()
        logger.info(f"Task created: {title}")

    return redirect("/")


@main.route("/complete/<int:id>")
def complete(id):

    task = Task.query.get_or_404(id)

    task.completed = True

    db.session.commit()
    logger.info(f"Task completed: {task.title}")

    return redirect("/")


@main.route("/delete/<int:id>")
def delete(id):

    task = Task.query.get_or_404(id)

    db.session.delete(task)

    db.session.commit()
    logger.info(f"Task deleted: {task.title}")

    return redirect("/")


@main.route("/health")
def health():

    try:

        db.session.execute(text("SELECT 1"))

        database = "connected"

    except Exception:

        database = "disconnected"

    return {
        "status": "healthy",
        "database": database
    }


@main.route("/version")
def version():

    return {
        "application": "DevOps Task Tracker",
        "version": "1.0.0"
    }
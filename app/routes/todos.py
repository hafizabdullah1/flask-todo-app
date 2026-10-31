from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.extensions import db
from app.models import Todo

# 1. Create the Blueprint named 'todos'
todos_bp = Blueprint('todos', __name__)

@todos_bp.route("/")
def home():
    filter_by = request.args.get("filter", "all")
    search_query = request.args.get("q", "").strip()

    query = Todo.query

    if filter_by == "pending":
        query = query.filter_by(done=False)
    elif filter_by == "completed":
        query = query.filter_by(done=True)

    if search_query:
        query = query.filter(Todo.title.contains(search_query))

    todos = query.all()
    return render_template("index.html", todos=todos, current_filter=filter_by, search_query=search_query)


@todos_bp.route("/add", methods=["POST"])
def add_todo():
    title = request.form.get("title")

    if title and title.strip():
        new_todo = Todo(title=title.strip())
        db.session.add(new_todo)
        db.session.commit()
        flash("Task added successfully!", "success")
    else:
        flash("Task title cannot be empty!", "error")

    return redirect(url_for("todos.home"))


@todos_bp.route("/toggle/<int:todo_id>")
def toggle_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    todo.done = not todo.done
    db.session.commit()

    status_text = "completed" if todo.done else "pending"
    flash(f"Task marked as {status_text}!", "info")

    return redirect(url_for("todos.home"))


@todos_bp.route("/delete/<int:todo_id>")
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    flash("Task deleted successfully!", "warning")

    return redirect(url_for("todos.home"))
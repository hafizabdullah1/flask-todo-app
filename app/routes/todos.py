from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Todo

todos_bp = Blueprint('todos', __name__)


@todos_bp.route("/")
@login_required
def home():
    filter_by = request.args.get("filter", "all")
    search_query = request.args.get("q", "").strip()

    # Query only tasks belonging to the currently logged in user
    query = Todo.query.filter_by(user_id=current_user.id)

    if filter_by == "pending":
        query = query.filter_by(done=False)
    elif filter_by == "completed":
        query = query.filter_by(done=True)

    if search_query:
        query = query.filter(Todo.title.contains(search_query))

    todos = query.all()
    return render_template("index.html", todos=todos, current_filter=filter_by, search_query=search_query)


@todos_bp.route("/add", methods=["POST"])
@login_required
def add_todo():
    title = request.form.get("title")

    if title and title.strip():
        # Associate task with the current logged in user
        new_todo = Todo(title=title.strip(), author=current_user)
        db.session.add(new_todo)
        db.session.commit()
        flash("Task added successfully!", "success")
    else:
        flash("Task title cannot be empty!", "error")

    return redirect(url_for("todos.home"))


@todos_bp.route("/toggle/<int:todo_id>")
@login_required
def toggle_todo(todo_id):
    # Ensure users can only modify their own tasks
    todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first_or_404()
    todo.done = not todo.done
    db.session.commit()

    status_text = "completed" if todo.done else "pending"
    flash(f"Task marked as {status_text}!", "info")

    return redirect(url_for("todos.home"))


@todos_bp.route("/delete/<int:todo_id>")
@login_required
def delete_todo(todo_id):
    # Ensure users can only delete their own tasks
    todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first_or_404()
    db.session.delete(todo)
    db.session.commit()
    flash("Task deleted successfully!", "warning")

    return redirect(url_for("todos.home"))

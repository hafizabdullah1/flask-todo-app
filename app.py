from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


# Configure the SQLite database.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'super-secret-key'

# Initialize SQLAlchemy.
db = SQLAlchemy(app)


# Define the todo table.
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Todo {self.id}: {self.title}>"


# Create database tables within the application context.
with app.app_context():
    db.create_all()


@app.route("/")
def home():
    # Read query parameters from URL: e.g. /?filter=pending&q=flask
    filter_by = request.args.get("filter", "all")
    search_query = request.args.get("q", "").strip()

    # Base query
    query = Todo.query

    # Apply Filter (Pending vs Completed)
    if filter_by == "pending":
        query = query.filter_by(done=False)
    elif filter_by == "completed":
        query = query.filter_by(done=True)

    # Apply Search Query (if user typed something)
    if search_query:
        query = query.filter(Todo.title.contains(search_query))

    todos = query.all()

    # Pass filter and search values back so HTML knows which tab is active
    return render_template("index.html", todos=todos, current_filter=filter_by, search_query=search_query)


@app.route("/add", methods=["POST"])
def add_todo():
    title = request.form.get("title")

    if title and title.strip():
        new_todo = Todo(title=title.strip())
        db.session.add(new_todo)
        db.session.commit()
        flash("Task added successfully!", "success")
    else:
        flash("Task title cannot be empty!", "error")

    return redirect(url_for("home"))


@app.route("/toggle/<int:todo_id>")
def toggle_todo(todo_id):
    # Return 404 if the todo does not exist.
    todo = Todo.query.get_or_404(todo_id)
    todo.done = not todo.done
    db.session.commit()

    status_text = "completed" if todo.done else "pending"
    flash(f"Task marked as {status_text}!", "info")

    return redirect(url_for("home"))


@app.route("/delete/<int:todo_id>")
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    
    db.session.delete(todo)
    db.session.commit()
    
    flash("Task deleted successfully!", "warning")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)

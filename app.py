from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the SQLite database.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
    # Fetch all todos for the home page.
    todos = Todo.query.all()
    return render_template("index.html", todos=todos)


@app.route("/add", methods=["POST"])
def add_todo():
    title = request.form.get("title")

    if title and title.strip():
        new_todo = Todo(title=title.strip())
        db.session.add(new_todo)
        db.session.commit()

    return redirect(url_for("home"))


@app.route("/toggle/<int:todo_id>")
def toggle_todo(todo_id):
    # Return 404 if the todo does not exist.
    todo = Todo.query.get_or_404(todo_id)
    todo.done = not todo.done
    db.session.commit()

    return redirect(url_for("home"))


@app.route("/delete/<int:todo_id>")
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    
    db.session.delete(todo)
    db.session.commit()

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)

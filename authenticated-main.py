from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///book-collection.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a secure secret key
db = SQLAlchemy(app)

# JWT Configuration
def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

def identity(payload):
    user_id = payload['identity']
    return User.query.filter_by(id=user_id).first()

jwt = JWT(app, authenticate, identity)

# Sample User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    author = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'

# db.create_all()

@app.route('/')
@jwt_required()
def home():
    all_books = db.session.query(Book).all()
    return render_template("index.html", books=all_books)

@app.route("/add", methods=["GET", "POST"])
@jwt_required()
def add():
    if request.method == "POST":
        # Create Object:
        new_book = Book(title=request.form["title"], author=request.form["author"])
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html")

@app.route("/edit-rating", methods=["GET", "POST"])
@jwt_required()
def edit_rating():
    if request.method == "POST":
        # Update rating:
        book_id = request.form["id"]
        book_to_update = Book.query.get(book_id)
        book_to_update.rating = request.form["rating"]
        db.session.commit()
        return redirect(url_for('home'))
    book_id = request.args.get('id')
    book_selected = Book.query.get(book_id)
    return render_template("edit-rating.html", book=book_selected)

@app.route("/delete")
@jwt_required()
def delete():
    book_id = request.args.get('id')
    book_to_delete = Book.query.get(book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True, port=5007)

from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

# Create the database and tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/submit', methods=['POST'])
def submit():
    username = request.form.get('username')
    password = request.form.get('password')

    # Check if user already exists
    user = User.query.filter_by(username=username).first()
    if user:
        return "User already exists!"

    # Create a new user and add to the database
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    
    print(f"Username: {username}")
    print(f"Password: {password}")
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

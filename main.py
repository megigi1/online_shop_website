import requests
# Done - Plan out the features and layout of your eCommerce website. This includes designing the user interface, deciding on the types of products you will sell, and creating a list of requirements for the website.
# Done - Set up a web server and database. You can use a cloud provider like AWS, Google Cloud, or DigitalOcean to set up your server and database. You'll also need to choose a programming language (such as Python or JavaScript) and a web framework (such as Flask or Django) to build your website.
# Done - Create a database schema. Your schema should include tables for products, users, orders, and payments.
# Done - Implement user authentication. Your website should allow users to create accounts, log in, and log out. You can use a library like Flask-Login or Django's built-in authentication system to handle this.
# Create the product catalog. Your website should have a page where users can browse through the products you are selling. You can use a library like Flask-WTF or Django Forms to create forms for adding and editing products.
# Implement the shopping cart. When a user adds a product to their cart, the product and its details should be stored in the database. You can use cookies or sessions to store the cart information.
# Implement the checkout process. When a user is ready to checkout, they should be taken to a page where they can enter their billing and shipping information. You can use a library like Stripe to handle the payment processing.
# Test your website. Make sure all the features are working as expected and there are no bugs.
# Deploy your website. You can use a cloud provider like AWS, Google Cloud, or DigitalOcean to deploy your website and make it accessible to the public.


from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import random
from flask_bootstrap import Bootstrap4
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo

#DATABASED CREATED CORRECTLY
#I AM NOT ABLE TO FINISH THIS WEBSITE AT THE MOMENT.
#I CAN'T TAKE DATA FROM EBAY WEBSITE. ERROR 500 IT IS SHOWING.
#AFTER RECIEVING DATA I WANTED TO BE ABLE PUT ITEMS IN BASKET
#TO DO CHECKOUT I WANTED USE THIS FOR HELP https://stripe.com/docs/payments/checkout

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'Secreto1!'
db = SQLAlchemy(app)

Bootstrap4(app)

# ENDPOINT = "https://www.ebay.com"
# END_TOKEN = "X-EBAY-API-IAF-TOKEN"
# OAUTH = "https://api.ebay.com/oauth/api_scope"

APPLICATION_ID = "MYID"
URL1 = "https://api.ebay.com/commerce/taxonomy/v1_beta/category_tree/0/get_category_subtree"
URL = "https://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findItemsByCategory&SERVICE-VERSION=1.13.0&SECURITY-APPNAME=Magdalen-Onlinesh-PRD-dca7161d2-d39658be&RESPONSE-DATA-FORMAT=JSON&REST-PAYLOAD&categoryId=0"
OAUTH = "MYAUTH"
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/sport", methods=['GET'])
def sport():
    headers = {
        'Authorization': 'Bearer v^1.1#i^1#I^3#f^0#r^0#p^3#t^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',
        'Content-Type': 'application/json',
        'X-EBAY-C-MARKETPLACE-ID': 'EBAY-US'
    }


    payload = {
        'category_tree_id': 0,
        'category_id': 'Sporting Goods',
        'depth': 1
    }


    response = requests.post(URL, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        categories = data['categorySubtree']['categoryTreeNodes']
        return jsonify(categories)
    else:
        error_message = f'Error: {response.status_code} - {response.text}'
        return jsonify({'error': error_message}), response.status_code

        # return render_template("sport.html")

class Ebay(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    products = db.Column(db.String(50))
    users = db.Column(db.String(50))
    orders = db.Column(db.String(50))
    payments = db.Column(db.String(50))
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f'<Ebay {self.id}>'

def init_db():
    with app.app_context():
        db.create_all()




class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Ebay(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Ebay.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            flash('Logged in successfully', 'success')
            return redirect(url_for('afterlog'))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)


@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/afterlog')
def afterlog():
    return render_template("basket.html")


if __name__ == '__main__':
    init_db()
    app.run(debug=True)


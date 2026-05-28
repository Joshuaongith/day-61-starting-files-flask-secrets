import os  # Required to access environment variables
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import PasswordField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from flask_bootstrap import Bootstrap5

app = Flask(__name__)

# Fallback security: Tries to find a real key in the environment variables. 
# If it finds nothing (like on a cloned GitHub repo), it defaults to the dummy string.
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "some-super-secret-string")

# Initializes Bootstrap-Flask to allow global macro styling across the app
bootstrap = Bootstrap5(app)


class MyForm(FlaskForm):
    email = EmailField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField(label='Log In')


@app.route("/")
def home():
    # Renders the initial landing page
    return render_template('index.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = MyForm()

    # Triggers only on a POST request when the user clicks 'Submit' AND all validators pass
    if form.validate_on_submit():
        # Hardcoded admin credentials for the portfolio demonstration
        if form.email.data == "admin@email.com" and form.password.data == "12345678":
            return render_template('success.html')
        else:
            return render_template('denied.html')

    # Triggers on the initial GET request, or if WTForms validation fails
    return render_template('login.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
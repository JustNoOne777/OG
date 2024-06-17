from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, RadioField, SelectField, SubmitField, IntegerField
from wtforms.validators import DataRequired, length , equal_to
from flask_wtf.file import FileField, FileRequired, FileSize, FileAllowed

class RegisterForm(FlaskForm):
    profile_img = FileField("პროფილის სურათი", validators=[
        FileAllowed(["jpg","png"], message ="მხოლოდ სურათების ატვირთვა შეიძლება"),FileSize(1024*1024*5)])
    username = StringField("შეიყვანეთ სახელი", validators=[DataRequired()])
    password = PasswordField("შეიყვანეთ პაროლი", validators=[DataRequired(), length(min=8, max=50, message='პაროლი უნდა შეიცავდეს 8-დან 50-მდე ასოს')])
    repeat_password = PasswordField("გაიმეორეთ პაროლი", validators=[DataRequired(), equal_to("password", message='პაროლები არ ემთხვევა ერთმანეთს')])
    birthday = DateField()
    phone_number = IntegerField("შეიყვანეთ ტელეფონის ნომერი", validators=[DataRequired()])
    gender = RadioField("მონიშნეთ სქესი", choices=["კაცი", "ქალი", "სხვა"], validators=[DataRequired()])
    country = SelectField("აირჩიეთ ქვეყანა", choices=["USA", "Georgia", "Italy", "Other"], validators=[DataRequired()])

    submit = SubmitField("რეგისტრაცია")

class ProductForm(FlaskForm):
    img = FileField()
    name = StringField("პროდუქტის სახელი")
    price= IntegerField("ფასი")
    info = StringField("აღწერა")
    submit = SubmitField("პროდუქტის ატვირთვა ")

class LoginForm(FlaskForm):
    username= StringField()
    password= PasswordField()
    login = SubmitField("შესვლა")
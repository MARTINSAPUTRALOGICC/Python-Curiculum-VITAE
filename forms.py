from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField, validators
from flask_wtf.file import FileField
from wtforms.validators import DataRequired, Email, InputRequired


class insertupdate_user(FlaskForm):
    email = StringField("email")
    job = StringField("job")
    keterangan = StringField("keterangan")
    username = StringField("username")
    submit = SubmitField("submit_register")


class insertfabicon(FlaskForm):
    title_fab = StringField("title_fab")
    icon_fab = StringField("icon_fab")
    href = StringField("href")


class insertEducation(FlaskForm):
    School = StringField("School")
    keterangan_school = StringField("keterangan_school")
    tahun_school = StringField("tahun_school")


class insertProgamming(FlaskForm):
    icon = StringField("icon")
    nama_skill = StringField("nama_skill")
    keterangan_skill = StringField("keterangan_skill")


class insertothers(FlaskForm):
    nama_skill = StringField("nama_skill")
    keterangan_skill = StringField("keterangan_skill")


class insertabout(FlaskForm):
    keterangan_About = StringField("keterangan_About")
    about = StringField("about")
    tahun_about = StringField("tahun_about")


class insertwork(FlaskForm):
    Job = StringField("Job")
    Company = StringField("Company")
    Years = StringField("Years")


class LoginForm(FlaskForm):
    email = StringField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    submit_login = SubmitField("submit_login")


class UploadFileForm(FlaskForm):
    foto_cv = FileField("foto_cv", validators=[InputRequired()])
    username = StringField("username")  # Change 'username' to 'fullname'
    status = StringField("status")  # Change 'username' to 'fullname'


class UpdatePasswordForm(FlaskForm):
    current_password = StringField("current_password")
    new_password = StringField("new_password")
    confirm_password = StringField("confirm_password")
    email = StringField("email")

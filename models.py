from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id_users = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    job = db.Column(db.String(50), nullable=False)
    keterangan = db.Column(db.String(50), nullable=False)
    Foto_Profile = db.Column(db.String(128), nullable=False)
    status = db.Column(db.Integer, default=3)

    def __init__(self, username, email, password, job, keterangan, status):
        self.username = username
        self.email = email
        self.password = password
        self.job = job
        self.keterangan = keterangan
        self.status = status


class fabicon(db.Model):
    __tablename__ = "fab_icon"
    id_fab = db.Column(db.Integer, primary_key=True)
    title_fab = db.Column(db.String(50))
    icon_fab = db.Column(db.String(50))
    href = db.Column(db.String(50))


class skillprogamming(db.Model):
    __tablename__ = "skillprogamming"
    id_skill = db.Column(db.Integer, primary_key=True)
    icon = db.Column(db.String(50))
    nama_skill = db.Column(db.String(50))
    keterangan_skill = db.Column(db.String(50))


class Education(db.Model):
    __tablename__ = "education"
    id_education = db.Column(db.Integer, primary_key=True)
    School = db.Column(db.String(50))
    keterangan_school = db.Column(db.String(50))
    tahun_school = db.Column(db.String(50))


class otherskill(db.Model):
    __tablename__ = "otherskill"
    id_other_skill = db.Column(db.Integer, primary_key=True)
    nama_skill = db.Column(db.String(50))
    keterangan_skill = db.Column(db.String(50))


class workexperience(db.Model):
    __tablename__ = "workexperience"
    id_work = db.Column(db.Integer, primary_key=True)
    Job = db.Column(db.String(50))
    Company = db.Column(db.String(50))
    Years = db.Column(db.String(50))


class about(db.Model):
    __tablename__ = "about"
    id_about = db.Column(db.Integer, primary_key=True)
    keterangan_About = db.Column(db.String(50))
    about = db.Column(db.String(50))
    tahun_about = db.Column(db.String(50))


class Sidebar(db.Model):
    __tablename__ = "side_bar"
    id_side = db.Column(db.Integer, primary_key=True)
    name_side = db.Column(db.String(50))
    icon_side = db.Column(db.String(50))
    url_side = db.Column(db.String(50))
    level_user = db.Column(db.String(50))

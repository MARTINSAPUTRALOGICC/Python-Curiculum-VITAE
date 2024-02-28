from flask import (
    Blueprint,
    request,
    redirect,
    url_for,
    flash,
    request,
    session,
)
from forms import (
    insertupdate_user,
    UploadFileForm,
    insertfabicon,
    insertabout,
    insertEducation,
    insertothers,
    insertProgamming,
    insertwork,
)
from models import (
    db,
    User,
    fabicon,
    workexperience,
    Education,
    otherskill,
    skillprogamming,
    about,
)
from werkzeug.utils import secure_filename
import os
from PIL import Image


insert_authfab = Blueprint("insert_fab", __name__)
update_auth = Blueprint("update_data", __name__)
delete_auth = Blueprint("delete_data", __name__)


insert_authprogamming = Blueprint("insert_progamming", __name__)
update_authprogamming = Blueprint("update_data_progamming", __name__)
delete_authprogamming = Blueprint("delete_data_progamming", __name__)

insert_authothers = Blueprint("insert_others", __name__)
update_authothers = Blueprint("update_data_others", __name__)
delete_authothers = Blueprint("delete_data_others", __name__)

insert_authabout = Blueprint("insert_about", __name__)
update_authabout = Blueprint("update_data_about", __name__)
delete_authabout = Blueprint("delete_data_about", __name__)

insert_authwork = Blueprint("insert_work", __name__)
update_authwork = Blueprint("update_data_work", __name__)
delete_authwork = Blueprint("delete_data_work", __name__)

insert_autheducation = Blueprint("insert_education", __name__)
update_autheducation = Blueprint("update_data_education", __name__)
delete_autheducation = Blueprint("delete_data_education", __name__)


update_userauth = Blueprint("update_userdata", __name__)
uploadfoto_auth = Blueprint("uploadfoto_auth", __name__)
updatepassword_auth = Blueprint("updatepassword_auth", __name__)

UPLOAD_FOLDER = "Data_Foto/Foto_User"
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@insert_authfab.route("/insert_fabicon", methods=["POST"])
def insert_fabicon():
    form = insertfabicon()

    if form.validate_on_submit():
        titlez = form.title_fab.data
        icon = form.icon_fab.data
        url = form.href.data

        fabiconz = fabicon(title_fab=titlez, icon_fab=icon, href=url)

        db.session.add(fabiconz)
        db.session.commit()

        return redirect(url_for("Dashboard"))


@insert_authprogamming.route("/insert_progamming", methods=["POST"])
def insert_progamming():
    form = insertProgamming()

    if form.validate_on_submit():
        iconz = form.icon.data
        nama_skillz = form.nama_skill.data
        keterangan_skillz = form.keterangan_skill.data

        progammingz = skillprogamming(
            icon=iconz, nama_skill=nama_skillz, keterangan_skill=keterangan_skillz
        )

        db.session.add(progammingz)
        db.session.commit()

        return redirect(url_for("skill_progamming"))


@insert_authothers.route("/insert_others", methods=["POST"])
def insert_others():
    form = insertothers()

    if form.validate_on_submit():
        nama_skillz = form.nama_skill.data
        keterangan_skillz = form.keterangan_skill.data

        otherskillz = otherskill(
            nama_skill=nama_skillz, keterangan_skill=keterangan_skillz
        )

        db.session.add(otherskillz)
        db.session.commit()

        return redirect(url_for("Otherskill"))


@insert_authabout.route("/insert_about", methods=["POST"])
def insert_about():
    form = insertabout()

    if form.validate_on_submit():
        keterangan_Aboutz = form.keterangan_About.data
        aboutz = form.about.data
        tahun_aboutz = form.tahun_about.data

        aboutz = about(
            keterangan_About=keterangan_Aboutz, about=aboutz, tahun_about=tahun_aboutz
        )

        db.session.add(aboutz)
        db.session.commit()

        return redirect(url_for("About"))


@insert_authwork.route("/insert_work", methods=["POST"])
def insert_work():
    form = insertwork()

    if form.validate_on_submit():
        Jobz = form.Job.data
        Companyz = form.Company.data
        Yearsz = form.Years.data

        work = workexperience(Job=Jobz, Company=Companyz, Years=Yearsz)

        db.session.add(work)
        db.session.commit()

        return redirect(url_for("work"))


@insert_autheducation.route("/insert_education", methods=["POST"])
def insert_education():
    form = insertEducation()

    if form.validate_on_submit():
        Schoolz = form.School.data
        keterangan_schoolz = form.keterangan_school.data
        tahun_schoolz = form.tahun_school.data

        education = Education(
            School=Schoolz,
            keterangan_school=keterangan_schoolz,
            tahun_school=tahun_schoolz,
        )

        db.session.add(education)
        db.session.commit()

        return redirect(url_for("education"))


# UPDATE MYSQL


@update_userauth.route(
    "/update_user/<id>", methods=["GET", "POST"], endpoint="update_user"
)
def update_user(id):
    user = None

    if id.isdigit():
        # If the identifier is a digit, assume it's an ID
        user = User.query.get(int(id))
    else:
        # If it's not a digit, assume it's a username
        user = User.query.filter_by(username=id).first()

    if user is None:
        return redirect(url_for("Dashboard"))

    form = insertupdate_user(obj=user)

    if form.validate_on_submit():
        if request.method == "POST":
            if form.username.data:
                user.username = form.username.data
            if form.job.data:
                user.job = form.job.data
            if form.keterangan.data:
                user.keterangan = form.keterangan.data
            if form.email.data:
                user.email = form.email.data

    if id.isdigit():
        session["username"] = user.username
        db.session.commit()
        return redirect(url_for("Dashboard"))

    else:
        session["username"] = user.username
        db.session.commit()
        return redirect(url_for("profile"))


@update_auth.route("/update/<id>", methods=["GET", "POST"], endpoint="update")
def update(id):
    fabiconz = None

    if id.isdigit():
        fabiconz = fabicon.query.get(int(id))

    if fabiconz is None:
        return redirect(url_for("Dashboard"))

    form = insertfabicon(obj=fabiconz)

    if form.validate_on_submit():
        if request.method == "POST":
            if form.title_fab.data:
                fabiconz.title_fab = form.title_fab.data
            if form.icon_fab.data:
                fabiconz.icon_fab = form.icon_fab.data
            if form.href.data:
                fabiconz.href = form.href.data

        db.session.commit()
        return redirect(url_for("Dashboard"))


@update_authprogamming.route(
    "/update_progamming/<id>", methods=["GET", "POST"], endpoint="update_progamming"
)
def update_progamming(id):
    skillprogammingz = None

    if id.isdigit():
        skillprogammingz = skillprogamming.query.get(int(id))

    if skillprogammingz is None:
        return redirect(url_for("skill_progamming"))

    form = insertProgamming(obj=skillprogammingz)

    if form.validate_on_submit():
        if request.method == "POST":
            if form.icon.data:
                skillprogammingz.icon = form.icon.data
            if form.nama_skill.data:
                skillprogammingz.nama_skill = form.nama_skill.data
            if form.keterangan_skill.data:
                skillprogammingz.keterangan_skill = form.keterangan_skill.data

        db.session.commit()
        return redirect(url_for("skill_progamming"))


@update_authothers.route(
    "/update_others/<id>", methods=["GET", "POST"], endpoint="update_others"
)
def update_others(id):
    otherskillz = None

    if id.isdigit():
        otherskillz = otherskill.query.get(int(id))

    if otherskillz is None:
        return redirect(url_for("Otherskill"))

    form = insertothers(obj=otherskillz)

    if form.validate_on_submit():
        if request.method == "POST":
            if form.nama_skill.data:
                otherskillz.nama_skill = form.nama_skill.data
            if form.keterangan_skill.data:
                otherskillz.keterangan_skill = form.keterangan_skill.data

        db.session.commit()
        return redirect(url_for("Otherskill"))


@update_authabout.route(
    "/update_about/<id>", methods=["GET", "POST"], endpoint="update_about"
)
def update_about(id):
    aboutz = None

    if id.isdigit():
        aboutz = about.query.get(int(id))

    if aboutz is None:
        return redirect(url_for("About"))

    form = insertabout(obj=aboutz)

    if form.validate_on_submit():
        if request.method == "POST":
            if form.keterangan_About.data:
                aboutz.keterangan_About = form.keterangan_About.data
            if form.about.data:
                aboutz.about = form.about.data
            if form.tahun_about.data:
                aboutz.tahun_about = form.tahun_about.data

        db.session.commit()
        return redirect(url_for("About"))


@update_authwork.route(
    "/update_work/<id>", methods=["GET", "POST"], endpoint="update_work"
)
def update_work(id):
    workz = None

    if id.isdigit():
        workz = workexperience.query.get(int(id))

    if workz is None:
        return redirect(url_for("work"))

    form = insertwork(obj=workz)

    if form.validate_on_submit():
        if request.method == "POST":
            if form.Job.data:
                workz.Job = form.Job.data
            if form.Company.data:
                workz.Company = form.Company.data
            if form.Years.data:
                workz.Years = form.Years.data

        db.session.commit()
        return redirect(url_for("work"))


@update_autheducation.route(
    "/update_education/<id>", methods=["GET", "POST"], endpoint="update_education"
)
def update_education(id):
    educationz = None

    if id.isdigit():
        educationz = Education.query.get(int(id))

    if educationz is None:
        return redirect(url_for("education"))

    form = insertEducation(obj=educationz)

    if form.validate_on_submit():
        if request.method == "POST":
            if form.School.data:
                educationz.School = form.School.data
            if form.keterangan_school.data:
                educationz.keterangan_school = form.keterangan_school.data
            if form.tahun_school.data:
                educationz.tahun_school = form.tahun_school.data

        db.session.commit()
        return redirect(url_for("education"))


# DELETE MYSQL
@delete_auth.route("/delete/<int:id>", methods=["GET"])
def delete(id):
    fabiconz = fabicon.query.get(id)

    if fabiconz:
        db.session.delete(fabiconz)
        db.session.commit()
        return redirect(url_for("Dashboard"))
    else:
        return redirect(url_for("Dashboard"))


@delete_authprogamming.route("/delete_progamming/<int:id>", methods=["GET"])
def delete_progamming(id):
    skillprogammingz = skillprogamming.query.get(id)

    if skillprogammingz:
        db.session.delete(skillprogammingz)
        db.session.commit()
        return redirect(url_for("skill_progamming"))
    else:
        return redirect(url_for("skill_progamming"))


@delete_authothers.route("/delete_others/<int:id>", methods=["GET"])
def delete_others(id):
    others = otherskill.query.get(id)

    if others:
        db.session.delete(others)
        db.session.commit()
        return redirect(url_for("Otherskill"))
    else:
        return redirect(url_for("Otherskill"))


@delete_authabout.route("/delete_about/<int:id>", methods=["GET"])
def delete_about(id):
    aboutz = about.query.get(id)

    if aboutz:
        db.session.delete(aboutz)
        db.session.commit()
        return redirect(url_for("About"))
    else:
        return redirect(url_for("About"))


@delete_authwork.route("/delete_work/<int:id>", methods=["GET"])
def delete_work(id):
    work = workexperience.query.get(id)

    if work:
        db.session.delete(work)
        db.session.commit()
        return redirect(url_for("work"))
    else:
        return redirect(url_for("work"))


@delete_autheducation.route("/delete_education/<int:id>", methods=["GET"])
def delete_education(id):
    Educationz = Education.query.get(id)

    if Educationz:
        db.session.delete(Educationz)
        db.session.commit()
        return redirect(url_for("education"))
    else:
        return redirect(url_for("education"))


@uploadfoto_auth.route("/upload_foto/<id>", methods=["GET", "POST"])
def upload_foto(id):
    form = UploadFileForm()

    if form.validate_on_submit():
        try:
            file = form.foto_cv.data
            usernamez = form.username.data
            status = form.status.data

            if file and allowed_file(file.filename):
                upload_folder = os.path.join(
                    os.path.abspath(os.path.dirname(__file__)),
                    "static",
                    UPLOAD_FOLDER,
                    status,
                    usernamez,
                )
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)

                # Change this to your desired new filename and extension
                new_filename = usernamez + ".png"

                file_path = os.path.join(upload_folder, secure_filename(new_filename))
                file.save(file_path)

                if new_filename.lower().endswith(
                    ".jpg"
                ) or new_filename.lower().endswith(".jpeg"):
                    image = Image.open(file_path)
                    image.save(file_path, "PNG")

                if id.isdigit():
                    FotoUpload = os.path.join(
                        UPLOAD_FOLDER, status, usernamez, new_filename
                    )
                    user = User.query.get(int(id))
                    user.Foto_Profile = FotoUpload  # Use capital "F" for Foto_Profile
                else:
                    FotoUpload = os.path.join(
                        UPLOAD_FOLDER, status, usernamez, new_filename
                    )
                    user = User.query.filter_by(username=id).first()
                    user.Foto_Profile = FotoUpload  # Use capital "F" for Foto_Profile

                    if id.isdigit():
                        db.session.commit()
                        return redirect(url_for("profile"))
                    else:
                        db.session.commit()
                        return redirect(url_for("profile"))

        except Exception as e:
            db.session.rollback()  # Rollback changes in case of an error
            print(f"An error occurred while processing the file: {str(e)}")

    return redirect(url_for("profile"))


@updatepassword_auth.route("/change_password/<string:id>", methods=["POST"])
def change_password(id):
    current_password = request.form["current_password"]
    new_password = request.form["new_password"]
    confirm_password = request.form["confirm_password"]

    # Retrieve the user from the database (you should adapt this based on your authentication method)
    user = User.query.filter_by(email=id).first()

    if user:
        # Check if the current password matches the one stored in the database
        if user.password == current_password:
            if new_password == confirm_password:
                # Update the password in the database
                user.password = (
                    new_password  # Replace this line with your database update logic
                )
                db.session.commit()
                flash("Password updated successfully", "success")
                return redirect(url_for("profile"))
            else:
                flash("New password and confirmation password do not match", "danger")
                return redirect(url_for("profile"))

        else:
            flash("Incorrect current password", "danger")
            return redirect(url_for("profile"))
    else:
        flash("User not found", "danger")
        return redirect(url_for("profile"))

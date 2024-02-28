from flask import (
    Flask,
    redirect,
    url_for,
    render_template,
    make_response,
    request,
    session,
    flash,
)

from constant import (
    LOGINPAGE,
    INDEX,
    DASHBOARD,
    ABOUT,
    OTHER_SKILL,
    SKILL_PROGAMMING,
    WORK,
    PROFILE,
    EDUCATION,
    SERVER,
    USER_SERVER,
    PASSWORD_SERVER,
    DATABASE,
    colum_about,
    colum_education,
    colum_fab_icon,
    colum_others_skill,
    colum_skill_proagmming,
    colum_work,
)

from forms import (
    LoginForm,
    insertfabicon,
    insertabout,
    insertEducation,
    insertothers,
    insertProgamming,
    insertwork,
    insertupdate_user,
    UploadFileForm,
    UpdatePasswordForm,
)

from flask_wtf.csrf import CSRFProtect, generate_csrf
from sqlalchemy import create_engine
from sqlalchemy.orm import Session as SQLAlchemySession
import os
from datetime import datetime, timedelta
from models import (
    db,
    User,
    Sidebar,
    fabicon,
    skillprogamming,
    otherskill,
    Education,
    workexperience,
    about,
)
from mysql import (
    insert_authfab,
    insert_authabout,
    insert_autheducation,
    insert_authprogamming,
    insert_authwork,
    insert_authothers,
    update_auth,
    update_authabout,
    update_autheducation,
    update_authprogamming,
    update_authwork,
    update_authothers,
    delete_auth,
    delete_authabout,
    delete_autheducation,
    delete_authprogamming,
    delete_authothers,
    delete_authwork,
    uploadfoto_auth,
    updatepassword_auth,
    update_userauth,
)

app = Flask(__name__)


app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"mysql://{USER_SERVER}:{PASSWORD_SERVER}@{SERVER}/{DATABASE}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

app.permanent_session_lifetime = timedelta(days=30)
app.secret_key = "many random bytes"

csrf = CSRFProtect(app)
app.config["WTF_CSRF_TIME_LIMIT"] = 3600
app.register_blueprint(insert_authfab)
app.register_blueprint(update_auth)
app.register_blueprint(delete_auth)

app.register_blueprint(insert_authabout)
app.register_blueprint(update_authabout)
app.register_blueprint(delete_authabout)

app.register_blueprint(insert_autheducation)
app.register_blueprint(update_autheducation)
app.register_blueprint(delete_autheducation)


app.register_blueprint(insert_authprogamming)
app.register_blueprint(update_authprogamming)
app.register_blueprint(delete_authprogamming)

app.register_blueprint(insert_authothers)
app.register_blueprint(update_authothers)
app.register_blueprint(delete_authothers)

app.register_blueprint(insert_authwork)
app.register_blueprint(update_authwork)
app.register_blueprint(delete_authwork)

app.register_blueprint(update_userauth)
app.register_blueprint(uploadfoto_auth, url_prefix="/uploadfoto_auth")
app.register_blueprint(updatepassword_auth, url_prefix="/updatepassword_auth")


@app.route("/", methods=["GET", "POST"])
def index():
    user = User.query.all()
    skill = skillprogamming.query.all()
    fabicoz = fabicon.query.all()
    edu = Education.query.all()
    oter = otherskill.query.all()
    wok = workexperience.query.all()
    bout = about.query.all()

    modief_user = []
    modief_skill = []
    modief_fab = []
    modief_edu = []
    modief_oter = []
    modief_wok = []
    modief_abot = []

    for users in user:
        modif_user = [
            users.username,
            users.email,
            users.job,
            users.keterangan,
            users.Foto_Profile,
        ]
        modief_user.append(modif_user)

    for skillz in skill:
        modief_skillz = [
            skillz.icon,
            skillz.nama_skill,
            skillz.keterangan_skill,
        ]
        modief_skill.append(modief_skillz)

    for fabicox in fabicoz:
        modief_fabz = [
            fabicox.href,
            fabicox.title_fab,
            fabicox.icon_fab,
        ]
        modief_fab.append(modief_fabz)

    for edux in edu:
        modief_edux = [
            edux.School,
            edux.keterangan_school,
            edux.tahun_school,
        ]
        modief_edu.append(modief_edux)

    for oterz in oter:
        modief_oterz = [
            oterz.nama_skill,
            oterz.keterangan_skill,
        ]
        modief_oter.append(modief_oterz)

    for wokz in wok:
        modief_wokz = [wokz.Job, wokz.Company, wokz.Years]
        modief_wok.append(modief_wokz)

    for boutz in bout:
        modief_abotz = [boutz.about, boutz.keterangan_About, boutz.tahun_about]
        modief_abot.append(modief_abotz)

    html_content = render_template(
        INDEX,
        users=modief_user,
        progamming=modief_skill,
        fabicon=modief_fab,
        education=modief_edu,
        otherskill=modief_oter,
        aboutz=modief_abot,
        workex=modief_wok,
    )

    response = make_response(html_content)

    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, no-store"

    return response


@app.route("/login_cv", methods=["GET", "POST"])
def login_cv():
    username = request.cookies.get("username")

    if username:
        return redirect(url_for("Dashboard"))
    else:
        login_form = LoginForm()

        if request.method == "POST":
            if "submit_login" in request.form and login_form.validate_on_submit():
                email = login_form.email.data
                password = login_form.password.data
                user = User.query.filter_by(email=email).first()

                if user and user.password == password:
                    csrf_token = generate_csrf()
                    session["username"] = user.username
                    session["csrf_token"] = csrf_token
                    session["status"] = user.status

                    resp = make_response(redirect(url_for("Dashboard")))
                    expiration_date = datetime.now() + timedelta(days=30)
                    resp.set_cookie("username", user.username, expires=expiration_date)
                    resp.set_cookie("status", str(user.status), expires=expiration_date)
                    return resp
                else:
                    message = "Password atau Email Salah!!"
                    flash(message, "error")  # Flash the error message
                    return redirect(url_for("login_cv"))

    html_content = render_template(LOGINPAGE, login_form=login_form)

    response = make_response(html_content)

    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, no-store"

    return response


@app.route("/Dashboard", methods=["GET", "POST"])
def Dashboard():
    session.permanent = True
    if "username" not in session:
        return redirect(url_for("logout"))

    status = session.get("status")
    if status is not None:
        status = str(status)
        username = session["username"]
        csrf_token = session["csrf_token"]
        user_data = User.query.filter_by(username=username).first()
        iconfab = fabicon.query.all()

        if status == "2":
            form = insertfabicon()
            sidebar_items = []
            sidebar_data = Sidebar.query.filter_by(level_user=status).all()

            modified_fabicon = []

            for fab in iconfab:
                modified_icon = [
                    fab.id_fab,
                    fab.title_fab,
                    fab.icon_fab,
                    fab.href,
                ]
                modified_fabicon.append(modified_icon)

            # Modify the sidebar data as needed
            for item in sidebar_data:
                sidebar_item = {
                    "name": item.name_side,
                    "icon": item.icon_side,
                    "url": item.url_side,
                }
                sidebar_items.append(sidebar_item)

        data_list = [
            {
                "label": "title fab",
                "input_type": "text",
                "name": "title_fab",
                "value": "title_fab",
            },
            {
                "label": "Icon Fab",
                "input_type": "text",
                "name": "icon_fab",
                "value": "icon_fab",
            },
            {
                "label": "URL",
                "input_type": "text",
                "name": "href",
                "value": "href",
            },
        ]
        data_list1 = [
            {
                "label": "title fab",
                "input_type": "text",
                "name": "title_fab",
                "required": "1",
            },
            {
                "label": "Icon Fab",
                "input_type": "text",
                "name": "icon_fab",
                "required": "1",
            },
            {
                "label": "URL",
                "input_type": "text",
                "name": "href",
                "required": "1",
            },
        ]
    html_content = render_template(
        DASHBOARD,
        sidebar_items=sidebar_items,
        csrf_token=csrf_token,
        user=user_data,
        data_list1=data_list1,
        data_list=data_list,
        form=form,
        fab=modified_fabicon,
        colum_fab_icon=colum_fab_icon,
    )

    response = make_response(html_content)

    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, no-store"

    return response


@app.route("/skill_progamming", methods=["GET", "POST"])
def skill_progamming():
    session.permanent = True
    if "username" not in session:
        return redirect(url_for("logout"))

    status = session.get("status")
    if status is not None:
        status = str(status)
        username = session["username"]
        csrf_token = session["csrf_token"]
        user_data = User.query.filter_by(username=username).first()
        skillprogammingz = skillprogamming.query.all()

        if status == "2":
            form = insertProgamming()
            sidebar_items = []
            sidebar_data = Sidebar.query.filter_by(level_user=status).all()

            modified_skill = []

            for skill in skillprogammingz:
                modified_skillz = [
                    skill.id_skill,
                    skill.icon,
                    skill.nama_skill,
                    skill.keterangan_skill,
                ]
                modified_skill.append(modified_skillz)

            # Modify the sidebar data as needed
            for item in sidebar_data:
                sidebar_item = {
                    "name": item.name_side,
                    "icon": item.icon_side,
                    "url": item.url_side,
                }
                sidebar_items.append(sidebar_item)

        data_list = [
            {
                "label": "Icon",
                "input_type": "text",
                "name": "icon",
                "value": "icon",
            },
            {
                "label": "Nama Skill",
                "input_type": "text",
                "name": "nama_skill",
                "value": "nama_skill",
            },
            {
                "label": "Keterangan Skill",
                "input_type": "text",
                "name": "keterangan_skill",
                "value": "keterangan_skill",
            },
        ]
    data_list1 = [
        {
            "label": "icon",
            "input_type": "text",
            "name": "icon",
            "required": "1",
        },
        {
            "label": "Nama Skill",
            "input_type": "text",
            "name": "nama_skill",
            "required": "1",
        },
        {
            "label": "Keterangan Skill",
            "input_type": "text",
            "name": "keterangan_skill",
            "required": "1",
        },
    ]

    html_content = render_template(
        SKILL_PROGAMMING,
        sidebar_items=sidebar_items,
        csrf_token=csrf_token,
        user=user_data,
        data_list1=data_list1,
        data_list=data_list,
        form=form,
        fab=modified_skill,
        colum_skill_proagmming=colum_skill_proagmming,
    )

    response = make_response(html_content)

    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, no-store"

    return response


@app.route("/education", methods=["GET", "POST"])
def education():
    session.permanent = True
    if "username" not in session:
        return redirect(url_for("logout"))

    status = session.get("status")
    if status is not None:
        status = str(status)
        username = session["username"]
        csrf_token = session["csrf_token"]
        user_data = User.query.filter_by(username=username).first()
        Educationz = Education.query.all()

        if status == "2":
            form = insertEducation()
            sidebar_items = []
            sidebar_data = Sidebar.query.filter_by(level_user=status).all()

            modified_education = []

            for edu in Educationz:
                modified_eduztionz = [
                    edu.id_education,
                    edu.School,
                    edu.keterangan_school,
                    edu.tahun_school,
                ]
                modified_education.append(modified_eduztionz)

            # Modify the sidebar data as needed
            for item in sidebar_data:
                sidebar_item = {
                    "name": item.name_side,
                    "icon": item.icon_side,
                    "url": item.url_side,
                }
                sidebar_items.append(sidebar_item)

        data_list = [
            {
                "label": "School",
                "input_type": "text",
                "name": "School",
                "value": "School",
            },
            {
                "label": "Keterangan School",
                "input_type": "text",
                "name": "keterangan_school",
                "value": "keterangan_school",
            },
            {
                "label": "Tahun School",
                "input_type": "text",
                "name": "tahun_school",
                "value": "tahun_school",
            },
        ]
    data_list1 = [
        {
            "label": "School",
            "input_type": "text",
            "name": "School",
            "required": "1",
        },
        {
            "label": "Keterangan School",
            "input_type": "text",
            "name": "keterangan_school",
            "required": "1",
        },
        {
            "label": "Tahun School",
            "input_type": "text",
            "name": "tahun_school",
            "required": "1",
        },
    ]

    html_content = render_template(
        EDUCATION,
        sidebar_items=sidebar_items,
        csrf_token=csrf_token,
        user=user_data,
        data_list1=data_list1,
        data_list=data_list,
        form=form,
        fab=modified_education,
        colum_education=colum_education,
    )

    response = make_response(html_content)

    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, no-store"

    return response


@app.route("/About", methods=["GET", "POST"])
def About():
    session.permanent = True
    if "username" not in session:
        return redirect(url_for("logout"))

    status = session.get("status")
    if status is not None:
        status = str(status)
        username = session["username"]
        csrf_token = session["csrf_token"]
        user_data = User.query.filter_by(username=username).first()
        Aboutz = about.query.all()

        if status == "2":
            form = insertabout()
            sidebar_items = []
            sidebar_data = Sidebar.query.filter_by(level_user=status).all()

            modified_about = []

            for abot in Aboutz:
                modified_aboutz = [
                    abot.id_about,
                    abot.keterangan_About,
                    abot.about,
                    abot.tahun_about,
                ]
                modified_about.append(modified_aboutz)

            # Modify the sidebar data as needed
            for item in sidebar_data:
                sidebar_item = {
                    "name": item.name_side,
                    "icon": item.icon_side,
                    "url": item.url_side,
                }
                sidebar_items.append(sidebar_item)

        data_list = [
            {
                "label": "Keterangan About",
                "input_type": "text",
                "name": "keterangan_About",
                "value": "keterangan_About",
            },
            {
                "label": "About",
                "input_type": "text",
                "name": "about",
                "value": "about",
            },
            {
                "label": "Tahun About",
                "input_type": "text",
                "name": "tahun_about",
                "value": "tahun_about",
            },
        ]
    data_list1 = [
        {
            "label": "Keterangan About",
            "input_type": "text",
            "name": "keterangan_About",
            "required": "1",
        },
        {
            "label": "About",
            "input_type": "text",
            "name": "about",
            "required": "1",
        },
        {
            "label": "Tahun About",
            "input_type": "text",
            "name": "tahun_about",
            "required": "1",
        },
    ]

    html_content = render_template(
        ABOUT,
        sidebar_items=sidebar_items,
        csrf_token=csrf_token,
        user=user_data,
        data_list1=data_list1,
        data_list=data_list,
        form=form,
        fab=modified_about,
        colum_about=colum_about,
    )

    response = make_response(html_content)

    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, no-store"

    return response


@app.route("/Otherskill", methods=["GET", "POST"])
def Otherskill():
    session.permanent = True
    if "username" not in session:
        return redirect(url_for("logout"))

    status = session.get("status")
    if status is not None:
        status = str(status)
        username = session["username"]
        csrf_token = session["csrf_token"]
        user_data = User.query.filter_by(username=username).first()
        Othersz = otherskill.query.all()

        if status == "2":
            form = insertothers()
            sidebar_items = []
            sidebar_data = Sidebar.query.filter_by(level_user=status).all()

            modified_others = []

            for othe in Othersz:
                modified_othersz = [
                    othe.id_other_skill,
                    othe.nama_skill,
                    othe.keterangan_skill,
                ]
                modified_others.append(modified_othersz)

            # Modify the sidebar data as needed
            for item in sidebar_data:
                sidebar_item = {
                    "name": item.name_side,
                    "icon": item.icon_side,
                    "url": item.url_side,
                }
                sidebar_items.append(sidebar_item)

        data_list = [
            {
                "label": "Nama Skill",
                "input_type": "text",
                "name": "nama_skill",
                "value": "nama_skill",
            },
            {
                "label": "Keterangan Skill",
                "input_type": "text",
                "name": "keterangan_skill",
                "value": "keterangan_skill",
            },
        ]
    data_list1 = [
        {
            "label": "Nama Skill",
            "input_type": "text",
            "name": "nama_skill",
            "required": "1",
        },
        {
            "label": "Keterangan Skill",
            "input_type": "text",
            "name": "keterangan_skill",
            "required": "1",
        },
    ]

    html_content = render_template(
        OTHER_SKILL,
        sidebar_items=sidebar_items,
        csrf_token=csrf_token,
        user=user_data,
        data_list1=data_list1,
        data_list=data_list,
        form=form,
        fab=modified_others,
        colum_others_skill=colum_others_skill,
    )

    response = make_response(html_content)

    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, no-store"

    return response


@app.route("/work", methods=["GET", "POST"])
def work():
    session.permanent = True
    if "username" not in session:
        return redirect(url_for("logout"))

    status = session.get("status")
    if status is not None:
        status = str(status)
        username = session["username"]
        csrf_token = session["csrf_token"]
        user_data = User.query.filter_by(username=username).first()
        Worksz = workexperience.query.all()

        if status == "2":
            form = insertwork()
            sidebar_items = []
            sidebar_data = Sidebar.query.filter_by(level_user=status).all()

            modified_work = []

            for wor in Worksz:
                modified_worksz = [wor.id_work, wor.Job, wor.Company, wor.Years]
                modified_work.append(modified_worksz)

            # Modify the sidebar data as needed
            for item in sidebar_data:
                sidebar_item = {
                    "name": item.name_side,
                    "icon": item.icon_side,
                    "url": item.url_side,
                }
                sidebar_items.append(sidebar_item)

        data_list = [
            {
                "label": "JOB",
                "input_type": "text",
                "name": "Job",
                "value": "Job",
            },
            {
                "label": "Company",
                "input_type": "text",
                "name": "Company",
                "value": "Company",
            },
            {
                "label": "Years",
                "input_type": "text",
                "name": "Years",
                "value": "Years",
            },
        ]
    data_list1 = [
        {
            "label": "JOB",
            "input_type": "text",
            "name": "Job",
            "required": "1",
        },
        {
            "label": "Company",
            "input_type": "text",
            "name": "Company",
            "required": "1",
        },
        {
            "label": "Years",
            "input_type": "text",
            "name": "Years",
            "required": "1",
        },
    ]

    html_content = render_template(
        WORK,
        sidebar_items=sidebar_items,
        csrf_token=csrf_token,
        user=user_data,
        data_list1=data_list1,
        data_list=data_list,
        form=form,
        fab=modified_work,
        colum_work=colum_work,
    )

    response = make_response(html_content)

    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, no-store"

    return response


@app.route("/profile", methods=["GET", "POST"])
def profile():
    session.permanent = True

    if "username" not in session:
        return redirect(
            url_for("login_cv")
        )  # Redirect to the login page if not logged in

    # Get the currently logged-in user's username from the session

    form = insertupdate_user()
    form1 = UploadFileForm()
    form2 = UpdatePasswordForm()
    usernamez = session["username"]
    csrf_token = session["csrf_token"]
    # Query the database to retrieve the user's data
    user = User.query.filter_by(username=usernamez).first()

    sidebar_items = []  # Define it at the beginning
    sidebar_data = (
        Sidebar.query.all()
    )  # Fetch all sidebar items (replace 'Sidebar' with your actual model name)

    # Modify the sidebar data as needed
    for item in sidebar_data:
        sidebar_item = {
            "name": item.name_side,
            "icon": item.icon_side,
            "url": item.url_side,
        }
        sidebar_items.append(sidebar_item)

    html_content = render_template(
        PROFILE,
        sidebar_items=sidebar_items,
        user=user,
        form=form,
        form1=form1,
        form2=form2,
        csrf_token=csrf_token,
    )

    response = make_response(html_content)

    # Set the Cache-Control header to prevent caching
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, no-store"

    return response


@app.route("/logout")
def logout():
    session.pop("username", None)

    resp = make_response(redirect(url_for("login_cv")))
    resp.delete_cookie("username")
    return resp


if __name__ == "__main__":
    app.run(debug=True, port=5009)

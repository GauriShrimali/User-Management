from flask import Flask, render_template, jsonify, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

engine = create_engine('sqlite:///usermanagement.db', echo=True)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123@localhost:3306/user'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)


class UserManagement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(45))
    lname = db.Column(db.String(45))
    email = db.Column(db.String(45))
    contact_no = db.Column(db.String(45))
    type = db.Column(db.String(45))
    uname = db.Column(db.String(45), primary_key=True)
    psw = db.Column(db.String(120))
    salary = db.Column(db.Integer)


@app.route('/')
def index():
    return render_template("login.html")


@app.route('/add', methods=['POST', 'GET'])
def add():
    user_data = request.json['user_data']
    user_obj = UserManagement()

    user_obj.contact_no = user_data['contact']
    user_obj.fname = user_data['fname']
    user_obj.lname = user_data['lname']
    user_obj.email = user_data['email']
    user_obj.id = user_data['id']
    user_obj.uname = user_data['uname']
    user_obj.salary = user_data['salary']
    user_obj.psw = generate_password_hash(user_data['psw'])
    user_obj.type = user_data['type']

    db.session.add(user_obj)
    db.session.commit()

    return 'index.html'


@app.route('/get_user', methods=["GET", "POST"])
def get_user():
    offset_value = request.json['offset_value']
    emp_data = [
        {'id': k.id, 'contact': k.contact_no, 'fname': k.fname, 'lname': k.lname, 'email': k.email, 'type': k.type, 'salary': k.salary} for
        k in UserManagement.query.limit(5).offset(offset_value).all()]
    return jsonify(emp_data=emp_data)


@app.route('/edit_user', methods=["POST", "GET"])
def edit_user():
    user_edit = request.json['user_edit']
    user_id = request.json['user_id']

    emp_edit = UserManagement().query.filter(UserManagement.id.like(user_id)).first()
    emp_edit.id = user_edit['id']
    emp_edit.fname = user_edit['fname']
    emp_edit.lname = user_edit['lname']
    emp_edit.email = user_edit['email']
    emp_edit.contact_no = user_edit['contact']
    emp_edit.salary = user_edit['salary']
    emp_edit.type = user_edit['type']
    db.session.add(emp_edit)
    db.session.commit()

    return 'index.html'


@app.route('/delete_user', methods=["POST", "GET"])
def delete_user():
    del_id = request.json['del_id']
    del_emp = UserManagement().query.filter(UserManagement.id.like(del_id)).first()
    db.session.delete(del_emp)
    db.session.commit()

    return 'index.html'


@app.route('/sign_up', methods=["POST", "GET"])
def sign_up():
    try:
        login_uname = request.form.get('uname')
        login_psw = request.form.get('psw')
        uname_login = UserManagement.query.filter(UserManagement.uname.like(login_uname), UserManagement.psw.like(login_psw)).first()
        if uname_login is None:
            return render_template("signUp.html")
        else:
            return render_template("login.html")
    except:
        flash("Incorrect Password or Username!")
        return render_template("login.html")


@app.route('/log_in', methods=["POST", "GET"])
def log_in():
    try:
        login_uname = request.form.get('uname', '')
        login_psw = request.form.get('psw', '')
        session['username'] = request.form['uname']
        session['psw'] = request.form['psw']
        login_type = UserManagement.query.filter(UserManagement.uname.like(login_uname)).first().type
        session['type'] = login_type
        uname_login = UserManagement.query.filter((UserManagement.uname.like(login_uname))).first()
        uname_psw = UserManagement.query.filter((UserManagement.uname.like(login_uname))).first().psw
        if uname_login is None:
            flash("Incorrect Password or Username!", category="warning")
            return render_template("login.html")

        else:
            if check_password_hash(uname_psw, login_psw):
                if request.form['uname'] == session['username'] and session['type'] == 'Admin':
                    flash(str("Logged in successfully as " + session['username']), category="success")
                    return render_template("index.html")

                elif request.form['uname'] == session['username'] and session['type'] == 'User':
                    flash(str("Logged in successfully as " + session['username']), category="success")
                    return render_template("index.html")
            else:
                flash("Incorrect Password or Username!", category="warning")
                return render_template("login.html")
    except:
        flash("User does not exist!", category="danger")
        return render_template("login.html")


@app.route('/signed_up', methods=["POST", "GET"])
def signed_up():
    try:
        signup_obj = UserManagement()
        login_id = request.form.get('id')
        login_fname = request.form.get('fname')
        login_lname = request.form.get('lname')
        login_contact = request.form.get('contact')
        login_salary = request.form.get('salary')
        login_uname = request.form.get('uname')
        login_email = request.form.get('email')
        login_type = request.form.get('type')
        login_psw = request.form.get('psw')
        login_re_psw = request.form.get('re_psw')

        if login_psw == login_re_psw:
            signup_obj.id = login_id
            signup_obj.fname = login_fname
            signup_obj.lname = login_lname
            signup_obj.contact_no = login_contact
            signup_obj.salary = login_salary
            signup_obj.uname = login_uname
            signup_obj.email = login_email
            signup_obj.type = login_type
            signup_obj.psw = generate_password_hash(login_psw)
            db.session.add(signup_obj)
            db.session.commit()
            flash('Successfully Signed Up!', category="signed_up")
            return render_template("login.html")
        else:
            flash('Invalid Credentials', category="invalid")
            return render_template("signUp.html")
    except:
        flash("User Exists!", category="error")
        return render_template("signUp.html")


@app.route('/logout', methods=["POST", "GET"])
def logout():
    session.pop(session['username'], None)
    flash(str('Logged out as ' + session['username']), category="logout")
    return render_template("login.html")


@app.route('/profile_user', methods=["POST", "GET"])
def profile_user():
    profile_uname = session['username']
    profile_psw = session['psw']
    profile_email = UserManagement.query.filter(UserManagement.uname.like(profile_uname)).first().email
    return jsonify(profile_uname=profile_uname, profile_psw=profile_psw, profile_email=profile_email)


@app.route('/profile_delete', methods=["POST", "GET"])
def profile_delete():
    profile_uname = session['username']
    del_profile = UserManagement().query.filter(UserManagement.uname.like(profile_uname)).first()
    db.session.delete(del_profile)
    db.session.commit()
    flash(session['username']+"'s account deleted!", category="deleted")
    return render_template("login.html")


@app.route('/update_psw', methods=["POST", "GET"])
def update_psw():
    update_uname = session['username']
    oldPsw = request.form.get('oldPsw')
    newPsw = request.form.get('newPsw')
    psw = UserManagement.query.filter(UserManagement.uname.like(update_uname)).first().psw
    if check_password_hash(psw, oldPsw):
        update_user = UserManagement.query.filter(UserManagement.uname.like(update_uname)).first()
        update_user.psw = generate_password_hash(newPsw)
        flash('Password changed!', category="correct")
        db.session.commit()
        return render_template("index.html")
    else:
        flash('Incorrect password!', category="incorrect")
        return render_template("index.html")


@app.route('/total_records', methods=["POST", "GET"])
def total_records():
    import math
    total_rec = UserManagement.query.count()
    pg = int(math.ceil(total_rec/5)) + 1

    role = session['type']
    return jsonify(pg=pg, role=role)


@app.route('/get_id', methods=["POST", "GET"])
def get_id():
    user_list = UserManagement.query.all()
    name = []
    salary = []
    for item in user_list:
        name.append(item.fname)
        salary.append(item.salary)
    return jsonify(name=name, salary=salary)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

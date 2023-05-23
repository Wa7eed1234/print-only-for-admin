from flask import Flask, render_template, request, url_for, session
from werkzeug.utils import redirect
from flask import Flask,render_template,request
from werkzeug.utils import redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
app = Flask(__name__)
# data base
app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
with app.app_context():
    class User(UserMixin, db.Model):
        __tablename__ = 'User'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), unique=True)
        password = db.Column(db.String(100))
        money = db.Column(db.Integer)
        is_admin = db.Column(db.Boolean, nullable=False, default=False)


    db.session.commit()
    db.create_all()
class MyModelView(ModelView):
    def is_accessible(self):

            return True
admin = Admin(app)
admin.add_view(MyModelView(User, db.session))


@app.route("/")
def start():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        user = User.query.filter_by(name=name, password=password).first()
        if user:
            if user.is_admin:
                users_list = User.query.all()
                return render_template("money.html", namey=[u.name for u in users_list], money=[u.money for u in users_list])
            else:
                return "The money has been paid to master mahmoud"
        else:
            return redirect("/register")
    return render_template("login.html")

@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
      name=request.form.get("name")
      password=request.form.get("password")
      money=request.form.get("money")
      new=User(
          name=name,
          password=password,
          money=money,
      )

      db.session.add(new)
      db.session.commit()
      return redirect("/login")
    return render_template("register.html")

if __name__==("__main__"):
    app.run(debug=True)
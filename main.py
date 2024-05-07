import mongo
from flask import *

app = Flask(__name__)
app.secret_key = "lkjsfdbjgjbs"
db = mongo.DataBase()


@app.route("/")
def index():
    return render_template("index.html")



@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        print("post")
        username = request.form["username"]
        password = request.form["password"]
        db.register(username, password)

    return render_template("registration.html")


@app.route("/login", methods =["GET", "POST"])
def login():
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        result = db.login(username, password)
        if result:
            session["username"] = result["username"]
        else:
            return "неверное имя пользователя или пароль"
        
    return render_template("login.html", username = session.get("username", False))


@app.route("/logout")
def logout():
    session.clear()
    return render_template("index.html")


@app.route("/make_ticket", methods = ["GET", "POST"])
def make_ticket():
    if request.method == "POST":
        username = session.get("username", False)
        if username:
            number = request.form["number"]
            description = request.form["description"]
            
            db.violations(username, number, description)
        else:
            print("Ты не в сессии, чебуркек")
    return render_template("make_ticket.html")

@app.route("/account")
def account():
    username = session.get("username", False)
    return render_template("account.html", username = username, docs=db.getTickets(username))

@app.route("/admin", methods = ["GET", "POST"])
def adminPanel():
    if db.admin(session["username"]):
        docs = db.getAllTickets()
        if request.method == "POST":
            _id = request.form["_id"]
            todo = request.form["select"]
            db.editTickets(_id, todo)
            
        
        
        return render_template("admin.html", docs=docs)
    
    else:
        return "404"
    
@app.route("/about")
def about():
    return render_template("about.html", username=session.get("username"))

@app.route("/rules")
def rules():
    return render_template("rules.html", username=session.get("username"))

@app.route("/contacts")
def contacts():
    return render_template("contacts.html", username=session.get("username"))


if __name__ == "__main__":
    app.run(debug=True)



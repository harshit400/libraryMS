from flask import Flask,render_template, request, redirect, url_for, session
import mysql.connector as sql

app=Flask(__name__)
@app.route("/",methods=["POST","GET"])
def inn():
    return render_template("registration.html")

#########   registration page   ###############   registration page   ################   registration page
@app.route("/ff",methods=["POST","GET"])
def registraton():
    con = sql.connect(host="localhost", password="harshit", user="root", database="library")
    cur = con.cursor()
    if request.form.get("submit"):
        roll_no = request.form.get("roll_no")
        name = request.form.get("name")
        phone_no = request.form.get("phone_no")
        email = request.form.get("email")
        password = request.form.get("password")
        values = (roll_no,name,phone_no,email,password)
        cur.execute("insert into register values(%s,%s,%s,%s,%s)", values)
        con.commit()
        con.close()
        return redirect(url_for('login'))
    else :
        return render_template("registration.html")

##############   login page   ######################   login page   #####################   login page   #####################login page
@app.route("/login",methods=["POST","GET"])
def login():
    con = sql.connect(host="localhost", password="harshit", user="root", database="library")
    cur = con.cursor()
    if (request.method == "POST"):
        roll_no = request.form.get("username")   # username=  roll_no , phone_no , email
        password = request.form.get("password")
        cur.execute("select roll_no,password from register where roll_no=%s ",(roll_no,)) # ======[(roll_no,),(password,)]
        user_input = cur.fetchall()
        con.commit()
        con.close()
        if int(roll_no)==user_input[0][0] and password==user_input[0][1]:
            return redirect(url_for('index'))
        else :
            return ("incorect username and password")
    else:
        return render_template("login.html")

##############   index page  ######################   index page  #####################   index page  #####################
@app.route("/index",methods=["POST","GET"])
def index():
    #mysql connector
    con = sql.connect(host="localhost", password="harshit", user="root", database="library")
    cur = con.cursor()

    if (request.method == "POST"):
        search = request.form.get("search")  # search bar in webiste
        # fetching the data from database with the using of search bar
        if search in ["all","ALL","ALl","All","AlL","aLL","aLl","alL",""," "]:
            cur.execute("select * from book")
            books_data = cur.fetchall()
        else :
            cur.execute("select * from book where book_title=%s",(search,))
            books_data = cur.fetchall()
            if len(books_data) == 0:
                books_data=[0]

    # fetching all data from the defolt database (opening the website)
    else:
        cur.execute("select * from book")  # fetch all data
        books_data = cur.fetchall()
    con.commit()
    con.close()
    return render_template( "ind.html",books_data=books_data)


@app.route("/about", methods=["POST", "GET"])
def about():
    return render_template( "about.html")

@app.route("/contact", methods=["POST", "GET"])
def contact():
    return render_template( "contact.html")





#$$$$$$$$$$$$$$$$$$$$$$   admin  $$$$$$$$$$$$$$$$$$$$$$$$$$$   admin  $$$$$$$$$$$$$$$$$$$$$$$$   admin  $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#$$$$$$$$$$$$$$$$$$$$$$   admin  $$$$$$$$$$$$$$$$$$$$$$$$$$$   admin  $$$$$$$$$$$$$$$$$$$$$$$$   admin  $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#$$$$$$$$$$$$$$$$$$$$$$   admin  $$$$$$$$$$$$$$$$$$$$$$$$$$$   admin  $$$$$$$$$$$$$$$$$$$$$$$$   admin  $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#$$$$$$$$$$$$$$$$$$$$$$   admin  $$$$$$$$$$$$$$$$$$$$$$$$$$$   admin  $$$$$$$$$$$$$$$$$$$$$$$$   admin  $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
@app.route("/admin_login", methods=["POST", "GET"])
def admin_login():
    return render_template( "admin_login.html")

@app.route("/admin_page", methods=["POST", "GET"])
def admin_page():
    con = sql.connect(host="localhost", password="harshit", user="root", database="library")
    cur = con.cursor()
    username = request.form.get("username")
    password = request.form.get("password")
    cur.execute("select * from admin")  # fetch all data
    main = cur.fetchall()
    con.commit()
    con.close()
    print(username,password)
    print(main)
    if username==main[0][0] and password==main[0][1]:
        return render_template( "library_m_s.html")
    else :
        return("incorect username and password")

@app.route("/admin_manage_books", methods=["POST", "GET"])
def admin_manage_books():
    con = sql.connect(host="localhost", password="harshit", user="root", database="library")
    cur = con.cursor()

    if (request.method == "POST"):
        coverUrl = request.form.get("coverUrl")
        title = request.form.get("title")
        author = request.form.get("author")
        values = (coverUrl, title, author)
        cur.execute("insert into book values(%s,%s,%s)", values)
        con.commit()
        con.close()
        return redirect(url_for('admin_manage_books'))
    else :
        cur.execute("select * from book")  # fetch all data
        books_data = cur.fetchall()
        con.commit()
        con.close()
        return render_template("manage_books.html",books_data=books_data)


@app.route("/admin_IssueAndReturn_books", methods=["POST", "GET"])
def admin_IssueAndReturn_books():
    con = sql.connect(host="localhost", password="harshit", user="root", database="library")
    cur = con.cursor()

    if (request.method == "POST"):
        title = request.form.get("title")
        roll_no = request.form.get("roll_no")
        issue_date = request.form.get("issue_date")
        due_dte = request.form.get("due_date")
        values = (title,roll_no,issue_date,due_dte)
        cur.execute("insert into books_issue values(%s,%s,%s,%s)", values)
        con.commit()
        con.close()
        return redirect(url_for('admin_IssueAndReturn_books'))
    else :
        cur.execute("select * from books_issue")  # fetch all data
        issue = cur.fetchall()
        con.commit()
        con.close()
        return render_template("issued.html", data=issue)


if __name__ == '__main__':
    app.run(debug=True)

import datetime
import threading
from flask import Flask, render_template, request, session, url_for, redirect
import psycopg2
import sqlite3 as sql

app = Flask(__name__, template_folder="templates")
app.config['SECRET_KEY'] = "bc916900ed8190ab5ffa1943c63827ae3317d303"
app.permanent_session_lifetime = datetime.timedelta(days=2)


# class Data:
#     def __init__(self, sess_data):
#         self.sess_data = sess_data
#         self.data_users = return_db_user(name_db="todo.db")
#         self.data_tasks = return_user_tasks(sess_data=sess_data, name_db="todo.db")
#         self.id_user = get_id_user(data_users=self.data_users, sess_data=sess_data)
#         self.login_user = get_login_user(data_users=self.data_users, sess_data=sess_data)
#

def get_login_user(sess_data):
    data_users = return_db_user()
    for i in data_users:
        if i[0] == sess_data:
            login_user = i[1]
            return login_user


def get_id_user(sess_data):
    data_users = return_db_user()
    for i in data_users:
        if i[0] == sess_data:
            id_user = i[0]
            return id_user


def return_user_tasks(sess_data, name_db="todo.db"):
    with sql.connect(name_db) as con:
        cur = con.cursor()
        cur.execute(f"""
                    SELECT * FROM tasks
                    """)
        data_tasks = cur.fetchall()
    datas = []
    for data_one in data_tasks:
        if data_one[1] == sess_data:
            datas.append(data_one)
    return datas


def return_db_user(name_db="todo.db"):
    data_users = None
    with sql.connect(name_db) as con:
        cur = con.cursor()
        cur.execute(f"""
                      SELECT * FROM users
                      """)
        data_users = cur.fetchall()
    return data_users


def insert_new_user(new_login, new_password):
    with sql.connect("todo.db") as con:
        cur = con.cursor()
        cur.execute(f"""
                INSERT INTO users (login,password) VALUES('{new_login}','{new_password}')
                """)


def insert_new_task(id_user, title, description):
    with sql.connect("todo.db") as con:
        cur = con.cursor()
        cur.execute(
            f"""INSERT INTO tasks (id_user,title,description,status) VALUES({id_user},'{title}','{description}',"no")""")


# def get_data_tasks():
#     data = []
#     index = 0
#     user_data = connect_db_user()
#     data_tasks = connect_db_task()
#     for i in user_data:
#         if i[0] == session["login"]:
#             id_user = i[0]
#             login_user = i[1]
#             for data_task in data_tasks:
#                 if data_task[1] == id_user:
#                     data.append({"id": data_task[0], "title": data_task[2], "description": data_task[3],
#                                  "url": f"get_task_{index}", "status": f"{data_task[4][:-1][1:]}"})
#                     index += 1
#     return data


@app.route("/", methods=['POST', 'GET'])
@app.route("/login", methods=['POST', 'GET'])
def login(error="", post=""):
    try:
        post = request.form['post']
    except:
        post = ""

    # Проверка на существование сессии, если она есть то переадресуемся в home.html
    if 'id' in session and session["id"] != 0:

        # id_user = get_id_user(session["id"])
        # login_user = get_login_user(session["id"])
        id_user = get_id_user(session["id"])
        login_user = get_login_user(session["id"])
        return redirect(url_for('.home', id_user=id_user, login_user=login_user))
    else:
        if request.method == "POST":
            if post == "login":
                new_login = request.form['new_login']
                new_password = request.form['new_password']
                if new_login == "" or new_password == "":
                    return render_template('login.html', error="Логин или пароль не введен")
                elif new_login == "":
                    return render_template('login.html', error="Логин не введен")
                elif new_password == "":
                    return render_template('login.html', error="Пароль не введен")
                else:

                    user_data = return_db_user()
                    for i in user_data:
                        if i[1] == new_login and i[2] == new_password:
                            return render_template('login.html', error="Такой пользователь уже существует")

                    insert_new_user(new_login, new_password)

                    data_session = 0
                    user_data = return_db_user()
                    for i in user_data:
                        if i[0] > data_session:
                            data_session = i[0]
                    session["id"] = data_session

                    id_user = get_id_user(sess_data=session['id'])
                    login_user = get_login_user(sess_data=session['id'])

                    return redirect(url_for('.home', id_user=id_user, login_user=login_user))
            elif post == "auth":
                log = request.form['login']
                password = request.form['password']
                if log == "" or password == "":
                    return render_template('login.html', error="Логин или пароль введен неверно")
                else:
                    data_users = return_db_user()
                    for i in data_users:
                        if i[1] == log and i[2] == password:
                            session["id"] = i[0]

                            id_user = get_id_user(sess_data=session['id'])
                            login_user = get_login_user(sess_data=session['id'])

                            return redirect(url_for('.home', id_user=id_user, login_user=login_user))
                    return render_template('login.html', error="Такого пользователя не существует")
        return render_template('login.html')


@app.route("/exit", methods=['POST', 'GET'])
def exit():
    # session.modified()
    session["id"] = 0

    return render_template('login.html')


@app.route("/home/<id_user>/<login_user>", methods=['GET', 'POST'])
def home(id_user, login_user):
    # if request.method == "POST":
    #     title = request.form['title']
    #     description = request.form['description']
    #
    #     with sql.connect("todo.db") as con:
    #         cur = con.cursor()
    #         cur.execute(f"""INSERT INTO tasks (id_user,title,description) VALUES({1},'{title}','{description}')""")
    #     data = []
    #     index = 0
    #     user_data = connect_db_user()
    #     data_tasks = connect_db_task()
    #     for i in user_data:
    #         if i[0] == session["login"]:
    #             id_user = i[0]
    #             login_user = i[1]
    #             data = get_data_tasks()
    #     return render_template('home.html', id_user=id_user, login_user=login_user, data_task=data)
    if 'id' in session and session["id"] != 0:
        id_user = get_id_user(sess_data=session['id'])
        login_user = get_login_user(sess_data=session['id'])
        data = return_user_tasks(sess_data=session['id'])
        return render_template('home.html', id_user=id_user, login_user=login_user, data_task=data)
    else:
        return render_template('login.html')


@app.route("/get_task/<string:id_user>/<string:id_task>")
def get_task(id_user, id_task):
    if 'id' in session and session["id"] != "0":
        data_tasks = return_user_tasks(sess_data=session['id'])
        login_user = get_login_user(sess_data=session['id'])
        title = None
        description = None
        for data_task in data_tasks:
            if f"{data_task[0]}" == f"{id_task}" and f"{data_task[1]}" == f"{id_user}":
                title = data_task[2]
                description = data_task[3]
        return render_template('TodoDetail.html', id_user=id_user, login_user=login_user, id_task=id_task, title=title,
                               description=description)
    else:
        return render_template('login.html')


@app.route("/add_task/<id_user>", methods=['POST', 'GET'])
def add_task(id_user):
    if 'id' in session and session["id"] != "0":
        login_user = get_login_user(sess_data=session['id'])
        if request.method == "POST":
            title = request.form['title']
            description = request.form['description']

            if title == "":
                return render_template(url_for('.add_task', id_user=id_user, login_user=login_user))

            else:

                insert_new_task(id_user, title, description)
                return redirect(url_for('.home', id_user=id_user, login_user=login_user))
        else:
            return render_template('TodoAdd.html', id_user=id_user, login_user=login_user)
    else:
        return render_template('login.html')


@app.route("/update_task_status/<string:id_user>/<string:id_task>", methods=['POST', 'GET'])
def update_task_status(id_user, id_task):
    if 'id' in session and session["id"] != "0":
        with sql.connect("todo.db") as con:
            cur = con.cursor()
            cur.execute(
                f"""UPDATE tasks SET status == 'yes' WHERE ID == '{id_task}'""")
        login_user = get_login_user(sess_data=session['id'])
        return redirect(url_for('.home', id_user=id_user, login_user=login_user))
    else:
        return render_template('login.html')



@app.route("/delete_task/<string:id_user>/<string:id_task>", methods=['POST', 'GET'])
def delete_task(id_user="", id_task=""):
    if 'id' in session and session["id"] != "0":
        with sql.connect("todo.db") as con:
            cur = con.cursor()
            cur.execute(
                f"""DELETE FROM tasks WHERE ID == '{id_task}'""")
        login_user = get_login_user(sess_data=session['id'])
        return redirect(url_for('.home', id_user=id_user, login_user=login_user))
    else:
        return render_template('login.html')



@app.route("/update_task", methods=['POST', 'GET'])
def update_task():
    if 'id' in session and session["id"] != "0":
        id_user = get_id_user(sess_data=session['id'])
        login_user = get_login_user(sess_data=session['id'])
        if request.method == "POST":
            title = request.form['title']
            description = request.form['description']
            id_task = request.form['id_task']

            with sql.connect("todo.db") as con:
                cur = con.cursor()
                cur.execute(
                    f"""UPDATE tasks SET title == '{title}', description == '{description}' WHERE ID == '{id_task}'""")

        return redirect(url_for('.home', id_user=id_user, login_user=login_user))
    else:
        return render_template('login.html')





if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)

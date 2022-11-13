from flask import Flask, render_template, url_for, jsonify,\
                    request, redirect, session

import code_password
from data import queries
from dotenv import load_dotenv
import bcrypt

load_dotenv()
app = Flask('codecool_series')

app.secret_key = b'_5#y2L"F4Q8z\xec]/'


@app.route('/')
def index():
    shows = queries.get_shows()
    return render_template('index.html', shows=shows)


@app.route('/design')
def design():
    return render_template('design.html')


@app.route('/simulation1')
def simulations():
    shows = queries.get_shows_from_1980s()
    return render_template('simulation1.html', shows=shows)


@app.route('/shows/most-rated/<int:_id>')
def most_rated(_id):
    offset = _id * 15
    shows = queries.get_most_rated_shows(offset)
    return render_template('shows-most-rated.html', shows=shows)


@app.route('/actors/')
def get_hundred_actors():
    actors = queries.get_hundred_actors()
    return render_template('actors.html', actors=actors)


@app.route('/tv-show/<int:show_id>', methods=["GET", "POST"])
def show(show_id):
    shows = queries.get_show_by_id()
    actors = queries.get_show_actors(show_id)
    seasons = queries.get_show_seasons(show_id)
    runtime = ""
    formatted_date = ""
    for item in shows:
        if item['id'] == show_id:
            for _ in item:
                formatted_date = item['year'].strftime("%d %b %Y")
                if item['runtime'] < 60:
                    runtime = "{} mins".format(item['runtime'])
                if item['runtime'] == 60:
                    runtime = "1h"
                if item['runtime'] > 60:
                    hours = item['runtime'] // 60
                    minutes = item['runtime'] % 60
                    runtime = "{}h:{} mins".format(hours, minutes)
    return render_template("show.html", shows=shows, show_id=show_id, runtime=runtime, actors=actors,
                           formatted_date=formatted_date, seasons=seasons)


@app.route('/api/all_shows_actor_starred/<id>')
def all_shows_actor_starred(id):
    shows = queries.get_shows_starred(id)
    return jsonify(shows)


@app.route('/api/actors_for_simulation_shows/<id>')
def actors_for_simulation_shows(id):
    actors_in_sim_shows = queries.get_show_actors(id)
    return jsonify(actors_in_sim_shows)


@app.route('/login', methods=['POST', 'GET'])
def login():
    message = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if queries.valid_login(username):
            hash_pass = queries.valid_login(username)[0]["password"]
            if code_password.verify_password(password, hash_pass):
                session["username"] = username
                return redirect(url_for("index"))
            else:
                message = "Invalid password"
        else:
            message = "Invalid username"

    return render_template("login.html", message=message)


@app.route("/register", methods=["GET", "POST"])
def registration_user():
    message = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        try:
            if username and password:
                hash_pass = str(code_password.hash_password(password))
                for elem in queries.get_all_users():
                    if username == elem["username"]:
                        raise KeyError
                session["username"] = username
                queries.add_user_to_database(username, hash_pass)
                return redirect(url_for("index"))
        except KeyError:
            pass
        message = "Invalid registration attempt"
    return render_template("register.html", message=message)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()

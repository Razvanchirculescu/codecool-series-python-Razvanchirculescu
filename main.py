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


@app.route('/simulation1')
def simulations():
    shows = queries.get_shows_from_1980s()
    return render_template('simulation1.html', shows=shows)


@app.route("/sim2")
def sim2():
    most_roles_played = queries.sim2()
    return render_template("sim2.html", most_roles_played=most_roles_played)


@app.route('/api/sim2/<actor_name>/')
def all_shows_actor_started(actor_name):
    shows = queries.sim2_by_actor_name(actor_name)
    return jsonify(shows)


@app.route('/sim3')
def sim3():
    all_genres = queries.sim3()
    return render_template('sim3.html', all_genres=all_genres)


@app.route('/api/sim3/<genres_name>/')
def sim4_top_rated_for_genre(genres_name):
    top_10_movies_for_genre = queries.sim3_top_rated_shows(genres_name)
    return jsonify(top_10_movies_for_genre)


@app.route('/sim4')
def sim4():
    runtime = queries.sim4_shortest_runtime()
    return render_template('sim4.html', runtime=runtime)


@app.route('/api/sim4/<show_genre>')
def sim4_show_genres(show_genre):
    show_genres = queries.sim4_show_genres(show_genre)
    return jsonify(show_genres)


@app.route('/sim5')
def sim5_10_latest_shows():
    ten_latest = queries.sim5_get_latest_10_shows()
    return render_template('sim5.html', ten_latest=ten_latest)


@app.route('/api/ten_latest/<show_id>')
def actors_in_ten_latest(show_id):
    actors_starring_in_ten_latest = queries.sim5_actors_starring_in_10_latest(show_id);
    return jsonify(actors_starring_in_ten_latest)


@app.route('/sim6')
def sim6_10_oldest_released_shows():
    oldest_shows = queries.sim6_first_10_released_shows()
    return render_template('sim6.html', oldest_shows=oldest_shows)


@app.route('/api/ten_oldest/<show_id>')
def sim6_seasons_and_episodes_count(show_id):
    seasons_and_episodes = queries.sim6_seasons_and_number_of_episodes_each(show_id)
    return jsonify(seasons_and_episodes)


@app.route('/sim7')
def sim7_all_action_shows():
    action_shows = queries.sim7_all_action_shows()
    return render_template('sim7.html', action_shows=action_shows)


@app.route('/api/runtime/<show_id>')
def sim7_runtime(show_id):
    runtime = queries.sim7movie_runtime(show_id)
    return jsonify(runtime)


@app.route('/sim8')
def sim8_actors_in_shows():
    actors = queries.sim8_all_action_shows()
    return render_template('sim8.html', actors=actors)


@app.route('/api/biography/<id>')
def sim8_actor_biography(id):
    biography = queries.sim8_biography(id)
    return jsonify(biography)


@app.route('/all_simulations/')
def all_simulations():
    return render_template('all_simulations.html')


@app.route('/sim9')
def sim9_all_genres_with_over_6_movies():
    genres_sim9 = queries.sim9_genres_with_over6shows()
    return render_template('sim9.html', genres_sim9=genres_sim9)


@app.route('/api/shows/<id>')
def sim9_shows_for_genre(id):
    shows_for_genre = queries.sim9_movies_for_genre(id)
    return jsonify(shows_for_genre)


@app.route('/PA')
def actors_in_musicals():
    actors_to_display = queries.pa_actors_in_musicals()
    return render_template('PA.html', actors_to_display=actors_to_display)


@app.route('/api/PA/<actor_id>')
def runtime_for_actor(actor_id):
    total_runtime = queries.pa_total_show_runtime_for_actor(actor_id)
    print(total_runtime)
    return jsonify(total_runtime)


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()


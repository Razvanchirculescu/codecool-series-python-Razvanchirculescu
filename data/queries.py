from data import data_manager


def get_shows():
    return data_manager.execute_select('SELECT id, title FROM shows;')


def get_most_rated_shows(offset):
    return data_manager.execute_select(
        """
        SELECT shows.id,
        shows.title,
        shows.year,
        shows.runtime,
        ROUND(shows.rating,1) AS rating_string,
        string_agg(genres.name,',' ORDER BY genres.name) AS genres_list,
        shows.trailer,
        shows.homepage
        FROM shows
        JOIN show_genres
        ON shows.id = show_genres.show_id
        JOIN genres
        ON show_genres.genre_id = genres.id
        GROUP BY shows.id
        ORDER BY rating_string DESC
        LIMIT 15
        OFFSET %(offset)s;""", {"offset": offset})


def get_show_by_id():
    return data_manager.execute_select(
        """
        SELECT shows.id,
        shows.title,
        shows.year,
        shows.runtime,
        ROUND(shows.rating,1) AS rating_string,
        string_agg(genres.name,',' ORDER BY genres.name) AS genres_list,
        shows.trailer,
        shows.homepage,
        shows.overview
        FROM shows
        JOIN show_genres
        ON shows.id= show_genres.show_id
        JOIN genres ON show_genres.genre_id = genres.id
        GROUP BY shows.id
        ORDER BY rating_string DESC;
        """)


def get_show_actors(_id_):
    return data_manager.execute_select(
        """
        SELECT a.name, a.birthday, a.death, a.biography
        FROM actors
        JOIN show_characters sc on actors.id = sc.actor_id
        JOIN actors a ON a.id = sc.actor_id
        WHERE show_id = %(id)s
        GROUP BY a.name, a.birthday, a.death, a.biography
        LIMIT 10;
    """, {"id": _id_})


def get_show_seasons(show_id):
    return data_manager.execute_select(
        """
            SELECT s.title, s.overview, s.season_number
            FROM shows
            JOIN seasons s on shows.id = s.show_id
            WHERE shows.id = %(show_id)s
            GROUP BY s.season_number, s.title, s.overview
        """, {'show_id': show_id})


def get_hundred_actors():
    return data_manager.execute_select(
        """
        SELECT * from actors
        ORDER BY birthday
        LIMIT 100
    """)


def get_shows_starred(id):
    return data_manager.execute_select(
        """
    SELECT DISTINCT shows.title AS title, a.name as name
    FROM shows
    INNER JOIN show_characters sc on shows.id = sc.show_id
    INNER JOIN actors a on a.id = sc.actor_id
    WHERE actor_id = %(id)s
    """, {'id': id})


def get_shows_from_1980s():
    return data_manager.execute_select(
        """
        SELECT s.id, s.title, ROUND (s.rating,2) as rating from shows s 
        WHERE EXTRACT(YEAR from s.year) BETWEEN '1980' AND '1990'
        ORDER BY s.rating DESC
        LIMIT 10
        """
    )


def add_user_to_database(username, password):
    return data_manager.execute_select(
        "INSERT INTO users (username, password) VALUES (%(username)s, %(password)s) RETURNING *;",
        {"username": username, "password": password},
    )


def get_all_users():
    return data_manager.execute_select("SELECT * FROM users;")


def valid_login(username):
    return data_manager.execute_select(
        "SELECT password FROM users WHERE username = %(username)s;",
        {"username": username},
    )


def sim2():
    return data_manager.execute_select(
        """
        SELECT COUNT(actor_id) as characters, a.name,string_agg(s.title, ',') as shows_played
        from show_characters sc
        INNER JOIN actors a on a.id = sc.actor_id
        INNER JOIN shows s on s.id = sc.show_id
        group by actor_id, a.name
        ORDER BY characters DESC 
        LIMIT 10
        """
    )


def sim2_by_actor_name(actor_name):
    return data_manager.execute_select("""
        SELECT title, a.id
        FROM shows 
        INNER JOIN show_characters sc on shows.id = sc.show_id
        INNER JOIN actors a on sc.actor_id = a.id
        WHERE a.name =%(actor_name)s
    """, {"actor_name": actor_name})


def sim3():
    return data_manager.execute_select("""
    SELECT * from genres
    """)


def sim3_top_rated_shows(genres_name):
    return data_manager.execute_select("""
    SELECT distinct s.title,
    ROUND(s.rating, 2) AS rating_str, g.name
    FROM shows s
    INNER JOIN show_genres sg on s.id = sg.show_id
    INNER JOIN genres g on g.id = sg.genre_id
    WHERE g.id=%(genres_name)s
    ORDER BY rating_str DESC
    LIMIT 10
  
    """, {"genres_name": genres_name})


def sim4_shortest_runtime():
    return data_manager.execute_select("""
    SELECT title, runtime,id
    from shows
    order by runtime ASC
    LIMIT 30
    """)


def sim4_show_genres(show_genre):
    return data_manager.execute_select("""
    SELECT g.name, g.id
    FROM genres g
    INNER JOIN show_genres sg on g.id = sg.genre_id
    WHERE sg.show_id=%(show_genre)s
    """, {"show_genre": show_genre})


def sim5_get_latest_10_shows():
    return data_manager.execute_select("""
    SELECT s.title, s.year as released, s.id as show_id
    FROM shows s
    GROUP BY s.year, s.title, s.id
    ORDER BY s.year DESC
    LIMIT 10
    """)


def sim5_actors_starring_in_10_latest(show_id):
    return data_manager.execute_select("""
    SELECT a.id, a.name, sc.show_id
    FROM shows s
    INNER JOIN show_characters sc on s.id = sc.show_id
    INNER JOIN actors a on a.id = sc.actor_id
    WHERE show_id=%(show_id)s
    """, {"show_id": show_id})


def sim6_first_10_released_shows():
    return data_manager.execute_select("""
    SELECT s.title, s.year, s.id 
    FROM shows s 
    GROUP BY s.title, s.year, s.id
    ORDER BY s.year 
    LIMIT 10
    """)


def sim6_seasons_and_number_of_episodes_each(show_id):
    return data_manager.execute_select("""
    SELECT ss.title as season_title, COUNT(e.episode_number)
    FROM seasons ss
    INNER JOIN episodes e on ss.id = e.season_id
    inner join shows s on s.id = ss.show_id
    WHERE s.id =%(show_id)s
    GROUP BY ss.title 
    """, {"show_id": show_id})


def sim7_all_action_shows():
    return data_manager.execute_select("""
    SELECT DISTINCT s.title, g.name, COUNT(a.id) as no_of_actors,
    string_agg(a.name,',' ORDER BY a.name) AS actors, s.id
    FROM shows s
    INNER JOIN show_characters sc on s.id = sc.show_id
    INNER JOIN actors a on a.id = sc.actor_id
    inner join show_genres sg on s.id = sg.show_id
    INNER JOIN genres g on g.id = sg.genre_id
    WHERE EXTRACT(YEAR FROM age(current_date, birthday)) > 20 AND g.name = 'Action' 
    GROUP BY s.title, g.name, s.id
    HAVING COUNT(a.id) >5
    """)


def sim7movie_runtime(show_id):
    return data_manager.execute_select("""
    SELECT s.runtime
    FROM shows s
    WHERE id=%(show_id)s
    """, {"show_id": show_id})


def sim8_all_action_shows():
    return data_manager.execute_select("""
    SELECT a.name, a.death, a.id
    FROM actors a
    INNER JOIN show_characters sc on a.id = sc.actor_id
    INNER JOIN shows s on s.id = sc.show_id
    WHERE a.death IS NOT NULL
    Group by a.death,a.name, a.id
    HAVING avg(s.rating) > 9.3
    """)


def sim8_biography(id):
    return data_manager.execute_select("""
    SELECT biography
    FROM actors
    WHERE id=%(id)s
    """, {'id': id})


def sim9_genres_with_over6shows():
    return data_manager.execute_select("""
    SELECT g.name, COUNT(sg.genre_id), sg.genre_id
    FROM genres g
    INNER JOIN show_genres sg on g.id = sg.genre_id
    INNER JOIN shows s on s.id = sg.show_id
    GROUP BY g.name, sg.genre_id
    HAVING COUNT(sg.show_id) > 6
    """)


def sim9_movies_for_genre(id):
    return data_manager.execute_select("""
        SELECT s.title
        FROM shows s
        INNER JOIN show_genres sg on s.id = sg.show_id
        WHERE sg.genre_id= %(id)s
    """, {'id': id})


def pa_actors_in_musicals():
    return data_manager.execute_select("""
    SELECT a.name, a.id
    FROM actors a 
    INNER JOIN show_characters sc on a.id = sc.actor_id
    INNER JOIN shows s on s.id = sc.show_id
    INNER JOIN show_genres sg on s.id = sg.show_id
    INNER JOIN genres g on g.id = sg.genre_id
    WHERE g.name = 'Musical'
    """)


def pa_total_show_runtime_for_actor(actor_id):
    return data_manager.execute_select("""
    SELECT SUM(s.runtime) as total_runtime
    FROM shows s
    INNER JOIN show_characters sc on s.id = sc.show_id
    INNER JOIN seasons s2 on s.id = s2.show_id
    WHERE sc.actor_id=%(actor_id)s
    """, {'actor_id': actor_id})












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

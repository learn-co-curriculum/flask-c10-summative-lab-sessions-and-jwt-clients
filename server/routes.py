from flask import request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
)

from extensions import db
from models import User, Movie


def register_routes(app):

    # Sign up
    @app.post("/signup")
    def signup():
        data = request.get_json()

        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400

        username = data.get("username")
        password = data.get("password")
        password_confirmation = data.get("password_confirmation")

        if not username or not password or not password_confirmation:
            return jsonify({
                "error": "Username, password and password_confirmation are required"
            }), 400

        if password != password_confirmation:
            return jsonify({"error": "Passwords do not match"}), 400

        if User.query.filter_by(username=username).first():
            return jsonify({"error": "Username already exists"}), 400

        try:
            user = User(username=username)
            user.password_hash = password

            db.session.add(user)
            db.session.commit()

            token = create_access_token(identity=str(user.id))

            return jsonify({
                "token": token,
                "user": user.to_dict()
            }), 201

        except ValueError as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400

    # Login
    @app.post("/login")
    def login():
        data = request.get_json()

        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400

        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({
                "error": "Username and password are required"
            }), 400

        user = User.query.filter_by(username=username).first()

        if user is None or not user.authenticate(password):
            return jsonify({
                "error": "Invalid username or password"
            }), 401

        token = create_access_token(identity=str(user.id))

        return jsonify({
            "token": token,
            "user": user.to_dict()
        }), 200

    # Current user
    @app.get("/me")
    @jwt_required()
    def me():

        user_id = int(get_jwt_identity())

        user = db.session.get(User, user_id)

        if user is None:
            return jsonify({"error": "User not found"}), 404

        return jsonify(user.to_dict()), 200

    # Create Movie
    @app.post("/movies")
    @jwt_required()
    def create_movie():

        user_id = int(get_jwt_identity())

        data = request.get_json()

        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400

        title = data.get("title")
        genre = data.get("genre")
        director = data.get("director")
        release_year = data.get("release_year")
        rating = data.get("rating")

        if not title or not genre or not director or release_year is None:
            return jsonify({
                "error": "title, genre, director and release_year are required"
            }), 400

        try:
            movie = Movie(
                title=title,
                genre=genre,
                director=director,
                release_year=release_year,
                rating=rating,
                user_id=user_id
            )

            db.session.add(movie)
            db.session.commit()

            return jsonify(movie.to_dict()), 201

        except ValueError as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400


    # Get all Movies
    @app.get("/movies")
    @jwt_required()
    def get_movies():

        user_id = int(get_jwt_identity())

        page = request.args.get("page", default=1, type=int)
        per_page = request.args.get("per_page", default=5, type=int)

        pagination = (
            Movie.query
            .filter_by(user_id=user_id)
            .paginate(page=page, per_page=per_page, error_out=False)
        )

        return jsonify({
            "movies": [movie.to_dict() for movie in pagination.items],
            "page": pagination.page,
            "pages": pagination.pages,
            "total": pagination.total,
            "per_page": pagination.per_page
        }), 200

    # Get a Movie
    @app.get("/movies/<int:movie_id>")
    @jwt_required()
    def get_movie(movie_id):

        user_id = int(get_jwt_identity())

        movie = Movie.query.filter_by(
            id=movie_id,
            user_id=user_id
        ).first()

        if movie is None:
            return jsonify({"error": "Movie not found"}), 404

        return jsonify(movie.to_dict()), 200

    # Update Movie
    @app.patch("/movies/<int:movie_id>")
    @jwt_required()
    def update_movie(movie_id):

        user_id = int(get_jwt_identity())

        movie = Movie.query.filter_by(
            id=movie_id,
            user_id=user_id
        ).first()

        if movie is None:
            return jsonify({"error": "Movie not found"}), 404

        data = request.get_json()

        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400

        try:
            if "title" in data:
                movie.title = data["title"]

            if "genre" in data:
                movie.genre = data["genre"]

            if "director" in data:
                movie.director = data["director"]

            if "release_year" in data:
                movie.release_year = data["release_year"]

            if "rating" in data:
                movie.rating = data["rating"]

            db.session.commit()

            return jsonify(movie.to_dict()), 200

        except ValueError as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400

    # Delete Movie
    @app.delete("/movies/<int:movie_id>")
    @jwt_required()
    def delete_movie(movie_id):

        user_id = int(get_jwt_identity())

        movie = Movie.query.filter_by(
            id=movie_id,
            user_id=user_id
        ).first()

        if movie is None:
            return jsonify({"error": "Movie not found"}), 404

        db.session.delete(movie)
        db.session.commit()

        return "", 204
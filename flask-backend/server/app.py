from flask import Flask, request, jsonify, session
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from models import db, Expense
from auth import auth_bp

# initialize app
app = Flask(__name__)

#app configurations
app.config["SECRET_KEY"] = "super-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#initialize extensions
db.init_app(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)

#register auth blueprint
app.register_blueprint(auth_bp)

#create expense routes
#index route
@app.route("/")
def home():
    return jsonify({"message": "Expense Tracker API Running"})

# Get all expenses -> ensure pagination
@app.route("/expenses", methods=["GET"])
def get_expenses():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized access.Kindly log in to continue..."}), 401

    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))

    query = Expense.query.filter_by(user_id=user_id)
    paginated = query.paginate(page=page, per_page=per_page, error_out=False)

    expenses = [e.to_dict() for e in paginated.items]

    return jsonify({
        "data": expenses,
        "page": page,
        "total_pages": paginated.pages
    }), 200


# Create an expense -> POST
@app.route("/expenses", methods=["POST"])
def create_expense():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized access.Kindly log in to continue..."}), 401

    data = request.get_json()
    if not data.get("title") or not data.get("amount"):
        return jsonify({"error": "Missing required fields"}), 400

    expense = Expense(
        title=data["title"],
        amount=data["amount"],
        category=data.get("category"),
        description=data.get("description"),
        user_id=user_id
    )

    #add and save to db
    db.session.add(expense)
    db.session.commit()

    return jsonify({"message": "Expense created successfully!"}), 201


# Update an expense -> PATCH
@app.route("/expenses/<int:id>", methods=["PATCH"])
def update_expense(id):
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized access.Kindly log in to continue..."}), 401

    expense = Expense.query.get(id)
    if not expense:
        return jsonify({"error": "Expense not found"}), 404

    if expense.user_id != user_id:
        return jsonify({"error": "Forbidden"}), 403

    data = request.get_json()

    expense.title = data.get("title", expense.title)
    expense.amount = data.get("amount", expense.amount)
    expense.category = data.get("category", expense.category)
    expense.description = data.get("description", expense.description)

    db.session.commit()

    return jsonify({"message": f"Expense with id {id} updated successfully"}), 200


# Delete an expense ->DELETE
@app.route("/expenses/<int:id>", methods=["DELETE"])
def delete_expense(id):
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized access.Kindly log in to continue..."}), 401

    expense = Expense.query.get(id)

    if not expense:
        return jsonify({"error": "Expense not found"}), 404

    if expense.user_id != user_id:
        return jsonify({"error": "Forbidden"}), 403

    db.session.delete(expense)
    db.session.commit()

    return jsonify({"message": f"Expense with id {id} deleted successfully!"}), 200


if __name__ == "__main__":
    app.run(debug=True, port=3000)
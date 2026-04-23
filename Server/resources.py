from flask import session, request, jsonify
from flask_restful import Resource
from models import db, User, Expense
from schemas import user_schema, expense_schema, expenses_schema
from app import bcrypt

class Register(Resource):
    def post(self):
        data = request.get_json()
        try:
            if User.query.filter_by(username=data['username']).first():
                return {"error": "Username already exists"}, 400
            password_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            user = User(username=data['username'], password_hash=password_hash)
            db.session.add(user)
            db.session.commit()
            session['user_id'] = user.id
            return user_schema.dump(user), 201
        except Exception as e:
            return {"error": str(e)}, 400
        
class Login(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username = data['username']).first()
        if not user or not bcrypt.check_password_hash(user.password_hash, data['password']):
            return {"error": "Invalid username or password"}, 401
        session['user_id'] = user.id
        return user_schema.dump(user), 200
    
class Logout(Resource):
    def delete(self):
        session.pop('user_id', None)
        return {}, 204
    
class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')
        if not user_id:
            return {}, 200
        user = User.query.get(user_id)
        if not user:
            return{}, 200
        return user_schema.dump(user), 200
    
class ExpenseList(Resource):
    def get (self):
        user_id = session.get('user_id')
        if not user_id:
            return{"error": "Not logged in"}, 401
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)
        expenses = Expense.query.filter_by(user_id = user_id).paginate(page=page, per_page=per_page, error_out=False)
        return {
            "expenses": expenses_schema.dump(expenses.items),
            "total": expenses.total,
            "pages": expenses.pages,
            "current_page": expenses.page
        }, 200
        
    def post(self):
        user_id = session.get('user_id')
        if not user_id:
            return {"error": "Not logged in"}, 401
        data = request.get_json()
        try:
            validated_data = expense_schema.load(data)
            expense = Expense(**validated_data, user_id = user_id)
            db.session.add(expense)
            db.session.commit()
            return expense_schema.dump(expense), 201
        except Exception as e:
            return {"error": str(e)}, 400
        
class ExpenseDetail(Resource):
    def get_expense_or_403(self, id):
        user_id = session.get('user_id')
        if not user_id:
            return None, {"error": "Not logged in"}, 401
        expense = Expense.query.get(id)
        if not expense:
            return None, {"error": "Expense not found"}, 404
        if expense.user_id != user_id:
            return None, {"error": "Unauthorised"}, 403
        return expense, None, None
    
    def patch(self, id):
        expense, error, status = self.get_expense_or_403(id)
        if error:
            return error, status
        data = request.get_json()
        try:
            for key, value in data.items():
                setattr(expense, key, value)
            db.session.commit()
            return expense_schema.dump(expense), 200
        except Exception as e:
            return {'error': str(e)}, 400

    def delete(self, id):
        expense, error, status = self.get_expense_or_403(id)
        if error:
            return error, status
        db.session.delete(expense)
        db.session.commit()
        return {}, 204
    
    
def register_routes(api):
    api.add_resource(Register, '/signup')
    api.add_resource(Login, '/login')
    api.add_resource(Logout, '/logout')
    api.add_resource(CheckSession, '/check_session')
    api.add_resource(ExpenseList, '/expenses')
    api.add_resource(ExpenseDetail, '/expenses/<int:id>')
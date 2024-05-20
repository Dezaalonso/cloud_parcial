from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, inspect
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS for the entire app, allowing requests from any origin
CORS(app, resources={r"/*": {"origins": "*"}})

# Configuration for multiple databases
app.config['SQLALCHEMY_BINDS'] = {
    'db_user': 'mysql://admin:Cloud998134@cloudpp1.cv478kobasse.us-east-1.rds.amazonaws.com/user_db',
    'db_bank': 'mysql://admin:Cloud998134@cloudpp1.cv478kobasse.us-east-1.rds.amazonaws.com/bank_db'
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "somethingunique"

db = SQLAlchemy(app)

# Define models, binding each to its respective database
class User(db.Model):
    __bind_key__ = 'db_user'
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    age = db.Column(db.Integer)

class Bank(db.Model):
    __bind_key__ = 'db_bank'
    __tablename__ = 'bank'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    money = db.Column(db.Integer)  # Changed from Numeric to Integer


def table_exists(engine, table_name):
    inspector = inspect(engine)
    return inspector.has_table(table_name)

with app.app_context():
    engines = {
        'db_user': db.get_engine(bind='db_user'),
        'db_bank': db.get_engine(bind='db_bank'),
    }
    
    # Check and create tables for each bind
    for bind_key, engine in engines.items():
        metadata = MetaData()
        metadata.reflect(bind=engine)
        if not table_exists(engine, 'user') and bind_key == 'db_user':
            User.__table__.create(bind=engine)
        if not table_exists(engine, 'bank') and bind_key == 'db_bank':
            Bank.__table__.create(bind=engine)


@app.route('/bank/<int:user_id>', methods=['POST'])
def create_bank_account(user_id):
    money = request.json.get('money')
    
    # Check if the user exists
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Create a new bank account for the user
    new_bank_account = Bank(user_id=user.id, money=int(money))  # Convert money to integer
    db.session.add(new_bank_account)
    db.session.commit()

    return jsonify({'message': 'Bank account created successfully', 'bank_id': new_bank_account.id}), 201

@app.route('/bank', methods=['GET'])
def get_all_bank_accounts():
    # Retrieve all bank accounts
    all_bank_accounts = Bank.query.all()
    
    # Prepare the response with bank account information
    if all_bank_accounts:
        bank_info = [{'bank_id': account.id, 'user_id': account.user_id, 'money': account.money} for account in all_bank_accounts]
        return jsonify(bank_info), 200
    else:
        return jsonify({'message': 'No bank accounts found'}), 404

@app.route('/bank/<int:user_id>', methods=['GET'])
def get_bank_account(user_id):
    # Check if the user exists
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Retrieve bank accounts for the user
    bank_accounts = Bank.query.filter_by(user_id=user.id).all()
    if not bank_accounts:
        return jsonify({'message': 'No bank accounts found for this user'}), 404
    
    # Prepare the response with bank account information
    bank_info = [{'bank_id': account.id, 'money': account.money} for account in bank_accounts]
    return jsonify(bank_info), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

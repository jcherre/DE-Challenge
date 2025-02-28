from os import environ
import sqlalchemy
from flask import Flask, request, jsonify
#from dotenv import load_dotenv
from db import connect_with_connector
from utils import *

#load_dotenv('cloud/.env')
app = Flask(__name__)

API_TOKEN = environ.get('API_TOKEN')

def token_required(f):
    def decorator(*args, **kwargs):
        token = request.headers.get("Authorization")
        if token != f"Bearer {API_TOKEN}":
            return jsonify({"message": "Unauthorized access"}), 403
        return f(*args, **kwargs)
    return decorator

@app.route('/upload_csv', endpoint='func1', methods=['POST'])
@token_required
def upload_csv():
    csv_file = request.files.get('file')
    table_name = request.form.get('table')

    if not csv_file or not table_name:
        return jsonify({'error': 'No file or table name provided'}), 400
    
    try:
        #Get engine
        engine = connect_with_connector(environ)
        #Get session
        session = get_session(engine)
        
        if table_name == 'departments':
            table_class = Department
        elif table_name == 'jobs':
            table_class = Job
        elif table_name == 'employees':
            table_class = Employee
        else:
            return jsonify({'error': 'Invalid table name'}), 400
        
        result = process_csv(csv_file, table_class, session)

        if result is True:
            return jsonify({'message': f'Data successfully uploaded to {table_name} table'}), 200
        else:
            return jsonify({'error': result}), 500
    except Exception as e:
        session.rollback()  # Rollback the transaction if there's an error
        print(f'Error occurred: {e}')
    finally:
        session.close()  # Ensure the session is closed
    
@app.route('/batch_insert', endpoint='func2', methods=['POST'])
@token_required
def batch_insert():
    data = request.get_json()

    table_name = data.get('table')
    rows = data.get('rows')

    if not table_name or not rows or len(rows) > 1000:
        return jsonify({'error': 'Invalid input data or row count exceeds 1000'}), 400

    try:
        #Get engine
        engine = connect_with_connector(environ)
        #Get session
        session = get_session(engine)
        
        if table_name == 'departments':
            table_class = Department
        elif table_name == 'jobs':
            table_class = Job
        elif table_name == 'employees':
            table_class = Employee
        else:
            return jsonify({'error': 'Invalid table name'}), 400
        
        result = process_batch(rows, table_class, session)

        if result is True:
            return jsonify({'message': f'Data successfully uploaded to {table_name} table'}), 200
        else:
            return jsonify({'error': result}), 500
    except Exception as e:
        session.rollback()  # Rollback the transaction if there's an error
        print(f'Error occurred: {e}')
    finally:
        session.close()  # Ensure the session is closed

@app.route('/employees_by_quarter', endpoint='func3', methods=['GET'])
@token_required
def employees_by_quarter():
    try:
        #Get engine
        engine = connect_with_connector(environ)
        #Get session
        session = get_session(engine)
        
        file = open('cloud/queries/count_quarter.sql')
        year = '2021'
        stmt = sqlalchemy.text(file.read().replace("{year}",year))

        result = session.execute(stmt)

        return jsonify({'message': f'Data from employees was loaded succesfully',
                        'data':[row._asdict() for row in result]}), 200
    except Exception as e:
        print(e)
        return f'Error occurred: {e}', 500
    finally:
        session.close()  # Ensure the session is closed
    
@app.route('/employees_hired', endpoint='func4', methods=['GET'])
@token_required
def employees_hired():
    try:
        #Get engine
        engine = connect_with_connector(environ)
        #Get session
        session = get_session(engine)
        
        file = open('cloud/queries/employees_hired.sql')
        year = '2021'
        stmt = sqlalchemy.text(file.read().replace("{year}",year))
        
        result = session.execute(stmt)

        return jsonify({'message': f'Data from employees was loaded succesfully',
                        'data':[row._asdict() for row in result]}), 200
    except Exception as e:
        return f'Error occurred: {e}', 500
    finally:
        session.close()  # Ensure the session is closed

@app.route('/data', endpoint='funcx', methods=['GET'])
@token_required
def get_data():
    # Your logic to retrieve and return data
    return jsonify({"data": "some protected data"})

@app.route('/')
def health_check():
    return 'API online!', 200

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)

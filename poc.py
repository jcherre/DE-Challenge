import os
import pandas as pd
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///local.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Departments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(100), nullable=False)

class Jobs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job = db.Column(db.String(100), nullable=False)

class Employees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    datetime = db.Column(db.String(100), nullable=True)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    department = db.relationship('Departments', backref=db.backref('employees', lazy=True))
    job = db.relationship('Jobs', backref=db.backref('employees', lazy=True))

# Create tables
with app.app_context():
    db.create_all()


def process_data(csv_file, table_class):
    try:
        if table_class == Departments:
            column_names = ['id', 'department']
        elif table_class == Jobs:
            column_names = ['id', 'job']
        elif table_class == Employees:
            column_names = ['id', 'name', 'datetime', 'department_id', 'job_id']
        
        df = pd.read_csv(csv_file, header=None, names=column_names)

        if table_class == Employees:
            df= df.dropna(subset=['name', 'department_id', 'job_id'])

        db_objects = []

        for index, row in df.iterrows():
            if table_class == Departments:
                db_objects.append(Departments(department=row['department']))
            elif table_class == Jobs:
                db_objects.append(Jobs(job=row['job']))
            elif table_class == Employees:
                db_objects.append(Employees(name=row['name'], datetime=row['datetime'], department_id=row['department_id'], job_id=row['job_id']))
        
        db.session.bulk_save_objects(db_objects)
        db.session.commit()

        return True
    except Exception as e:
        db.session.rollback()
        return f"Error processing data: {str(e)}"

@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    csv_file = request.files.get('file')
    table_name = request.form.get('table')

    if not csv_file or not table_name:
        return jsonify({'error': 'No file or table name provided'}), 400

    if table_name == 'departments':
        table_class = Departments
    elif table_name == 'jobs':
        table_class = Jobs
    elif table_name == 'employees':
        table_class = Employees
    else:
        return jsonify({'error': 'Invalid table name'}), 400

    file_path = os.path.join('uploads', csv_file.filename)
    csv_file.save(file_path)

    result = process_data(file_path, table_class)

    os.remove(file_path)

    if result is True:
        return jsonify({'message': f'Data successfully uploaded to {table_name} table'}), 200
    else:
        return jsonify({'error': result}), 500

@app.route('/batch_insert', methods=['POST'])
def batch_insert():
    data = request.get_json()

    table_name = data.get('table')
    rows = data.get('rows')

    if not table_name or not rows or len(rows) > 1000:
        return jsonify({'error': 'Invalid input data or row count exceeds 1000'}), 400

    if table_name == 'departments':
        table_class = Departments
    elif table_name == 'jobs':
        table_class = Jobs
    elif table_name == 'employees':
        table_class = Employees
    else:
        return jsonify({'error': 'Invalid table name'}), 400

    try:
        db_objects = []
        for row in rows:
            if table_class == Departments:
                db_objects.append(Departments(department=row['department']))
            elif table_class == Jobs:
                db_objects.append(Jobs(job=row['job']))
            elif table_class == Employees:
                db_objects.append(Employees(name=row['name'], datetime=row['datetime'], department_id=row['department_id'], job_id=row['job_id']))

        db.session.bulk_save_objects(db_objects)
        db.session.commit()

        return jsonify({'message': f'{len(rows)} rows successfully inserted into {table_name} table'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)

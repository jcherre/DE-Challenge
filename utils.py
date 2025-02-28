from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship, backref, sessionmaker
import pandas as pd
import math

class Base(DeclarativeBase):
    pass

class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True)
    department = Column(String(100), nullable=False)

class Job(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True)
    job = Column(String(100), nullable=False)

class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    datetime = Column(String(100), nullable=True)
    department_id = Column(Integer, ForeignKey('departments.id'), nullable=False)
    job_id = Column(Integer, ForeignKey('jobs.id'), nullable=False)
    department = relationship('Department', backref=backref('employees', lazy=True))
    job = relationship('Job', backref=backref('employees', lazy=True))

def get_session(engine):
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

def process_csv(csv_file, table_class, session):
    try:
        if table_class == Department:
            column_names = ['id', 'department']
        elif table_class == Job:
            column_names = ['id', 'job']
        elif table_class == Employee:
            column_names = ['id', 'name', 'datetime', 'department_id', 'job_id']
        
        df = pd.read_csv(csv_file, header=None, names=column_names)

        db_objects = []

        nans = 0

        for index, row in df.iterrows():
            if table_class == Department:
                if math.isnan(row['id']):
                    nans += 1
                else:
                    db_objects.append(Department(id=row['id'], department=row['department']))
            elif table_class == Job:
                if math.isnan(row['id']):
                    nans += 1
                else:
                    db_objects.append(Job(id=row['id'], job=row['job']))
            elif table_class == Employee:
                if math.isnan(row['id']) or math.isnan(row['department_id']) or math.isnan(row['job_id']):
                    nans += 1
                else:
                    db_objects.append(Employee(id=row['id'], name=row['name'], datetime=str(row['datetime']), department_id=int(row['department_id']), job_id=int(row['job_id'])))
        
        if nans > 0:
            print("There are "+str(nans)+" row(s) with null id values which won't be inserted")
        session.add_all(db_objects)
        session.commit()

        return True
    except Exception as e:
        session.rollback()
        return f"Error processing data: {str(e)}"
    
def process_batch(rows, table_class, session):
    try:
        db_objects = []
        nans = 0
        for row in rows:
            if table_class == Department:
                if math.isnan(row['id']):
                    nans += 1
                else:
                    db_objects.append(Department(id=row['id'], department=row['department']))
            elif table_class == Job:
                if math.isnan(row['id']):
                    nans += 1
                else:
                    db_objects.append(Job(id=row['id'], job=row['job']))
            elif table_class == Employee:
                if math.isnan(row['id']) or math.isnan(row['department_id']) or math.isnan(row['job_id']):
                    nans += 1
                else:
                    db_objects.append(Employee(id=row['id'], name=row['name'], datetime=str(row['datetime']), department_id=int(row['department_id']), job_id=int(row['job_id'])))
        
        if nans > 0:
            print("There are "+str(nans)+" row(s) with null id values which won't be inserted")
        session.add_all(db_objects)
        session.commit()

        return True
    except Exception as e:
        session.rollback()
        return f"Error processing data: {str(e)}"
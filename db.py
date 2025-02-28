from google.cloud.sql.connector import Connector, IPTypes
import pg8000
import sqlalchemy

def connect_with_connector(env_connection_sql) -> sqlalchemy.engine.base.Engine:
    """
    Initializes a connection pool for a Cloud SQL instance of Postgres.

    Uses the Cloud SQL Python Connector package.
    """
    # Note: Saving credentials in environment variables is convenient, but not
    # secure - consider a more secure solution such as
    # Cloud Secret Manager (https://cloud.google.com/secret-manager) to help
    # keep secrets safe.

    instance_name = ':'.join([env_connection_sql.get('PROJECT_ID'),env_connection_sql.get('REGION'),env_connection_sql.get('INSTANCE')])

    # Define connection parameters for PostgreSQL
    INSTANCE_CONNECTION_NAME = instance_name
    DB_USER = env_connection_sql.get('DB_USER')
    DB_PASS = env_connection_sql.get('DB_PASS')
    DB_NAME = env_connection_sql.get('DB_NAME')

    ip_type = IPTypes.PRIVATE #IPTypes.PUBLIC

    # initialize Cloud SQL Python Connector object
    connector = Connector(refresh_strategy="LAZY")

    def getconn() -> pg8000.dbapi.Connection:
        conn: pg8000.dbapi.Connection = connector.connect(
            INSTANCE_CONNECTION_NAME,
            "pg8000",
            user=DB_USER,
            password=DB_PASS,
            db=DB_NAME,
            ip_type=ip_type,
        )
        return conn

    # The Cloud SQL Python Connector can be used with SQLAlchemy
    # using the 'creator' argument to 'create_engine'
    pool = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=getconn,
        pool_size=5,
        max_overflow=2,
        pool_timeout=30,
        pool_recycle=1800
    )
    return pool


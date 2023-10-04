from secret_manager import get_secret

DATABASE_URI = "sqlite:///omdb.db"
OMDB_API_URL = 'https://www.omdbapi.com/'
OMDB_API_KEY = 'cc7855c5'
GCP_PROJECT_NO = 945031540661   # GCP project number or id
SQL_HOST = '<host_ip or hostname>'  # host server ip or hostname
SQL_PASSWORD_SECRET_ID = 'MYSQL_DB_PASSWORD'
SQL_USERNAME_SECRET_ID = 'MYSQL_DB_USERNAME'
SQL_DB_NAME_SECRET_ID = 'MYSQL_DB_NAME'
SQL_USERNAME = get_secret(GCP_PROJECT_NO, SQL_USERNAME_SECRET_ID)
SQL_DB_NAME = get_secret(GCP_PROJECT_NO, SQL_DB_NAME_SECRET_ID)
DATABASE_URI = f"mysql+pymysql://{SQL_USERNAME}:{get_secret(GCP_PROJECT_NO, SQL_PASSWORD_SECRET_ID)}@{SQL_HOST}/{SQL_DB_NAME}"

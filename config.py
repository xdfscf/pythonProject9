WTF_CSRF_ENABLED = True
import os
# You should change this
'''
db_user = "root"
db_pass = "Q13579qscesz"
db_name = "musicdb"
db_host = "127.0.0.1:3307"

# Extract port from db_host if present,
# otherwise use DB_PORT environment variable.
host_args = db_host.split(":")
if len(host_args) == 1:
    db_hostname = db_host
    db_port = os.environ["DB_PORT"]
elif len(host_args) == 2:
    db_hostname, db_port = host_args[0], int(host_args[1])

pool = sqlalchemy.create_engine(
    # Equivalent URL:
    # mysql+pymysql://<db_user>:<db_pass>@<db_host>:<db_port>/<db_name>
    sqlalchemy.engine.url.URL.create(
        drivername="mysql+pymysql",
        username=db_user,  # e.g. "my-database-user"
        password=db_pass,  # e.g. "my-database-password"
        host=db_hostname,  # e.g. "127.0.0.1"
        port=db_port,  # e.g. 3306
        database=db_name,  # e.g. "my-database-name"
    ),

)
basedir = os.path.abspath(os.path.dirname(__file__))


SECRET_KEY = 'hard to guess'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Q13579qscesz@127.0.0.1:3307/musicdb'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
'''
basedir = os.path.abspath(os.path.dirname(__file__))


SECRET_KEY = 'hard to guess'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Q13579qscesz@127.0.0.1:3306/bookstore_db1'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')


#exts.py
#py_exts.vm make Basic flask app templete
import os
from sqlalchemy import MetaData  # Used to define metadata for the database model
from flask import Flask  # Import the Flask framework
from flask_sqlalchemy import SQLAlchemy  # Import the Flask-SQLAlchemy extension for database operations
from flask_babel import Babel  # Import the Flask-Babel extension for internationalization and localization
from flask_migrate import Migrate  # Import the Flask-Migrate extension for database migrations
from flask_mail import Mail  # Import the Flask-Mail extension for sending emails
from flask_cors import CORS
from flask_session import Session
# Create and configure the Flask application
app = Flask(__name__, instance_relative_config=True)
# SECRET_KEY: must be set via env; startup validation in config.validate_startup_config() will exit if missing
app.secret_key = os.environ.get("SECRET_KEY") or ""
# Server-side session: store session data on filesystem (avoids signed-cookie size limit for large session payloads)
_session_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "instance", "flask_session")
os.makedirs(_session_dir, exist_ok=True)
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = _session_dir
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True
app.config["SESSION_KEY_PREFIX"] = "app:"
app.config["SESSION_COOKIE_NAME"] = "app_session"
Session(app)
# CORS: restrict CORS_ORIGINS in production (e.g. https://yourdomain.com)
_cors_origins = [x.strip() for x in (os.getenv("CORS_ORIGINS") or "*").split(",") if x.strip()]
_cors_methods = [x.strip() for x in (os.getenv("CORS_METHODS") or "GET,POST,PUT,DELETE,OPTIONS").split(",") if x.strip()]
_cors_allow_headers = [x.strip() for x in (os.getenv("CORS_ALLOW_HEADERS") or "Content-Type,Authorization").split(",") if x.strip()]
CORS(app, origins=_cors_origins, methods=_cors_methods, allow_headers=_cors_allow_headers)
# Initialize the Flask-Migrate extension
migrate = Migrate()

# Initialize the Flask-Mail extension
mail = Mail()

# Initialize the Flask-Babel extension
babel = Babel()

# Create a MetaData object with naming conventions for SQLAlchemy
convention = {
    # "ix": Represents an index and is a naming convention that includes the column label.
    "ix": "ix_%(column_0_label)s",
    # "uq": Represents a unique constraint and is a naming convention that includes the table name and column name.
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    # "ck": Represents a check constraint and is a naming convention that includes the table name and constraint name.
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    # "fk": Represents a foreign key and is a naming convention that includes the table name, column name, and referred table name.
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    # "pk": Represents a primary key and is a naming convention that includes the table name.
    "pk": "pk_%(table_name)s",
}

# Create the SQLAlchemy database object and apply the above naming conventions
metadata = MetaData(naming_convention=convention)
# ORM
db = SQLAlchemy(metadata=metadata)

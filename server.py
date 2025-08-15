from flask import Flask
from flask_wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from os import environ
from pathlib import Path

# Global extensions (initialized without app, bound in create_app)
csrf = CSRFProtect()
db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()


def _default_database_uri() -> str:
	data_dir = Path(__file__).parent / "data"
	data_dir.mkdir(exist_ok=True)
	return f"sqlite:///{(data_dir / 'app.db').as_posix()}"


def create_app() -> Flask:
	app = Flask(__name__, static_folder="src/static", template_folder="src/templates")

	# Basic config
	app.config.update(
		SECRET_KEY=environ.get("SECRET_KEY", "dev-secret-change-me"),
		SQLALCHEMY_DATABASE_URI=environ.get("DATABASE_URL", _default_database_uri()),
		SQLALCHEMY_TRACK_MODIFICATIONS=False,
		WTF_CSRF_TIME_LIMIT=None,
	)

	# Init extensions
	csrf.init_app(app)
	db.init_app(app)
	login_manager.init_app(app)
	login_manager.login_view = "admin.login"
	bcrypt.init_app(app)

	# Models must be imported after db is created
	from src.models.entities import AdminUser, get_or_create_admin  # noqa: F401

	@login_manager.user_loader
	def load_user(user_id: str):
		try:
			return AdminUser.query.get(int(user_id))
		except Exception:
			return None

	# Blueprints
	from src.controllers.routes import public_bp, admin_bp
	app.register_blueprint(public_bp)
	app.register_blueprint(admin_bp, url_prefix="/admin")

	# Create DB on first run (MVP convenience) and seed admin
	with app.app_context():
		db.create_all()
		admin_username = environ.get("ADMIN_USERNAME", "admin")
		admin_password = environ.get("ADMIN_PASSWORD", "change-me")
		try:
			get_or_create_admin(admin_username, admin_password)
		except Exception:
			pass

	@app.context_processor
	def inject_globals():
		from datetime import datetime as _dt
		return {"current_year": _dt.utcnow().year}

	return app


# For WSGI servers
app = create_app()


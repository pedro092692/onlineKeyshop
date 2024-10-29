from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean, ForeignKey, DateTime
from typing import List
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from sqlalchemy import exists
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from turbo_flask import Turbo
from dotenv import load_dotenv


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "security.login"
turbo = Turbo()
load_dotenv()

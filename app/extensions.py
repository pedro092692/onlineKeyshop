from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean, ForeignKey, DateTime
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()

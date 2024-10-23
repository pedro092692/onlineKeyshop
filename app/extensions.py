from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean, ForeignKey, DateTime
from typing import List
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from sqlalchemy import exists

db = SQLAlchemy()

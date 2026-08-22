from sqlalchemy import (
    Column, 
    String, 
    Integer, 
    Enum as SQLEnum
)
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from src.db import Base
from src.common.enums import (
    UserRole, 
    UserStatus, 
    UserVisibility
)



class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer, 
        primary_key = True, 
        nullable = False
    )

    name = Column(
        String(30), 
        nullable = False
    )

    lastname = Column(
        String(30),
        nullable = True
    )

    username = Column(
        String(30), 
        nullable = False, 
        unique = True
    )

    biography = Column(
        String(250),
        nullable = True
    )
    email = Column(
        String(60), 
        nullable = False, 
        unique = True
    )

    password = Column(
        String, 
        nullable = False
    )

    role = Column(
        SQLEnum(*(e.value for e in UserRole), name = "user_role_enum"),
        nullable = False,
        server_default = "user"
    )

    status = Column(
        SQLEnum(*(e.value for e in UserStatus), name = "user_status_enum"),
        nullable = False,
        server_default = "active"
    )

    visibility = Column(
        SQLEnum(*(e.value for e in UserVisibility), name = "user_visibility_enum"),
        nullable = False,
        server_default = "public"
    )

    created_at = Column(
        TIMESTAMP(timezone = True), 
        server_default = text("now()"), 
        nullable = False
    )

    updated_at = Column(
        TIMESTAMP(timezone = True),
        server_default = text("now()"),
        nullable = False
    )

    def __repr__(self):
        return f"<User id={self.id} username={self.username} email={self.email}>"
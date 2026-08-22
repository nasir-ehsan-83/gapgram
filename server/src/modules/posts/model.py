from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy import (
    Column, 
    String, 
    Integer, 
    ForeignKey, 
    Enum as SQLEnum
)
from src.db import Base
from src.modules.users.model import User # type: ignore
from src.common.enums import (
    PostStatus, 
    PostType, 
    PostVisibility
)

class Post(Base):
    __tablename__ = "posts"

    id = Column(
        Integer, 
        primary_key = True, 
        nullable = False
    )

    title = Column(
        String, 
        nullable = False
    )

    content = Column(
        String, 
        nullable = False
    )

    status = Column(
        SQLEnum(*(e.value for e in PostStatus), name = "post_status_enum"),
        nullable = False,
        server_default = "published"
    )

    type = Column(
        SQLEnum(*(e.value for e in PostType), name = "post_type_enum"),
        nullable = False
    )

    visibility = Column(
        SQLEnum(*(e.value for e in PostVisibility), name = "post_visibility_enum"),
        nullable = False,
        server_default = "public"
    )

    media_url = Column(
        String, 
        nullable = True
    )

    owner_id = Column(
        Integer, 
        ForeignKey("users.id", ondelete = "CASCADE"), 
        nullable = False
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

    owner = relationship("User", lazy = "joined")

    def __repo__(self):
        return f"<Post id:{self.id} title: {self.title} owner_id: {self.owner_id}>"
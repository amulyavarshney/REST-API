from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from .database import Base


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    # date = Column(Date, default=datetime.now().strftime("%Y-%m-%d" "%H:%M:%S"))
    name = Column(String(50), nullable=False, index=True)
    dob = Column(String(10), index=True)
    status = Column(String(6), index=True)
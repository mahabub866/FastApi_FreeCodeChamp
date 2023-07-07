from datetime import datetime, timezone,timedelta
from email.policy import default

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship

from db.database import Base

# Python3 code to generate the
# random id using uuid1()
  
import uuid

CATEGORIES = (
    ('REGISTRATION', 'reg'),
    ('ADMIN', 'admin'),
    ('XRAY', 'xray'),
    ('MDOCTOR', 'm_doctor'),
    ('EYE', 'eye'),
    ('FDOCTOR', 'f_doctor'),
    ('URIN', 'urin')
)
RECEIPT_STATUSES = (
    ('PROCESSING', 'processing'),
    ('REJECT', 'reject'),
    ('HOLD', 'hold'),
    ('DONE', 'done')
)



class DbCount(Base):
    __tablename__="counts"


    count_no=Column(Integer,default=1)
    date=Column(DateTime, default=datetime.now())
    id = Column(String, primary_key = True, default = str(uuid.uuid4()) )
    def __repr__(self):
        return f'<DbCount {self.count_no}'

class DbToken(Base):

    __tablename__ = 'tokens'

    id = Column(Integer, primary_key=True, index=True)
    token_id = Column(Integer)
    create_at = Column(DateTime, default=datetime.now(timezone.utc))
    # token_status = Column(ChoiceType(
    #     choices=RECEIPT_STATUSES), default="PROCESSING")
    token_status = Column(String, default="PROCESSING")
    reg = Column(Boolean, default=False)
    xray = Column(Boolean, default=False)
    m_doctor = Column(Boolean, default=False)
    f_doctor = Column(Boolean, default=False)
    eye = Column(Boolean, default=False)
    urin = Column(Boolean, default=False)
    is_picked = Column(Boolean, default = False)
    counter =  Column(Integer)
    
    t_counter_categories = Column(String, ForeignKey(
        "users.counter_categories"), nullable=False)

    user = relationship("DbUser", back_populates="reg_token")

    def __repr__(self):
        return f'<DbToken {self.token_id}'

class DbUser(Base):

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(25), unique=True)
    email = Column(String(80), unique=True)
    counter_name = Column(String(80), unique=True)
    counter_no = Column(Integer, unique=True)
    password = Column(String, nullable=True)
    is_active = Column(Boolean, default=False)
    is_staff = Column(Boolean, default=False)
    # counter_categories = Column(ChoiceType(
    #     choices=CATEGORIES), default="REGISTRATION")
    counter_categories = Column(String, default="reg")
    # # counter_categories = Column(ChoiceType(
    # #     choices=CATEGORIES), default="REGISTRATION")
    # counter_f =  Column(Integer, ForeignKey(
    #     "users.counter_no"), nullable=True)

    reg_token = relationship("DbToken", back_populates="user")

    def __repr__(self):
        return f'<DbUser {self.username}'

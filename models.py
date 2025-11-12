from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base

class Team(Base):
    __tablename__ = "teams"
    key = Column(String, primary_key=True)  # 'left' | 'right'
    name = Column(String, nullable=False)

class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    total_sum = Column(Integer, default=0)
    team_key = Column(String, ForeignKey("teams.key"), default="left")
    results = relationship("Result", back_populates="employee", cascade="all, delete-orphan")

class Result(Base):
    __tablename__ = "results"
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False, index=True)
    day = Column(String, nullable=False)  # 'ПТ','СБ','ПН','ВТ','СР','ЧТ'
    amount = Column(Integer, default=0)
    employee = relationship("Employee", back_populates="results")
    __table_args__ = (UniqueConstraint("employee_id", "day", name="uniq_emp_day"),)

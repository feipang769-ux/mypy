from sqlalchemy.orm import (
                            DeclarativeBase,
                            MappedAsDataclass,
                            Mapped,
                            mapped_column,
                            )
from sqlalchemy import (
                        DateTime, 
                        func, 
                        String, 
                        Text, 
                        CheckConstraint,
                        )
from datetime import datetime
from typing import Optional


class Base(MappedAsDataclass, DeclarativeBase):
    pass

class Task(Base):
    __tablename__ = 'user_task'


    __table_args__ = (
        CheckConstraint(
            "status IN ('pending', 'achieved', 'cancelled')", 
            name="check_table_status"
        ),
        CheckConstraint(
            "priority IN ('high', 'medium', 'low') OR priority IS NULL", 
            name="check_table_priority"
        ),
    )


    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    title: Mapped[str] = mapped_column(String(200), index=True)
# optional of description or none
    description: Mapped[Optional[str]] = mapped_column(Text, default=None)
# status: pending, achieved, cancelled
    status: Mapped[str] = mapped_column(String(20), index=True, default='pending')
# optional of priority or none
    priority: Mapped[Optional[str]] = mapped_column(String(20), default=None, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        init=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        init=False,
    )


    def __repr__(self):
        return f'Task(AAAid={self.id}, title={self.title}, status={self.status})'



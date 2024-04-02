# long_term_memory_app/app/models/models.py

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ConversationSummary(db.Model):
    __tablename__ = 'conversation_summaries'

    id = db.Column(db.Integer, primary_key=True)
    summary = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<ConversationSummary {self.id}>'

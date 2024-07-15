# app/models.py

from . import db

class QnA(db.Model):
    __tablename__ = 'qna'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String, nullable=False)
    answer = db.Column(db.String, nullable=False)

def init_db():
    # No need to call db.init_app(app) here
    with db.create_all():
        pass

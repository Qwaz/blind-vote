from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Setting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    value = db.Column(db.String(200))

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return '<Setting %s>' % self.name


class Voters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True)
    voted = db.Column(db.Boolean())

    def __init__(self, key):
        self.key = key
        self.voted = False

    def __repr__(self):
        return '<Voters %s>' % self.key

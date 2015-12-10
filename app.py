import os, binascii
from flask import Flask
from models import db, Setting

app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)


def generate_key():
    return binascii.hexlify(os.urandom(10)).decode('ascii')


@app.route('/')
def hello_world():
    if Setting.query.filter_by(name='master').first():
        return 'Master Key Initialized'
    else:
        master = Setting('master', generate_key())
        db.session.add(master)
        db.session.commit()
        return 'Master Key is %s' % master.value


if __name__ == '__main__':
    app.debug = True
    with app.app_context():
        db.create_all()
    app.run('0.0.0.0', port=8080)

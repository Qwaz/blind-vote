import os, binascii
from flask import Flask, render_template, redirect, url_for
from models import db, Setting
from forms import InitForm

app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)


def generate_key():
    return binascii.hexlify(os.urandom(10)).decode('ascii')


@app.route('/init', methods=['POST'])
def init():
    if Setting.query.filter_by(name='matser').first():
        return redirect(url_for('index'))
    else:
        form = InitForm()
        return redirect(url_for('index'))


@app.route('/')
def index():
    if Setting.query.filter_by(name='master').first():
        return render_template('simple.html', title="초기화 완료!", content="초기화되었습니다")
    else:
        form = InitForm()
        form.master.data = generate_key()
        return render_template('init.html', form=form)


if __name__ == '__main__':
    app.debug = True
    with app.app_context():
        db.create_all()
    app.run('0.0.0.0', port=8080)

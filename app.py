import os, binascii
from flask import Flask, request, render_template, redirect, url_for
from models import db, Setting
from forms import InitForm, StartForm

app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)


def generate_key():
    return binascii.hexlify(os.urandom(10)).decode('ascii')


@app.route('/init', methods=['POST'])
def init():
    if Setting.query.filter_by(name='master').first():
        return redirect(url_for('index'))
    else:
        form = InitForm()
        if form.validate():
            db.session.add(Setting('master', form.master.data))
            db.session.add(Setting('vote_name', form.vote_name.data))
            db.session.add(Setting('detail', form.detail.data))
            db.session.add(Setting('response', form.response.data))
            db.session.add(Setting('wait', 'true'))
            db.session.commit()
        return redirect(url_for('index'))


@app.route('/start', methods=['GET', 'POST'])
def start():
    if not Setting.query.filter_by(name='master').first():
        return redirect(url_for('index'))
    form = StartForm()

    error = False
    if request.method == 'POST':
        if not form.validate():
            error = '폼을 채워 주세요'
        if form.master.data != Setting.query.filter_by(name='master').first().value:
            error = '마스터 키가 틀렸어요'
        if not error:
            Setting.query.filter_by(name='wait').first().value = 'false'
            db.session.commit()
            # TODO 각 키에 대응하는 Voter 생성
            return redirect(url_for('index'))
    return render_template('start.html', form=form, error=error)


@app.route('/')
def index():
    if Setting.query.filter_by(name='master').first():
        if Setting.query.filter_by(name='wait').first().value == 'true':
            vote_name = Setting.query.filter_by(name='vote_name').first().value
            return render_template('wait.html', vote_name=vote_name, key=generate_key())
        else:
            return "실제 투표 아직 구현 안 됨"
    else:
        form = InitForm()
        form.master.data = generate_key()
        return render_template('init.html', form=form)


if __name__ == '__main__':
    app.debug = True
    with app.app_context():
        db.create_all()
    app.run('0.0.0.0', port=8080)

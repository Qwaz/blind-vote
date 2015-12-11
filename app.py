import os, binascii, re
from flask import Flask, request, render_template, redirect, url_for
from models import db, Setting, Voters, Vote
from forms import InitForm, StartForm, VoteForm

app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)


def get_stage():
    return Setting.query.filter_by(name='stage').first()


def generate_key():
    return binascii.hexlify(os.urandom(10)).decode('ascii')


def split_response():
    p = re.compile(',\s*')
    split_array = p.split(Setting.query.filter_by(name='response').first().value)
    return zip([str(i) for i in range(len(split_array))], split_array)


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
            get_stage().value = 'wait'
            db.session.commit()
        return redirect(url_for('index'))


@app.route('/start', methods=['GET', 'POST'])
def start():
    if get_stage().value != 'wait':
        return redirect(url_for('index'))
    form = StartForm()

    error = False
    if request.method == 'POST':
        if not form.validate():
            error = '폼을 채워 주세요'
        if form.master.data != Setting.query.filter_by(name='master').first().value:
            error = '마스터 키가 틀렸어요'
        if not error:
            for key in form.keys.data.split():
                db.session.add(Voters(key))
            get_stage().value = 'vote'
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('start.html', form=form, error=error)


@app.route('/vote', methods=['GET', 'POST'])
def vote():
    if get_stage().value != 'vote':
        return redirect(url_for('index'))
    form = VoteForm()
    form.selection.choices = split_response()

    error = False
    if request.method == 'POST':
        if not form.validate():
            error = '폼을 채워 주세요'
        else:
            voter = Voters.query.filter_by(key=form.key.data).first()
            if not voter:
                error = '키를 잘못 입력했어요'
            elif voter.voted:
                error = '이미 투표하셨네요'
            else:
                voter.voted = True
                vote = Vote(int(form.selection.data))
                db.session.add(vote)
                db.session.commit()
                return render_template('result.html', vote=vote, select=list(split_response())[vote.selection][1])
        form.selection.choices = split_response()
    return render_template('vote.html', form=form, error=error,
                           vote_name=Setting.query.filter_by(name='vote_name').first().value)


@app.route('/')
def index():
    stage = get_stage()
    if stage.value == 'init':
        form = InitForm()
        form.master.data = generate_key()
        return render_template('init.html', form=form)
    elif stage.value == 'wait':
        vote_name = Setting.query.filter_by(name='vote_name').first().value
        return render_template('wait.html', vote_name=vote_name, key=generate_key())
    elif stage.value == 'vote':
        return redirect(url_for('vote'))


if __name__ == '__main__':
    app.debug = True
    with app.app_context():
        db.create_all()
        if not get_stage():
            db.session.add(Setting('stage', 'init'))
            db.session.commit()
    app.run('0.0.0.0', port=8080)

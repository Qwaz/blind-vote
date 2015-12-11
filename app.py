import os, binascii, re
from flask import Flask, request, render_template, redirect, url_for
from models import db, Setting, Voters, Vote
from forms import InitForm, StartForm, VoteForm

app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)


def get_setting(name):
    setting = Setting.query.filter_by(name=name).first()
    return setting.value if setting else None
app.jinja_env.globals.update(get_setting=get_setting)


def set_stage(stage):
    Setting.query.filter_by(name='stage').first().value = stage


def generate_key():
    return binascii.hexlify(os.urandom(10)).decode('ascii')


def get_remain():
    return Voters.query.filter_by(voted=False).count()


def split_response():
    p = re.compile(',\s*')
    split_array = p.split(get_setting('response'))
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
            set_stage('wait')
            db.session.commit()
        return redirect(url_for('index'))


@app.route('/start', methods=['GET', 'POST'])
def start():
    if get_setting('stage') != 'wait':
        return redirect(url_for('index'))
    form = StartForm()

    error = False
    if request.method == 'POST':
        if not form.validate():
            error = '폼을 채워 주세요'
        if form.master.data != get_setting('master'):
            error = '마스터 키가 틀렸어요'
        if not error:
            for key in form.keys.data.split():
                db.session.add(Voters(key))
            set_stage('vote')
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('start.html', form=form, error=error)


@app.route('/vote', methods=['GET', 'POST'])
def vote():
    if get_setting('stage') != 'vote':
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
                remain = get_remain()
                if remain == 0:
                    set_stage('result')
                db.session.commit()
                return render_template('result.html', vote=vote, select=list(split_response())[vote.selection][1],
                                       remain=remain)
        form.selection.choices = split_response()
    return render_template('vote.html', form=form, error=error,
                           remain=get_remain())


@app.route('/')
def index():
    stage = get_setting('stage')
    if stage == 'init':
        form = InitForm()
        form.master.data = generate_key()
        return render_template('init.html', form=form)
    elif stage == 'wait':
        return render_template('wait.html', key=generate_key())
    elif stage == 'vote':
        return redirect(url_for('vote'))
    elif stage == 'result':
        result = []
        responses = split_response()
        for selection, name in responses:
            result.append((name, Vote.query.filter_by(selection=int(selection)).count()))
        return render_template('final.html', result = result)


if __name__ == '__main__':
    app.debug = True
    with app.app_context():
        db.create_all()
        if not get_setting('stage'):
            db.session.add(Setting('stage', 'init'))
            db.session.commit()
    app.run('0.0.0.0', port=8080)

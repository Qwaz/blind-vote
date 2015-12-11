from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, HiddenField, RadioField
from wtforms.validators import DataRequired


class InitForm(Form):
    master = HiddenField('마스터키')
    vote_name = StringField('투표명', validators=[DataRequired()])
    detail = TextAreaField('질문')
    response = StringField('답변(쉼표로 구분)', validators=[DataRequired()])


class StartForm(Form):
    master = StringField('마스터키', validators=[DataRequired()])
    keys = TextAreaField('키 목록', validators=[DataRequired()])


class VoteForm(Form):
    key = StringField('키', validators=[DataRequired()])
    selection = RadioField('투표', validators=[DataRequired()])

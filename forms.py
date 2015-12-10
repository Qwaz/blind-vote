from flask.ext.wtf import Form

from wtforms import StringField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length

class InitForm(Form):
    master = HiddenField('마스터키')
    vote_name = StringField('투표명', validators=[DataRequired()])
    detail = TextAreaField('질문')
    response = StringField('답변(쉼표로 구분)', validators=[DataRequired()])
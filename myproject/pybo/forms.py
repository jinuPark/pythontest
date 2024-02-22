from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, EmailField
from wtforms.validators import DataRequired, EqualTo, Email, Length

#FlaskForm을 상속

#로그인 : email, password

class UserLoginForm(FlaskForm):
    email = EmailField('이메일',validators=[DataRequired(), Email()])
    password = PasswordField('비밀번호', validators=[DataRequired()])

class UserCreateForm(FlaskForm):
    #Length: 이름 최소 3글, 최대 25글자
    username = StringField('사용자 이름', validators=[DataRequired('이름은 입력 필수 입니다.'), Length(min=3,max=25)])
    
    #EqualTo : password1 == password2 동일한지 check용
    #<input type='password'/>
    password1 = PasswordField('비밀번호', validators=[DataRequired()
        ,EqualTo('password2','비밀번호가 일치하지 않습니다.')])
    password2 = PasswordField('비밀번호 확인', validators=[DataRequired()])
    # <input type='email'/>
    # pip install email_validator
    email     = EmailField('이메일', validators=[DataRequired(),Email()])

class QuestionForm(FlaskForm):
    #StringField 글자수 제한이 있는 경우
    subject = StringField('제목', validators=[DataRequired('제목은 입력 필수 입니다.')])
    #TextAreaField 글자수 제한이 없는 경우
    contents = TextAreaField('내용',validators=[DataRequired('내용은 필수 입력 항목 입니다.')])

#답변 등록 form
class AnswerForm(FlaskForm):
    contents = TextAreaField('내용',validators=[DataRequired('내용은 필수 입력 항목 입니다.')])
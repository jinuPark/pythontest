from pybo import db


#question voter : 다대다(N:N) 관계
question_voter = db.Table(
    'question_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE', primary_key=True)),
    db.Column('question_id', db.Integer, db.ForeignKey('question.id', ondelete='CASCADE', primary_key=True))
)


class User(db.Model):
    id = db.Column(db.Integer,primary_key=True) #숫자
    username = db.Column(db.String(150),nullable=False) #문자, not null
    password = db.Column(db.String(200),nullable=False) #문자, not null
    email    = db.Column(db.String(320),nullable=False,unique=True) #문자, not null

class Question(db.Model):
    id = db.Column(db.Integer,primary_key=True) #숫자
    subject = db.Column(db.String(200),nullable=False) #문자
    contents = db.Column(db.Text(),nullable=False) #오라클 CLOB
    create_date = db.Column(db.DateTime(),nullable=False) #날짜
    #server_default, default : server_default는 기존 데이터에도 적용, default는 신규 데이터에만 적용
    user_id     = db.Column(db.Integer,db.ForeignKey('user.id', ondelete='CASCADE'),nullable=False)#User와 fk연결
    user        = db.relationship('User', backref=db.backref('question_set')) #User모델을 참조하기 위한 속성
    modify_date = db.Column(db.DateTime(), nullable=True) #수정일
    voter = db.relationship('User', secondary=question_voter, backref=db.backref('question_voter_set'))

#answer voter : 다대다(N:N) 관계
answer_voter = db.Table(
    'answer_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE', primary_key=True)),
    db.Column('answer_id', db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE', primary_key=True))
)

class Answer(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    # fk생성:sql수행시 적용
    # ondelete='CASCADE' ->sql수행시 적용
    # question = db.relationship('Question',backref=db.backref('answer_set', cascade='all, delete-origin'))
    question_id = db.Column(db.Integer,db.ForeignKey('question.id',ondelete='CASCADE'))
    question = db.relationship('Question',backref=db.backref('answer_set'))
    contents = db.Column(db.Text(),nullable=False)
    create_date = db.Column(db.DateTime(),nullable=False)
    #server_default, default : server_default는 기존 데이터에도 적용, default는 신규 데이터에만 적용
    user_id     = db.Column(db.Integer,db.ForeignKey('user.id', ondelete='CASCADE'),nullable=False)#User와 fk연결
    user        = db.relationship('User', backref=db.backref('answer_set')) #User모델을 참조하기 위한 속성
    modify_date = db.Column(db.DateTime(), nullable=True) #수정일
    voter = db.relationship('User', secondary=answer_voter, backref=db.backref('answer_voter_set'))


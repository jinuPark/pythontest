from flask import Blueprint, render_template, request, url_for, redirect, g, flash  # redirect 추가
from pybo.models import Question
from pybo.forms import QuestionForm, AnswerForm
from datetime import datetime

from .answer_views import login_required
from .. import db

bp = Blueprint('question', __name__, url_prefix='/question')


@bp.route('/vote/<int:question_id>')
@login_required
def vote(question_id):
    _question = Question.query.get_or_404(question_id)
    #본인이 작성한 글은 추천 불가
    if g.user == _question.user:
        flash('본인이 작성한 글은 추천 불가 합니다.')
    else:
        _question.voter.append(g.user)
        db.session.commit()
    return redirect(url_for('question.detail',question_id=question_id))



#삭제 : delete
@bp.route('/delete/<int:question_id>')
@login_required
def delete(question_id):

    question = Question.query.get_or_404(question_id) #question_id에 해당하는 데이터 조회

    #권한: 글쓴이만 삭제 가능
    if g.user != question.user:
        flash('삭제권한이 없습니다.')
        return redirect(url_for('question.detail', question_id=question_id))


    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('question._list'))




#수정 : question_form.html 같이 사용
@bp.route('/modify/<int:question_id>',methods=('GET', 'POST'))
@login_required
def modify(question_id):
    print('-'*30)
    print(f'question_id:{question_id}')
    print(f'request.method  :{request.method}')
    print('-' * 30)
    question = Question.query.get_or_404(question_id)

    #수정 권한 체크
    if g.user != question.user:
        flash('수정 권한이 없습니다.')
        return redirect( url_for('question.detail',question_id=question_id))


    if request.method == 'POST':    #POST
        form = QuestionForm()

        if form.validate_on_submit():
            #수정 : form 변수 들어 있는 데이터를 question객체에 update역할
            form.populate_obj(question) #화면에서 들어오는 질문 제목, 내용 update
            question.modify_date = datetime.now() #수정일시
            print(f'question:{question}')
            db.session.commit()
            return redirect( url_for('question.detail',question_id=question_id))



        pass
    else:   #GET
        form = QuestionForm(obj=question)

    return render_template('question/question_form.html',form=form)

    pass


#@@login_required @bp.route뒤에 위치해야 한다. 그렇지 않으면 정상 동작 하지 않는다.
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    form = QuestionForm()

    print(f'create,request:{request.method}')  # 따옴표 변경
    print(f'form.validate_on_submit():{form.validate_on_submit()}')  # 따옴표 변경

    if request.method == 'POST' and form.validate_on_submit():
        question = Question(subject=form.subject.data,contents=form.contents.data
                            ,create_date=datetime.now(), user=g.user)
        db.session.add(question)
        db.session.commit()

        print(f'main,request:{url_for("main.index")}')  # 따옴표 변경
        return redirect(url_for('main.index'))  # 리다이렉트 수정

    return render_template('question/question_form.html', form=form)

@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    form = AnswerForm()  # 답변을 입력할 폼 생성
    question = Question.query.get_or_404(question_id)  # question_id에 해당하는 질문을 데이터베이스에서 가져옴
    return render_template('question/question_detail.html', question=question, form=form)  # 질문 상세 페이지 템플릿을 렌더링하고, 질문과 답변 폼을 전달

@bp.route('/list')
def _list():
    question_list = Question.query.order_by(Question.create_date.desc())

    #paging: http://127.0.0.1:5000/question/list?page=1
    page = request.args.get('page', type=int, default=1)
    print(f'page:{page}')

    question_list=question_list.paginate(page=page, per_page=10)



    print(f'question_list:{question_list}')

    return render_template('question/question_list.html', question_list=question_list)
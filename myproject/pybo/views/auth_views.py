#g변수는 : 플라스크의 컨텍스트 변수
from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from pybo import db
from pybo.forms import UserCreateForm, UserLoginForm
from pybo.models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')



@bp.route('/logout')
def logout():
    session.clear() # session 삭제
    return redirect( url_for('main.index'))


#로그인 여부 확인
# bp.before_app_request : 모든 request전에 수행되는 기능의 어노테이션
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)


@bp.route('/login',methods=("GET","POST"))
def login():
    form = UserLoginForm()
    #로그인 화면에서 로그인 버튼 click
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        print(f'-'*50)
        print(f'email:{form.email.data}')
        print(f'password:{form.password.data}')
        print(f'-'*50)

        #email존재 유무 check
        user = User.query.filter_by(email= form.email.data).first()
        print(f'user:{user}')
        #flag = check_password_hash(user.password, form.password.data)
        #print(f'flag:{flag}')

        if not user:
            error = '존재하지 않는 사용자입니다.'
        elif not check_password_hash(user.password, form.password.data):
            error = '비밀번호를 확인 하세요.'

        #로그인 session처리
        if error is None:
            session.clear() #session clear
            session['user_id'] = user.id #session : user_id

            _next = request.args.get('next','')

            # _next 유무에 따라 : next 파라미터 값이 없으며 메인 페이지로, 있으면, 로그인 후 해당 페이지로

            if _next :
                return redirect(_next)
            else :
                return redirect(url_for('main.index'))

            return redirect(url_for('main.index'))

        #error 메시지 전달
        flash(error)



    return render_template('auth/login.html',form=form)

# GET: 화면 등록 화면
# POST: 회원가입 저장
@bp.route('/signup', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()

    # 회원 가입 저장
    if request.method == 'POST' and form.validate_on_submit():
        # 사용자가 존재하는지 확인
        user = User.query.filter_by(email=form.email.data).first()
        print('-' * 50)
        print('-' * 50)
        print(f'user:{user}')

        if not user:
            # 회원 생성
            new_user = User(username=form.username.data,
                            password=generate_password_hash(form.password1.data),
                            email=form.email.data)

            # DB에 추가하고 commit
            db.session.add(new_user)
            db.session.commit()

            flash('회원가입이 완료되었습니다.')
            return redirect(url_for('main.index'))
        else:
            flash(f'이미 존재하는 사용자입니다.{user.username}')

    return render_template('auth/signup.html', form=form)
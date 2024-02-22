from flask import Blueprint,url_for
from werkzeug.utils import redirect

#__name__: main_views.py
bp = Blueprint('main',__name__,url_prefix='/')


@bp.route('/hello')
def hello_pybo():
    return "Hello, world!!!"

@bp.route('/')
def index():
    #redirect(URL) : URL로 페이지 이동
    #url_for(라우팅 함수명) : 라우팅 함수에 매핑되어 있는 URL return
    print("-"*50)
    print(f'url_for(question._list):{url_for('question._list')}')
    print("-" * 50)
    return redirect(url_for('question._list'))
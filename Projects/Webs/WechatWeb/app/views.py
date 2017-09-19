from app import app


@app.route('/')
@app.route('/index')
def index():
    return request.args.items().__str__()
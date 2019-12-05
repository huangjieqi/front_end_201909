from flask import Flask, render_template, request, escape
from vsearch import search4letters
from viwe_log import *
from DBcm import UseDatabase

app = Flask(__name__)

app.config['dbconfig'] = {'host': '127.0.0.1',
                          'user': 'root',
                          'password': '123456',
                          'database': 'new', }


def log_request(req: 'flask_request') -> None:
    """Log details of the web request and the results."""

    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """insert into new
                  (title, type, description, place, img)
                  values
                  (%s, %s, %s, %s, %s)"""
        cursor.execute(_SQL, (req.form['title'],
                              req.form['type'],
                              req.form['description'],
                              req.form['place'],
                              req.form['img'], ))


@app.route('/search4', methods=['POST'])
def do_search() -> 'html':
    """Extract the posted data; perform the search; return results."""
    title = request.form['title']
    type = request.form['type']
    description = request.form['description']
    place = request.form['place']
    img = request.form['img']
    title = 'Here are your results:'
    log_request(request)
    return render_template('results.html',
                           the_title=title,
                           title = title,
                           type = type,
                           description = description,
                           place = place,
                           img = img,)


@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    """Display this webapp's HTML form."""
    return render_template('entry.html',
                           the_title='欢迎使用新闻发布系统')


@app.route('/viewlog')
def view_the_log() -> 'html':
    """Display the contents of the log file as a HTML table."""
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """select title, type, description, place, img
                  from new"""
        cursor.execute(_SQL)
        contents = cursor.fetchall()
    titles = ('title', 'type', 'description', 'place', 'img')
    return render_template('viewlog.html',
                           the_title='View Log',
                           the_row_titles=titles,
                           the_data=contents,)


if __name__ == '__main__':
    app.run(debug=True)

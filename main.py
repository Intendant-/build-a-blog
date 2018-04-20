from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True      # displays runtime errors in the browser, too
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:launchcode@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    body = db.Column(db.String(200))
    ##pub_date = db.Column(db.DateTime)

    def __init__(self, title, body): ## pub_date = None):
        self.title = title
        self.body = body
        ##if pub_date is None:
        ##    pub_date = datetime.utcnow()
        ##self.pub_date = pub_date

def blog_entries():
    return Blog.query.all()

@app.route('/')
def index():
    return redirect('/blog')

@app.route('/newpost', methods=['GET', 'POST'])
def newpost():
    if request.method == 'POST':
        title = request.form['blog_title']
        body = request.form['blog_text']
        blg_title = ''
        blg_text = ''
        if not title or not body:
            error = '**Please fill in both fields'
            blg_title = title
            blg_text = body
            return render_template('newpost.html', blog_title = blg_title, blog_text = blg_text, error= error)
        # TODO validate form title and body
        else:
            entry = Blog(title, body)
            db.session.add(entry)
            db.session.commit()
            return redirect('/blog?id={0}'.format(entry.id)) 
    else:  
        return render_template('newpost.html')

@app.route('/blog', methods=['GET', 'POST'])
def blog():
    id = request.args.get('id')
    if id:
        post = Blog.query.filter_by(id=id).first()
        return render_template('post.html', post = post)
    else:
        return render_template('blog.html', blog_entries = blog_entries()) 

@app.route("/blog?id=")
def post():
    id = request.args.get('id')
    return render_template('post.html', entry=entry)

if __name__ == "__main__":
    app.run()      
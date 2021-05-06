from flask import Flask, render_template,request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

myApp=Flask(__name__)
myApp.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///site.db'
db=SQLAlchemy(myApp)


class Blog(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(150), nullable=False)
    intro = db.Column(db.Text, nullable=False)
    story = db.Column(db.Text , nullable=False)
    data_ = db.Column(db.DateTime, default=datetime.utcnow())
    def __repr__(self):
        return'Blog %r'%self.id
@myApp.route('/index')
@myApp.route('/')
def intex():
    notes = Blog.query.all()
    notes= notes[::-1]
    return render_template('first.html', notes=notes)

@myApp.route('/about', methods=['POST','GET'])
def about():
    if request.method=='POST':
        title=request.form['title']
        intro=request.form['intro']
        story=request.form['story']
        blog=Blog(title=title, intro=intro, story=story)
        try:
            db.session.add(blog)
            db.session.commit()
            return redirect('/')
        except:
            return 'error'
    else:
        return render_template('def.html')

@myApp.route('/other')
def other():
        return render_template('def2.html')

@myApp.route('/sign', methods=['POST','GET'])
def sign():
    if request.method=='POST':
        names=request.form['login']
        passes=request.form['password']
        return names,passes
    return render_template('singIn.html')

@myApp.route('/print_db/<int:id>')
def side(id):
    ob_db = Blog.query.get(id)
    return render_template('printer_db.html', ob_db=ob_db)

@myApp.route('/print_db/<int:id>/delete')
def deletes(id):
    delete_obj = Blog.query.get_or_404(id)
    try:
        db.session.delete(delete_obj)
        db.session.commit()
        return redirect('/')
    except:
        return 'error'

@myApp.route('/print_db/<int:id>/editor')
def editor(id):
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        story = request.form['story']
        blog = Blog(title=title, intro=intro, story=story)
        try:
            db.session.add(blog)
            db.session.commit()
            return redirect('/')
        except:
            return 'error'
    else:
        return render_template('def.html')


if __name__=='__main__':
    myApp.run(debug=True)
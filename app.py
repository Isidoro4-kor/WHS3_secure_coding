import os
from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=True)
    user = db.relationship('User')
    children = db.relationship('Comment')
    is_deleted = db.Column(db.Boolean, default=False)  




@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        email = request.form['email']
        pw = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, pw):
            session['user_id'] = user.id
            return redirect('/home')
        else:
            return '로그인 실패!'
    return render_template('main.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        pw = request.form['password']
        hashed_pw = bcrypt.generate_password_hash(pw).decode('utf-8')
        if User.query.filter_by(email=email).first():
            return '이미 존재하는 이메일입니다.'
        new_user = User(email=email, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/')
    return render_template('register.html')

@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect('/')
    items = Item.query.all()
    return render_template('home.html', items=items)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'user_id' not in session:
        return redirect('/')
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        desc = request.form['description']
        image = request.files['image']
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        new_item = Item(name=name, price=price, description=desc,
                        image=filename, user_id=session['user_id'])
        db.session.add(new_item)
        db.session.commit()
        return redirect('/home')
    return render_template('upload.html')

@app.route('/item/<int:item_id>', methods=['GET', 'POST'])
def item_detail(item_id):
    item = Item.query.get_or_404(item_id)
    uploader = User.query.get(item.user_id)
    comments = Comment.query.filter_by(item_id=item_id, parent_id=None).all()

    if request.method == 'POST' and 'user_id' in session:
        text = request.form['comment'].strip()
        parent_id = request.form.get('parent_id')

        if text:  # 빈 댓글이 아닐 때만 저장
            new_comment = Comment(
                text=text,
                item_id=item_id,
                user_id=session['user_id'],
                parent_id=parent_id if parent_id else None
            )
            db.session.add(new_comment)
            db.session.commit()

        return redirect(url_for('item_detail', item_id=item_id))

    return render_template('item.html', item=item, uploader=uploader, comments=comments)


@app.route('/comment/edit/<int:comment_id>', methods=['GET', 'POST'])
def edit_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if 'user_id' not in session or comment.user_id != session['user_id']:
        return '권한이 없습니다.', 403

    if request.method == 'POST':
        comment.text = request.form['text']  
        db.session.commit()
        return redirect(url_for('item_detail', item_id=comment.item_id))

    return render_template('edit_comment.html', comment=comment)

@app.route('/comment/delete/<int:comment_id>', methods=['POST'])
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if 'user_id' not in session or comment.user_id != session['user_id']:
        return '권한이 없습니다.', 403

    comment.is_deleted = True  
    db.session.commit()
    return redirect(url_for('item_detail', item_id=comment.item_id))




@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

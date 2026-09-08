import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Đổi secret key phù hợp
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Vui lòng đăng nhập để truy cập trang này."

# --- BẢNG USER (MÔ HÌNH DỮ LIỆU) ---
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='author')  # 'reader', 'author', 'admin'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Tự động tạo cơ sở dữ liệu nếu chưa có
with app.app_context():
    db.create_all()

# --- ROUTES XỬ LÝ ---

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # 1. Kiểm tra email đã tồn tại chưa
        if User.query.filter_by(email=email).first():
            flash("Email đã tồn tại. Vui lòng sử dụng email khác!", "danger")
            return render_template("register.html")

        # 2. Kiểm tra username đã tồn tại chưa
        if User.query.filter_by(username=username).first():
            flash("Tên người dùng đã tồn tại!", "danger")
            return render_template("register.html")

        # 3. Tạo user mới & mã hóa mật khẩu
        new_user = User(username=username, email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        flash("Đăng ký tài khoản thành công! Hãy đăng nhập.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        # Kiểm tra sự tồn tại của User và khớp Mật khẩu
        if user and user.check_password(password):
            login_user(user)
            flash("Đăng nhập thành công!", "success")
            
            # Chuyển hướng tới trang người dùng định truy cập trước đó (nếu có)
            next_page = request.args.get('next')
            return redirect(next_page or url_for("home"))
        else:
            flash("Email hoặc mật khẩu không chính xác!", "danger")

    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Bạn đã đăng xuất thành công.", "info")
    return redirect(url_for("home"))

# Trang yêu cầu đăng nhập mới được truy cập
@app.route("/submit")
@login_required
def submit():
    return render_template("submit.html")

if __name__ == "__main__":
    app.run(debug=True)
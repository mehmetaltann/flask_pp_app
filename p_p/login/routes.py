from flask import render_template, request, redirect, url_for, flash, session
from p_p.extensions import db, login_manager, UserMixin, login_required, login_user, logout_user
from p_p.login import giris
from urllib.parse import urlparse, urljoin

login_manager.login_view = "giris.login"
login_manager.login_message = ""

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@giris.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter(User.username == username).first()
        if not user:
            flash('Kullanıcı adı hatalı', 'danger')
            return render_template("login.html")
        if not user.password == password:
            flash('Şifre Hatalı', 'danger')
            return render_template("login.html")
        login_user(user, remember=True)
        if "next" in session and session["next"]:
            if is_safe_url(session["next"]):
                return redirect(session["next"])
        return redirect(url_for("main.index"))
    session["next"] = request.args.get("next")
    return render_template("login.html")


@giris.route('/logout')
@login_required
def log_out():
    logout_user()
    return redirect(url_for("giris.login"))


@giris.route('/parametreler/')
@login_required
def parametreler():
    users = User.query.all()    
    return render_template("parametre.html", users=users)


@giris.route('/parametreler/ekle/kullanici/', methods=["GET", "POST"])
def parametreler_kullanici_ekle():
    if request.method == 'POST':
        username = request.form.get("kullaniciisimekle")
        password = request.form.get("kullanicisifreekle")
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Kullanıcı Veritabanına Eklenmiştir', 'success')
        return redirect(url_for("giris.parametreler"))
    else:
        flash('Veriler Eklenemedi', 'danger')
        return redirect(url_for("giris.parametreler"))
    
@giris.route('/parametreler/guncelle/kullanici/<int:user_id>/', methods=["GET", "POST"])
def parametreler_kullanici_guncelle(user_id):
    if request.method == 'POST':
        username = request.form.get("kullaniciadiguncelle")
        password = request.form.get("kullanicisifreguncelle")
        user = User.query.filter(User.id == user_id).first()
        user.username = username
        user.password = password
        db.session.commit()
        flash('Kullanıcı Verileri Güncellenmiştir.', 'success')
        return redirect(url_for("giris.parametreler"))
    else:
        flash('Kullanıcı Verileri Güncellenemedi', 'danger')
        return redirect(url_for("giris.parametreler"))
    
@giris.route('/parametreler/sil/kullanici/<int:user_id>/', methods=["GET", "POST"])
def parametreler_kullanici_sil(user_id):
    user = User.query.filter(User.id == user_id).first()
    db.session.delete(user)
    db.session.commit()
    flash('Seçilen Kullanıcı Veritabanından Silinmiştir', 'success')
    return redirect(url_for("giris.parametreler"))
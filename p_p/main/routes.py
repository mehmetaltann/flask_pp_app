from flask import render_template, request, redirect, url_for, flash
from p_p.main import main
from ..extensions import db, login_required
from ..models import Musteriler, MusteriSiparis, Siparisler, SiparisUrun, Urunler, UrunTarif, UrunMalzeme, Tarifler, TarifMalzeme, Hammaddeler, Notlar, Notlar2
from datetime import datetime
from .functions import tarih_getir,siparis_istatistikleri,siparis_maliyeti_gir,top10,siparis_bilgileri,istatistikler

#  ! ///////////////////////////////////////////////////////////////
# * INDEX SAYFASI

@main.route('/')
@login_required
def index():
    siparisler = Siparisler.query.all()
    urunler = Urunler.query.all()
    musteriler = Musteriler.query.all()
    bugun = datetime.now().date()
    return render_template("index.html", siparis_istatistikleri=siparis_istatistikleri(bugun), top10 = top10(siparisler,musteriler),
                           bugun = tarih_getir(bugun), musteriler=musteriler, urunler=urunler, siparisler=siparisler, 
                           siparis_bilgileri=siparis_bilgileri(siparisler))
    
# * Sipariş Ekle

@main.route('/anasayfa/siparis/ekle/', methods=['POST', 'GET'])
def index_siparis_ekle():
    isimler = ["siparismusteriekle", "siparisurunekle", "siparistarihiekle", "siparisturekle",
               "siparistutarekle", "siparismodelekle", "siparisnotekle"]
    if request.method == 'POST':
        siparis_bilgileri = {isim: request.form.get(isim) for isim in isimler}
        for key,values in siparis_bilgileri.items():
            if not siparis_bilgileri[key]:
                siparis_bilgileri[key] = None                 
        yeni_siparis = Siparisler(tarih=datetime.strptime(siparis_bilgileri["siparistarihiekle"], '%Y-%m-%d'), 
                                tur=siparis_bilgileri["siparisturekle"],
                                model=siparis_bilgileri["siparismodelekle"],
                                tutar=siparis_bilgileri["siparistutarekle"], 
                                aciklama=siparis_bilgileri["siparisnotekle"],
                                maliyet = 0)
        db.session.add(yeni_siparis)
        db.session.commit()
        son_siparis = Siparisler.query.order_by(Siparisler.id.desc()).first()
        yeni_musteri_siparisi = MusteriSiparis(musteri_id=siparis_bilgileri["siparismusteriekle"],siparis_id=son_siparis.id)
        db.session.add(yeni_musteri_siparisi)
        yeni_siparis_urun = SiparisUrun(urun_id=siparis_bilgileri["siparisurunekle"],siparis_id=son_siparis.id)
        db.session.add(yeni_siparis_urun)
        db.session.commit()
        siparis_maliyeti_gir(son_siparis.id)               
        flash('Sipariş Veritabanına Eklenmiştir', 'success')
        return redirect(url_for("main.index"))
    else:
        flash('Sipariş Verileri Eklenemedi', 'danger')
        return redirect(url_for("main.index"))
    
# * Müşteri Ekle

@main.route('/anasayfa/musteri/ekle/', methods=['POST', 'GET'])
def index_musteri_ekle():
    isimler = ["musteriisimekle", "musterisoyisimekle", "musteritelefonekle", "musterinotekle"]
    if request.method == 'POST':
        musteri_bilgileri = {isim: request.form.get(isim) for isim in isimler}
        for key,values in musteri_bilgileri.items():
            if not musteri_bilgileri[key]:
                musteri_bilgileri[key] = None           
        yeni_musteri = Musteriler(isim=musteri_bilgileri["musteriisimekle"], 
                                 soyisim=musteri_bilgileri["musterisoyisimekle"],
                                 telefon=musteri_bilgileri["musteritelefonekle"], 
                                 aciklama=musteri_bilgileri["musterinotekle"])
        db.session.add(yeni_musteri)
        db.session.commit()
        flash('Müşteri Veritabanına Eklenmiştir', 'success')
        return redirect(url_for("main.index"))
    else:
        flash('Müşteri Verileri Eklenemedi', 'danger')
        return redirect(url_for("main.index"))

#  ! ///////////////////////////////////////////////////////////////
# * HAMMADDE SAYFASI

@main.route('/hammadde')
@login_required
def hammadde():
    hamms = Hammaddeler.query.all()
    return render_template("hammadde.html", hammaddeler=hamms)

# * Hammadde Ekle

@main.route('/hammadde/ekle/', methods=['POST', 'GET'])
def hammadde_ekle():
    isimler = ["hammaddeisimekle", "hammaddetürüekle", "hammaddebirimekle", "hammaddemiktarekle", "hammaddefiyatekle", 
               "hammaddemarkaekle", "hammaddealinmatarihiekle", "hammaddenotekle"]
    if request.method == 'POST':
        hammadde_bilgileri = {isim: request.form.get(isim) for isim in isimler}
        for key,values in hammadde_bilgileri.items():
            if not hammadde_bilgileri[key]:
                hammadde_bilgileri[key] = None
                  
        yeni_hammadde = Hammaddeler(isim=hammadde_bilgileri["hammaddeisimekle"], 
                                 tur=hammadde_bilgileri["hammaddetürüekle"],
                                 birim=hammadde_bilgileri["hammaddebirimekle"], 
                                 miktar=hammadde_bilgileri["hammaddemiktarekle"],
                                 fiyat=hammadde_bilgileri["hammaddefiyatekle"],
                                 marka=hammadde_bilgileri["hammaddemarkaekle"],
                                 alinma_tarihi=datetime.strptime(hammadde_bilgileri["hammaddealinmatarihiekle"], '%Y-%m-%d'),
                                 aciklama=hammadde_bilgileri["hammaddenotekle"])
        db.session.add(yeni_hammadde)
        db.session.commit()
        flash('Malzeme Veritabanına Eklenmiştir', 'success')
        return redirect(url_for("main.hammadde"))
    else:
        flash('Malzeme Verileri Eklenemedi', 'danger')
        return redirect(url_for("main.hammadde"))
    
# * Hammadde Sil

@main.route('/hammadde/sil/<int:hammadde_id>/')
def hammadde_sil(hammadde_id):
    tarif_malzeme = TarifMalzeme.query.filter(TarifMalzeme.hammadde_id == hammadde_id).first()
    urun_malzeme = UrunMalzeme.query.filter(UrunMalzeme.hammadde_id == hammadde_id).first()
    if not tarif_malzeme:
        if not urun_malzeme:
            hammadde = Hammaddeler.query.filter(Hammaddeler.id == hammadde_id).first()
            db.session.delete(hammadde)
            db.session.commit()
            flash('Seçilen Malzeme Veritabanından Silinmiştir', 'success')
            return redirect(url_for("main.hammadde"))
        else:
            flash('Seçilen Malzeme Üründe Kullanılmıştır. Silinemez', 'warning')
            return redirect(url_for("main.hammadde"))
    else:
        flash('Seçilen Malzeme Tarifte Kullanılmıştır. Silinemez', 'warning')
        return redirect(url_for("main.hammadde"))

# * Hammadde Güncelle

@main.route('/hammadde/guncelle/<int:hammadde_id>/', methods=['POST', 'GET'])
def hammadde_guncelle(hammadde_id):
    isimler = ["hammaddeisimguncelle", "hammaddemiktarguncelle", "hammaddebirimguncelle", "hammaddefiyatguncelle",
               "hammaddemarkaguncelle", "hammaddeturguncelle", "hammaddealinmatarihiguncelle", "hammaddenotguncelle"]
    if request.method == 'POST':
        hammadde_bilgileri = {isim: request.form.get(isim) for isim in isimler}
        hammadde = Hammaddeler.query.filter(Hammaddeler.id == hammadde_id).first()
        hammadde.isim = hammadde_bilgileri["hammaddeisimguncelle"]
        hammadde.miktar = hammadde_bilgileri["hammaddemiktarguncelle"]
        hammadde.birim = hammadde_bilgileri["hammaddebirimguncelle"]
        hammadde.fiyat = hammadde_bilgileri["hammaddefiyatguncelle"]
        hammadde.marka = hammadde_bilgileri["hammaddemarkaguncelle"]
        hammadde.tur = hammadde_bilgileri["hammaddeturguncelle"]
        hammadde.alinma_tarihi = datetime.strptime(hammadde_bilgileri["hammaddealinmatarihiguncelle"], '%Y-%m-%d')
        hammadde.aciklama = hammadde_bilgileri["hammaddenotguncelle"]
        db.session.commit()
        flash('Malzeme Verileri Güncellenmiştir.', 'success')
        return redirect(url_for("main.hammadde"))
    else:
        flash('Malzeme Verileri Güncellenemedi', 'danger')
        return redirect(url_for("main.hammadde"))

#  ! ///////////////////////////////////////////////////////////////
# * TARİFLER SAYFASI

@main.route('/tarifler')
@login_required
def tarifler():
    tarifler = Tarifler.query.all()
    return render_template("tarifler.html", tarifler=tarifler)

# * Tarif Ekle 

@main.route('/tarif/ekle/', methods=['POST', 'GET'])
def tarif_ekle():
    isimler = ["tarifisimekle", "tarifnotekle"]
    if request.method == 'POST':
        tarif_bilgileri = {isim: request.form.get(isim) for isim in isimler}
        for key,values in tarif_bilgileri.items():
            if not tarif_bilgileri[key]:
                tarif_bilgileri[key] = None
                  
        yeni_tarif = Tarifler(isim=tarif_bilgileri["tarifisimekle"], aciklama=tarif_bilgileri["tarifnotekle"])
        db.session.add(yeni_tarif)
        db.session.commit()
        flash('Tarif Veritabanına Eklenmiştir', 'success')
        return redirect(url_for("main.tarifler"))
    else:
        flash('Tarif Verileri Eklenemedi', 'danger')
        return redirect(url_for("main.tarifler"))

# * Tarif Güncelle

@main.route('/tarif/guncelle/<int:tarif_id>/', methods=['POST', 'GET'])
def tarif_guncelle(tarif_id):
    isimler = ["tarifisimguncelle", "tarifnotguncelle"]
    if request.method == 'POST':
        tarif_bilgileri = {isim: request.form.get(isim) for isim in isimler}
        tarif = Tarifler.query.filter(Tarifler.id == tarif_id).first()
        tarif.isim = tarif_bilgileri["tarifisimguncelle"]
        tarif.aciklama = tarif_bilgileri["tarifnotguncelle"]
        db.session.commit()
        flash('Tarif Verileri Güncellenmiştir.', 'success')
        return redirect(url_for("main.tarifler"))
    else:
        flash('Tarif Verileri Güncellenemedi', 'danger')
        return redirect(url_for("main.tarifler"))
    
# * Tarif Sil

@main.route('/tarif/sil/<int:tarif_id>/')
def tarif_sil(tarif_id):
    tarif_urun = UrunTarif.query.filter(UrunTarif.tarif_id == tarif_id).first()
    if not tarif_urun:
        TarifMalzeme.query.filter(TarifMalzeme.tarif_id == tarif_id).delete()
        tarif = Tarifler.query.filter(Tarifler.id == tarif_id).first()
        db.session.delete(tarif)
        db.session.commit()
        flash('Seçilen Tarif Veritabanından Silinmiştir', 'success')
        return redirect(url_for("main.tarifler"))
    else:
        flash('Seçilen Tarif Üründe Kullanılmaktadır. Silinemez', 'warning')
        return redirect(url_for("main.tarifler"))

# * Tarif Mazlemeleri Getir

@main.route('/tarif/malzemeler/<int:tarif_id>/')
def malzeme_getir(tarif_id):
    tarifler = Tarifler.query.all()   
    tarif = Tarifler.query.filter(Tarifler.id == tarif_id).first()
    malzemeler = tarif.malzemeler
    hammadde = Hammaddeler.query.filter(Hammaddeler.tur == "Gıda").all()
    kilavuz = {1:1}
    db.session.commit()
    return render_template("tarifler.html", malzemeler = malzemeler, tarifler=tarifler, 
                           tum_malzemeler = hammadde, kilavuz=kilavuz, tarif_id = tarif_id, tarif_ismi = tarif.isim)

# * Tarif Malzemeleri Ekle

@main.route('/tarif/malzemeler/ekle/<int:tarif_id>/', methods=['POST', 'GET'])
def tarif_malzeme_ekle(tarif_id):
    isimler = ["tarifmalzemeekle", "tarifmalzememiktarekle", "tarifmalzemebirimekle"]
    if request.method == 'POST':
        tarif_malzeme_bilgileri = {isim: request.form.get(isim) for isim in isimler}  
        hammadde = Hammaddeler.query.filter(Hammaddeler.id == tarif_malzeme_bilgileri["tarifmalzemeekle"]).first()
        yeni_tarif_malzeme = TarifMalzeme(tarif_id=tarif_id, hammadde_id=tarif_malzeme_bilgileri["tarifmalzemeekle"], 
                                        hammadde_miktari=tarif_malzeme_bilgileri["tarifmalzememiktarekle"], 
                                        hammadde_birimi=hammadde.birim)
        db.session.add(yeni_tarif_malzeme)       
        db.session.commit()
        flash('Tarif Malzeme Verileri Eklenmiştir', 'success')
        return redirect(url_for("main.malzeme_getir", tarif_id=tarif_id))
    else:
        flash('Tarif Malzeme Verileri Eklenememiştir.', 'danger')
        return redirect(url_for("main.malzeme_getir", tarif_id=tarif_id))
    
# * Tarif Mazlemeleri Sil

@main.route('/tarif/malzemeler/sil/<int:tarif_malzeme_id>/<int:tarif_id>/')
def tarif_malzeme_sil(tarif_malzeme_id, tarif_id):
    silinecek = TarifMalzeme.query.filter(TarifMalzeme.id == tarif_malzeme_id).first()
    db.session.delete(silinecek)
    db.session.commit()
    flash('Seçilen Tarif Malzemesi Veritabanından Silinmiştir', 'success')
    return redirect(url_for("main.malzeme_getir", tarif_id=tarif_id))

# * Tarif Mazlemeleri Güncelle
@main.route('/tarif/malzemeler/guncelle/<int:tarif_malzeme_id>/<int:tarif_id>/', methods=['POST', 'GET'])
def tarif_malzeme_guncelle(tarif_malzeme_id, tarif_id):
    isimler = ["tarifmalzememiktarguncelle", "tarifmalzemebirimguncelle"]
    if request.method == 'POST':
        tarif_malzeme_bilgileri = {isim: request.form.get(isim) for isim in isimler}
        tarifmalzeme = TarifMalzeme.query.filter(TarifMalzeme.id == tarif_malzeme_id).first()
        tarifmalzeme.hammadde_miktari = tarif_malzeme_bilgileri["tarifmalzememiktarguncelle"]
        tarifmalzeme.hammadde_birimi = tarif_malzeme_bilgileri["tarifmalzemebirimguncelle"]       
        db.session.commit()
        flash('Tarif Malzemesi Verileri Güncellenmiştir.', 'success')
        return redirect(url_for("main.malzeme_getir", tarif_id=tarif_id))
    else:
        flash('Tarif malzemesi Verileri Güncellenemedi', 'danger')
        return redirect(url_for("main.malzeme_getir", tarif_id=tarif_id))

#  ! ///////////////////////////////////////////////////////////////
# * ÜRÜNLER SAYFASI

@main.route('/urunler')
@login_required
def urunler():
    urunler = Urunler.query.all()
    return render_template("urunler.html", urunler=urunler)

# * Ürün Ekle 

@main.route('/urun/ekle/', methods=['POST', 'GET'])
def urun_ekle():
    isimler = ["urunisimekle", "urunboyutekle", "urunnotekle"]
    if request.method == 'POST':
        urun_bilgileri = {isim: request.form.get(isim) for isim in isimler}
        for key,values in urun_bilgileri.items():
            if not urun_bilgileri[key]:
                urun_bilgileri[key] = None              
        yeni_urun = Urunler(isim=urun_bilgileri["urunisimekle"], 
                             boyut=urun_bilgileri["urunboyutekle"], 
                             aciklama=urun_bilgileri["urunnotekle"])
        db.session.add(yeni_urun)
        db.session.commit()
        flash('Ürün Veritabanına Eklenmiştir', 'success')
        return redirect(url_for("main.urunler"))
    else:
        flash('Ürün Verileri Eklenemedi', 'danger')
        return redirect(url_for("main.urunler"))
    
# * Ürün Güncelle

@main.route('/urun/guncelle/<int:urun_id>/', methods=['POST', 'GET'])
def urun_guncelle(urun_id):
    isimler = ["urunisimguncelle","urunboyutguncelle", "urunnotguncelle"]
    if request.method == 'POST':
        urun_bilgileri = {isim: request.form.get(isim) for isim in isimler}
        urun = Urunler.query.filter(Urunler.id == urun_id).first()
        urun.isim = urun_bilgileri["urunisimguncelle"]
        urun.boyut = urun_bilgileri["urunboyutguncelle"]
        urun.aciklama = urun_bilgileri["urunnotguncelle"]
        db.session.commit()
        flash('Ürün Verileri Güncellenmiştir.', 'success')
        return redirect(url_for("main.icerik_getir", urun_id=urun_id))
    else:
        flash('Ürün Verileri Güncellenemedi', 'danger')
        return redirect(url_for("main.icerik_getir", urun_id=urun_id))

# * Ürün Sil

@main.route('/urun/sil/<int:urun_id>/')
def urun_sil(urun_id):
    siparis_urun = SiparisUrun.query.filter(SiparisUrun.urun_id == urun_id).first()
    if not siparis_urun:
        UrunTarif.query.filter(UrunTarif.urun_id == urun_id).delete()
        db.session.commit()
        UrunMalzeme.query.filter(UrunMalzeme.urun_id == urun_id).delete()
        db.session.commit()
        urun = Urunler.query.filter(Urunler.id == urun_id).first()
        db.session.delete(urun)
        db.session.commit()
        flash('Seçilen Ürün Veritabanından Silinmiştir', 'success')
        return redirect(url_for("main.urunler"))
    else:
        flash('Seçilen Ürün Siparişe Bağlanmıştır. Silinemez', 'warning')
        return redirect(url_for("main.urunler"))

# * İçerik Getir

@main.route('/urun/icerik/<int:urun_id>/')
def icerik_getir(urun_id):
    urunler = Urunler.query.all()
    hammaddeler = Hammaddeler.query.all()
    tarifler = Tarifler.query.all() 
    urun = Urunler.query.filter(Urunler.id == urun_id).first()
    urun_hammaddeler = urun.hammaddeler
    urun_tarifler = urun.tarifler
    kilavuz = {1:1}
    return render_template("urunler.html", kilavuz=kilavuz, urunler=urunler, hammaddeler=hammaddeler, urun_id=urun_id, urun_ismi=urun.isim,
                           urun_boyutu=urun.boyut, tarifler = tarifler, urun_hammaddeler=urun_hammaddeler, urun_tarifler=urun_tarifler)

# * Ürün Hammadde Ekle

@main.route('/urun/malzemeler/ekle/<int:urun_id>/', methods=['POST', 'GET'])
def urun_malzeme_ekle(urun_id):
    isimler = ["urunmalzemeekle", "urunmalzememiktarekle", "urunmalzemebirimekle"]
    if request.method == 'POST':
        urun_malzeme_bilgileri = {isim: request.form.get(isim) for isim in isimler}
        hammadde = Hammaddeler.query.filter(Hammaddeler.id == urun_malzeme_bilgileri["urunmalzemeekle"]).first()
        yeni_urun_malzeme = UrunMalzeme(urun_id=urun_id, hammadde_id=urun_malzeme_bilgileri["urunmalzemeekle"], 
                                        hammadde_miktari=urun_malzeme_bilgileri["urunmalzememiktarekle"], 
                                        hammadde_birimi=hammadde.birim)
        db.session.add(yeni_urun_malzeme)       
        db.session.commit()
        flash('Ürün Malzeme Verileri Eklenmiştir', 'success')
        return redirect(url_for("main.icerik_getir", urun_id=urun_id))
    else:
        flash('Ürün Malzeme Verileri Eklenememiştir.', 'danger')
        return redirect(url_for("main.icerik_getir", urun_id=urun_id))
    
# * Ürün Hammadde Güncelle

@main.route('/urun/malzemeler/guncelle/<int:urun_hammadde_id>/<int:urun_id>/', methods=['POST', 'GET'])
def urun_hammadde_guncelle(urun_hammadde_id, urun_id):
    isimler = ["urunhammaddemiktarguncelle", "urunhammaddebirimguncelle"]
    if request.method == 'POST':
        urun_hammadde_bilgileri = {isim: request.form.get(isim) for isim in isimler}
        urunhammadde = UrunMalzeme.query.filter(UrunMalzeme.id == urun_hammadde_id).first()
        urunhammadde.hammadde_miktari = urun_hammadde_bilgileri["urunhammaddemiktarguncelle"]
        urunhammadde.hammadde_birimi = urun_hammadde_bilgileri["urunhammaddebirimguncelle"]       
        db.session.commit()
        flash('Ürüm Malzeme Verileri Güncellenmiştir.', 'success')
        return redirect(url_for("main.icerik_getir", urun_id=urun_id))
    else:
        flash('Ürüm Malzeme Verileri Güncellenemedi', 'danger')
        return redirect(url_for("main.icerik_getir", urun_id=urun_id))

# * Ürün Hammadde Sil

@main.route('/urun/malzemeler/sil/<int:urun_hammadde_id>/<int:urun_id>/')
def urun_hammadde_sil(urun_hammadde_id, urun_id):
    silinecek = UrunMalzeme.query.filter(UrunMalzeme.id == urun_hammadde_id).first()
    db.session.delete(silinecek)
    db.session.commit()
    flash('Seçilen Ürün Malzemesi Veritabanından Silinmiştir', 'success')
    return redirect(url_for("main.icerik_getir", urun_id=urun_id))
    
# * Ürün Tarif Ekle

@main.route('/urun/tarifler/ekle/<int:urun_id>/', methods=['POST', 'GET'])
def urun_tarif_ekle(urun_id):
    isimler = ["uruntarifekle", "uruntarifmiktarekle", "uruntarifbirimekle"]
    if request.method == 'POST':
        urun_tarif_bilgileri = {isim: request.form.get(isim) for isim in isimler}
        yeni_urun_tarif= UrunTarif(urun_id=urun_id, tarif_id=urun_tarif_bilgileri["uruntarifekle"], 
                                        tarif_miktari=urun_tarif_bilgileri["uruntarifmiktarekle"], 
                                        tarif_birimi=urun_tarif_bilgileri["uruntarifbirimekle"])
        db.session.add(yeni_urun_tarif)       
        db.session.commit()
        flash('Ürün Tarif Verileri Eklenmiştir', 'success')
        return redirect(url_for("main.icerik_getir", urun_id=urun_id))
    else:
        flash('Ürün Tarif Verileri Eklenememiştir.', 'danger')
        return redirect(url_for("main.icerik_getir", urun_id=urun_id))
 
# * Ürün Tarif Güncelle 
 
@main.route('/urun/tarifler/guncelle/<int:urun_tarif_id>/<int:urun_id>/', methods=['POST', 'GET'])
def urun_tarif_guncelle(urun_tarif_id, urun_id):
    isimler = ["uruntarifmiktarguncelle", "uruntarifbirimguncelle"]
    if request.method == 'POST':
        urun_tarif_bilgileri = {isim: request.form.get(isim) for isim in isimler}
        uruntarif = UrunTarif.query.filter(UrunTarif.id == urun_tarif_id).first()
        uruntarif.tarif_miktari = urun_tarif_bilgileri["uruntarifmiktarguncelle"]
        uruntarif.tarif_birimi = urun_tarif_bilgileri["uruntarifbirimguncelle"]       
        db.session.commit()
        flash('Ürüm Tarif Verileri Güncellenmiştir.', 'success')
        return redirect(url_for("main.icerik_getir", urun_id=urun_id))
    else:
        flash('Ürüm Tarif Verileri Güncellenemedi', 'danger')
        return redirect(url_for("main.icerik_getir", urun_id=urun_id))
    
# * Ürün Tarif Sil

@main.route('/urun/tarifler/sil/<int:urun_tarif_id>/<int:urun_id>/')
def urun_tarif_sil(urun_tarif_id, urun_id):
    silinecek = UrunTarif.query.filter(UrunTarif.id == urun_tarif_id).first()
    db.session.delete(silinecek)
    db.session.commit()
    flash('Seçilen Ürün Tarifi Veritabanından Silinmiştir', 'success')
    return redirect(url_for("main.icerik_getir", urun_id=urun_id))

#  ! ///////////////////////////////////////////////////////////////
# * SİPARİŞLER SAYFASI

@main.route('/Siparisler')
@login_required
def siparisler():
    siparisler = Siparisler.query.all()
    urunler = Urunler.query.all()
    musteriler = Musteriler.query.all()
    return render_template("siparisler.html", siparisler=siparisler, urunler=urunler, musteriler=musteriler)



# * Sipariş Ekle
    
@main.route('/siparis/ekle/', methods=['POST', 'GET'])
def siparis_ekle():
    isimler = ["siparismusteriekle", "siparisurunekle", "siparistarihiekle", "siparisturekle",
               "siparistutarekle", "siparismodelekle", "siparisnotekle"]
    if request.method == 'POST':
        siparis_bilgileri = {isim: request.form.get(isim) for isim in isimler}
        for key,values in siparis_bilgileri.items():
            if not siparis_bilgileri[key]:
                siparis_bilgileri[key] = None                 
        yeni_siparis = Siparisler(tarih=datetime.strptime(siparis_bilgileri["siparistarihiekle"], '%Y-%m-%d'), 
                                tur=siparis_bilgileri["siparisturekle"],
                                model=siparis_bilgileri["siparismodelekle"],
                                tutar=siparis_bilgileri["siparistutarekle"], 
                                aciklama=siparis_bilgileri["siparisnotekle"],
                                maliyet = 0)
        db.session.add(yeni_siparis)
        db.session.commit()
        son_siparis = Siparisler.query.order_by(Siparisler.id.desc()).first()
        yeni_musteri_siparisi = MusteriSiparis(musteri_id=siparis_bilgileri["siparismusteriekle"],siparis_id=son_siparis.id)
        db.session.add(yeni_musteri_siparisi)
        yeni_siparis_urun = SiparisUrun(urun_id=siparis_bilgileri["siparisurunekle"],siparis_id=son_siparis.id)
        db.session.add(yeni_siparis_urun)
        db.session.commit()
        siparis_maliyeti_gir(son_siparis.id)               
        flash('Sipariş Veritabanına Eklenmiştir', 'success')
        return redirect(url_for("main.siparisler"))
    else:
        flash('Sipariş Verileri Eklenemedi', 'danger')
        return redirect(url_for("main.siparisler"))

# * Sipariş Sil

@main.route('/siparis/sil/<int:siparis_id>/')
def siparis_sil(siparis_id):
    SiparisUrun.query.filter(SiparisUrun.siparis_id == siparis_id).delete()
    db.session.commit()
    MusteriSiparis.query.filter(MusteriSiparis.siparis_id == siparis_id).delete()
    db.session.commit()
    siparis = Siparisler.query.filter(Siparisler.id == siparis_id).first()
    db.session.delete(siparis)
    db.session.commit()
    flash('Seçilen Sipariş Veritabanından Silinmiştir', 'success')
    return redirect(url_for("main.siparisler"))

# * Sipariş Güncelle

@main.route('/siparis/guncelle/<int:siparis_id>/', methods=['POST', 'GET'])
def siparis_guncelle(siparis_id):
    isimler = ["siparistarihiguncelle", "siparisfiyatguncelle", "siparisturguncelle", "siparismodelguncelle",
               "siparisnotguncelle"]
    if request.method == 'POST':
        siparis_bilgileri = {isim: request.form.get(isim) for isim in isimler}
        siparis = Siparisler.query.filter(Siparisler.id == siparis_id).first()
        siparis.tarih = datetime.strptime(siparis_bilgileri["siparistarihiguncelle"], '%Y-%m-%d')
        siparis.tutar = siparis_bilgileri["siparisfiyatguncelle"]
        siparis.tur = siparis_bilgileri["siparisturguncelle"]
        siparis.model = siparis_bilgileri["siparismodelguncelle"]
        siparis.aciklama = siparis_bilgileri["siparisnotguncelle"]
        db.session.commit()
        flash('Sipariş Verileri Güncellenmiştir.', 'success')
        return redirect(url_for("main.siparisler"))
    else:
        flash('Sipariş Verileri Güncellenemedi', 'danger')
        return redirect(url_for("main.siparisler"))


# * Sipariş Ürün Ekle

@main.route('/siparis/urun/ekle/<int:siparis_id>/', methods=['POST', 'GET'])
def siparis_urun_ekle(siparis_id):
    if request.method == 'POST':
        urun_id = request.form.get("siparisekurunekle")
        yeni_siparis_urun = SiparisUrun(urun_id = urun_id, siparis_id = siparis_id)
        db.session.add(yeni_siparis_urun)
        db.session.commit()
        siparis_maliyeti_gir(siparis_id) 
        flash('Siparişe Ürün Eklendi', 'success')
        return redirect(url_for("main.siparisler"))
    else:
        flash('Siparişe Ürün Eklenemedi', 'danger')
        return redirect(url_for("main.siparisler"))


# * Sipariş Ürün Sil

@main.route('/siparis/urun/sil/<int:siparis_id>/', methods=['POST', 'GET'])
def siparis_urun_sil(siparis_id):
    if request.method == 'POST':
        urun_id = request.form.get("siparisuruncikar")
        urun_siparis = SiparisUrun.query.filter(SiparisUrun.siparis_id == siparis_id) \
                                        .filter(SiparisUrun.urun_id == urun_id).first()                      
        db.session.delete(urun_siparis)
        db.session.commit()
        siparis_maliyeti_gir(siparis_id) 
        flash('Siparişten Ürün Silindi', 'success')
        return redirect(url_for("main.siparisler"))
    else:
        flash('Siparişten Ürün Silinemedi', 'danger')
        return redirect(url_for("main.siparisler"))

#  ! ///////////////////////////////////////////////////////////////
# * MÜŞTERİLER SAYFASI

@main.route('/Musteriler')
@login_required
def musteriler():
    musteriler = Musteriler.query.all()
    return render_template("musteriler.html", musteriler=musteriler)

# * Müşteri Ekle

@main.route('/musteri/ekle/', methods=['POST', 'GET'])
def musteri_ekle():
    isimler = ["musteriisimekle", "musterisoyisimekle", "musteritelefonekle", "musterinotekle"]
    if request.method == 'POST':
        musteri_bilgileri = {isim: request.form.get(isim) for isim in isimler}
        for key,values in musteri_bilgileri.items():
            if not musteri_bilgileri[key]:
                musteri_bilgileri[key] = None           
        yeni_musteri = Musteriler(isim=musteri_bilgileri["musteriisimekle"], 
                                 soyisim=musteri_bilgileri["musterisoyisimekle"],
                                 telefon=musteri_bilgileri["musteritelefonekle"], 
                                 aciklama=musteri_bilgileri["musterinotekle"])
        db.session.add(yeni_musteri)
        db.session.commit()
        flash('Müşteri Veritabanına Eklenmiştir', 'success')
        return redirect(url_for("main.musteriler"))
    else:
        flash('Müşteri Verileri Eklenemedi', 'danger')
        return redirect(url_for("main.musteriler"))
    
# * Müşteri Sil

@main.route('/musteri/sil/<int:musteri_id>/')
def musteri_sil(musteri_id):
    musteri = Musteriler.query.filter(Musteriler.id == musteri_id).first()
    if not musteri.siparisler:
        db.session.delete(musteri)
        db.session.commit()
        flash('Seçilen Müşteri Veritabanından Silinmiştir', 'success')
        return redirect(url_for("main.musteriler"))
    else:
        flash('Seçilen Müşterinin Siparişleri Vardır. Silinemez', 'warning')
        return redirect(url_for("main.musteriler"))

# * Müşteri Güncelle

@main.route('/musteri/guncelle/<int:musteri_id>/', methods=['POST', 'GET'])
def musteri_guncelle(musteri_id):
    isimler = ["musteriisimguncelle", "musterisoyisimguncelle", "musteritelefonguncelle", "musterinotguncelle"]
    if request.method == 'POST':
        musteri_bilgileri = {isim: request.form.get(isim) for isim in isimler}
        musteri = Musteriler.query.filter(Musteriler.id == musteri_id).first()
        musteri.isim = musteri_bilgileri["musteriisimguncelle"]
        musteri.soyisim = musteri_bilgileri["musterisoyisimguncelle"]
        musteri.telefon = musteri_bilgileri["musteritelefonguncelle"]
        musteri.aciklama = musteri_bilgileri["musterinotguncelle"]
        db.session.commit()
        flash('Musteri Verileri Güncellenmiştir.', 'success')
        return redirect(url_for("main.musteriler"))
    else:
        flash('Musteri Verileri Güncellenemedi', 'danger')
        return redirect(url_for("main.musteriler"))
    
    
#  ! ///////////////////////////////////////////////////////////////
# * İSTATİSTİK SAYFASI

@main.route('/Rakamlar/', defaults={'sure': "6 Ay"})
@main.route('/Rakamlar/<string:sure>')
@login_required
def rakamlar(sure):
    bugun = datetime.now().date()
    return render_template("rakamlar.html", sure=sure, istatistikler = istatistikler(bugun,sure))

@main.route('/Rakamlar/getir/', methods=['POST', 'GET'])
def rakamlari_getir():
    if request.method == 'POST':
        sure = request.form.get("suregir")
        return redirect(url_for("main.rakamlar", sure=sure))
    
#  ! ///////////////////////////////////////////////////////////////
# * NOTLAR SAYFASI

@main.route('/Notlar')
@login_required
def notlar():
    kisisel_notlar = Notlar.query.filter(Notlar.durum == 0).all()
    is_notlari = Notlar2.query.filter(Notlar2.durum == 0).all()
    return render_template("notlar.html",kisisel_notlar=kisisel_notlar,is_notlari=is_notlari)

@main.route('/not-ekle', methods=["POST", "GET"])
def not_ekle():
    if request.method == 'POST':
        konu = request.form.get("not_konu_ekle")
        icerik = request.form.get("not_icerik_ekle")
        tarih = request.form.get("not_tarih_ekle")
        new_not = Notlar(konu=konu, icerik=icerik,
                         tarih=datetime.strptime(tarih, '%Y-%m-%d'), durum=0)
        db.session.add(new_not)
        db.session.commit()
        return redirect(url_for("main.notlar"))
    else:
        flash('Bağlantı Kurulamadı', 'danger')
        return redirect(url_for("main.notlar"))


@main.route('/not-sil/<int:not_id>')
def not_sil(not_id):
    noti = Notlar.query.filter(Notlar.id == not_id).first()
    db.session.delete(noti)
    db.session.commit()
    return redirect(url_for("main.notlar"))


@main.route('/not-tamamla/<int:not_id>')
def not_tamamlama(not_id):
    noti = Notlar.query.filter(Notlar.id == not_id).first()
    noti.durum = 1
    db.session.commit()
    return redirect(url_for("main.notlar"))


@main.route('/not-ekle2', methods=["POST", "GET"])
def not_ekle2():
    if request.method == 'POST':
        konu = request.form.get("not_konu_ekle")
        icerik = request.form.get("not_icerik_ekle")
        tarih = request.form.get("not_tarih_ekle")
        new_not = Notlar2(konu=konu, icerik=icerik,
                          tarih=datetime.strptime(tarih, '%Y-%m-%d'), durum=0)
        db.session.add(new_not)
        db.session.commit()
        return redirect(url_for("main.notlar"))
    else:
        flash('Bağlantı Kurulamadı', 'danger')
        return redirect(url_for("main.notlar"))


@main.route('/not-sil2/<int:not_id>')
def not_sil2(not_id):
    noti = Notlar2.query.filter(Notlar2.id == not_id).first()
    db.session.delete(noti)
    db.session.commit()
    return redirect(url_for("main.notlar"))


@main.route('/not-tamamla2/<int:not_id>')
def not_tamamlama2(not_id):
    noti = Notlar2.query.filter(Notlar2.id == not_id).first()
    noti.durum = 1
    db.session.commit()
    return redirect(url_for("main.notlar"))

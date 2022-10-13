from p_p.extensions import db

class Musteriler(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    isim = db.Column(db.String(50), nullable=False)  
    soyisim = db.Column(db.String(30)) 
    siparisler = db.relationship("MusteriSiparis", back_populates="musteri")
    telefon = db.Column(db.Integer) 
    odeme = db.Column(db.String(20)) 
    aciklama = db.Column(db.String(100))
    
class MusteriSiparis(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    musteri_id = db.Column(db.Integer, db.ForeignKey("musteriler.id"))
    siparis_id = db.Column(db.Integer, db.ForeignKey("siparisler.id"))
    siparisler = db.relationship("Siparisler", back_populates="musteri")
    musteri = db.relationship("Musteriler", back_populates="siparisler")

class Siparisler(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    tarih = db.Column(db.Date, nullable=False)
    urunler = db.relationship("SiparisUrun")
    musteri = db.relationship("MusteriSiparis", back_populates="siparisler")
    tur = db.Column(db.String(30))
    model = db.Column(db.String(30))
    tutar = db.Column(db.Float)
    maliyet = db.Column(db.Float)
    aciklama = db.Column(db.String(100))
    
class SiparisUrun(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    siparis_id = db.Column(db.Integer, db.ForeignKey("siparisler.id")) 
    urun_id = db.Column(db.Integer, db.ForeignKey("urunler.id"))
    urun = db.relationship("Urunler")
    
class Urunler(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    isim = db.Column(db.String(50), nullable=False)
    tarifler = db.relationship("UrunTarif")
    hammaddeler = db.relationship("UrunMalzeme")
    boyut = db.Column(db.String(20))
    aciklama = db.Column(db.String(100))
    siparis_sayisi = db.Column(db.Integer)

class UrunTarif(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    urun_id = db.Column(db.Integer, db.ForeignKey("urunler.id"))
    tarif_id = db.Column(db.Integer, db.ForeignKey("tarifler.id"))
    tarif = db.relationship("Tarifler")
    tarif_miktari = db.Column(db.Float)
    tarif_birimi = db.Column(db.String(30))
    
class UrunMalzeme(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True) 
    urun_id = db.Column(db.Integer, db.ForeignKey("urunler.id"))
    hammadde_id = db.Column(db.Integer, db.ForeignKey("hammaddeler.id"))
    hammadde = db.relationship("Hammaddeler")
    hammadde_miktari = db.Column(db.Float, nullable=False)
    hammadde_birimi = db.Column(db.String(30))

class Tarifler(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    isim = db.Column(db.String(50), nullable=False)
    malzemeler = db.relationship("TarifMalzeme")
    aciklama = db.Column(db.String(100))

class TarifMalzeme(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    tarif_id = db.Column(db.Integer, db.ForeignKey("tarifler.id"))
    hammadde_id = db.Column(db.Integer, db.ForeignKey("hammaddeler.id"))
    hammadde = db.relationship("Hammaddeler")
    hammadde_miktari = db.Column(db.Float, nullable=False)
    hammadde_birimi = db.Column(db.String(30))

class Hammaddeler(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    isim = db.Column(db.String(50), nullable=False)
    tur = db.Column(db.String(30), nullable=False)
    birim = db.Column(db.String(30), nullable=False)
    miktar = db.Column(db.Integer, nullable=False)
    fiyat = db.Column(db.Float, nullable=False)
    marka = db.Column(db.String(30))
    alinma_tarihi = db.Column(db.Date, nullable=False)
    aciklama = db.Column(db.String(100))   

class Notlar(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    konu = db.Column(db.String(25), nullable=False)
    icerik = db.Column(db.String(200))
    tarih = db.Column(db.Date, nullable=False)
    durum = db.Column(db.Integer, nullable=False)

class Notlar2(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    konu = db.Column(db.String(25), nullable=False)
    icerik = db.Column(db.String(200))
    tarih = db.Column(db.Date, nullable=False)
    durum = db.Column(db.Integer, nullable=False)

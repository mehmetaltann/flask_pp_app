from calendar import month
from datetime import datetime, timedelta
from ..models import Musteriler, Siparisler, Urunler
from ..extensions import db

def siparis_maliyeti_gir(siparis_id):
    siparis = Siparisler.query.filter(Siparisler.id == siparis_id).first()
    toplam_maliyet = 0
    for siparisurun in siparis.urunler:
        toplam_tarif_maliyeti = 0
        toplam_malzeme_maliyeti = 0
        for urun_tarif in siparisurun.urun.tarifler:
            for malzeme in urun_tarif.tarif.malzemeler:
                toplam_tarif_maliyeti +=  float(malzeme.hammadde.fiyat * malzeme.hammadde_miktari / malzeme.hammadde.miktar * urun_tarif.tarif_miktari)
        for malzeme in siparisurun.urun.hammaddeler:
            toplam_malzeme_maliyeti += float(malzeme.hammadde.fiyat * malzeme.hammadde_miktari / malzeme.hammadde.miktar)
        toplam_maliyet += (toplam_tarif_maliyeti + toplam_malzeme_maliyeti)
    siparis.maliyet = toplam_maliyet
    db.session.commit()
    
def tarih_getir(bugun):
    ay_donusum={'Jan': 'Ocak', 'Feb': 'Şubat', 'Mar': 'Mart', 'Apr': 'Nisan', 'May': 'Mayıs', 'Jun': 'Haziran',
                'Jul': 'Temmuz', 'Aug': 'Ağustos', 'Sep': 'Eylül', 'Oct': 'Ekim', 'Nov': 'Kasım', 'Dec': 'Aralık'}
    gun_donusum = {'Monday':"Pazartesi", 'Tuesday':"Salı", 'Wednesday':"Çarşamba", 
                'Thursday':"Perşembe", 'Friday':"Cuma", 'Saturday':"Cumartesi", 'Sunday':"Pazar"}
    haftabasi = bugun - timedelta(days=bugun.weekday())
    haftabasi_gun = haftabasi.strftime("%d")
    haftabasi_ay = haftabasi.strftime("%b")
    haftasonu = haftabasi + timedelta(days=6)
    haftasonu_gun = haftasonu.strftime("%d")
    haftasonu_ay = haftasonu.strftime("%b")
    yazi = f"{haftabasi_gun} {ay_donusum[haftabasi_ay]} - {haftasonu_gun} {ay_donusum[haftasonu_ay]}"
    yil = bugun.strftime("%Y")
    gun_adi_ingilizce = bugun.strftime("%A")
    gun_adi = gun_donusum[gun_adi_ingilizce]
    gun = bugun.strftime("%d")
    ay_adi_ingilizce = bugun.strftime("%b")
    ay = ay_donusum[ay_adi_ingilizce]
    tarih_bilgisi={"yil":yil,"gun":gun,"ay":ay,"gun_adi":gun_adi,"yazi":yazi}
    return tarih_bilgisi
 
def siparis_istatistikleri(bugun):
    
    def ayin_son_gunu(daynow):
        next_month = daynow.replace(day=28) + timedelta(days=4)
        return next_month - timedelta(days=next_month.day)
    
    def malzemeleri_getir(tarihli_siparisler):
        malzeme_miktar_listesi = {"Un":[0,"kg"],"Toz Şeker":[0,"kg"],"Tereyağ":[0,"kg"],"Yumurta":[0,"adet"],
                              "Süt":[0,"lt"],"Sıvıyağ":[0,"lt"],"Sütlü Çikolata":[0,"kg"],"Beyaz Çikolata":[0,"kg"],
                              "Bitter Çikolata":[0,"kg"],"Şeker Hamuru":[0,"kg"],"Krema":[0,"lt"]}
        for siparis in tarihli_siparisler:
            for siparisurun in siparis.urunler:
                for urun_tarif in siparisurun.urun.tarifler:
                    for malzeme in urun_tarif.tarif.malzemeler:
                        if malzeme.hammadde.isim in malzeme_miktar_listesi:
                            malzeme_miktar_listesi[malzeme.hammadde.isim][0] += float(malzeme.hammadde_miktari  * urun_tarif.tarif_miktari)
                        else:
                            pass
                for malzeme in siparisurun.urun.hammaddeler:
                    if malzeme.hammadde.isim in malzeme_miktar_listesi:
                        malzeme_miktar_listesi[malzeme.hammadde.isim][0] += float(malzeme.hammadde_miktari)
                    else:
                        pass
        return malzeme_miktar_listesi           

    dun = (datetime.now() - timedelta(days=1)).date()
    on_gun_once = (datetime.now() - timedelta(days=10)).date()
    bu_haftanin_ilk_gunu = bugun - timedelta(days=bugun.weekday())
    bu_haftanin_son_gunu = bu_haftanin_ilk_gunu + timedelta(days=6)
    bu_ayin_ilk_gunu = bugun.replace(day=1)
    bu_ayin_son_gunu = ayin_son_gunu(bugun)
    bu_yil = bugun.strftime("%Y")
    haftanin_siparisleri = Siparisler.query.filter(Siparisler.tarih.between(bu_haftanin_ilk_gunu, bu_haftanin_son_gunu)).all()
    ayin_siparisleri = Siparisler.query.filter(Siparisler.tarih.between(bu_ayin_ilk_gunu, bu_ayin_son_gunu)).all()
    yilin_siparisleri = Siparisler.query.filter(Siparisler.tarih.between(f"{bu_yil}-01-01", f"{bu_yil}-12-31")).all()
    gecen_on_gunun_siparisleri = Siparisler.query.filter(Siparisler.tarih.between(on_gun_once, dun)).all()
    haftanin_malzemeleri = malzemeleri_getir(haftanin_siparisleri)
    ayin_malzemeleri = malzemeleri_getir(ayin_siparisleri)
    yilin_malzemeleri = malzemeleri_getir(yilin_siparisleri)
    siparis_rakamlari = {"haftanin_siparisleri":haftanin_siparisleri,"ayin_siparisleri":ayin_siparisleri, "yilin_siparisleri":yilin_siparisleri,
                         "gecen_on_gunun_siparisleri":gecen_on_gunun_siparisleri,"haftanin_malzemeleri":haftanin_malzemeleri,"ayin_malzemeleri":ayin_malzemeleri,
                         "yilin_malzemeleri":yilin_malzemeleri}
    return siparis_rakamlari

def top10 (siparisler,musteriler):
    top10= []
    top10_siparis = {}
    top10_siparis_list=[]
    top10_model={}
    top10_model_list=[]
    top10_kullanim={}
    top10_kullanim_list=[]
    top10_musteri={}
    top10_musteri_list=[]
    for siparis in siparisler:
        if not siparis.tur in top10_kullanim:
            top10_kullanim[siparis.tur] = 1
        else:
            top10_kullanim[siparis.tur] += 1
        if not siparis.model in top10_model:
            top10_model[siparis.model] = 1
        else:
            top10_model[siparis.model] += 1
        for siparisurun in siparis.urunler:
            if not siparisurun.urun_id in top10_siparis:
                top10_siparis[siparisurun.urun_id] = 1
            else:
                top10_siparis[siparisurun.urun_id] += 1
    my_keys_kullanim = sorted(top10_kullanim, key=top10_kullanim.get, reverse=True)[:10]
    my_keys_model = sorted(top10_model, key=top10_model.get, reverse=True)[:10]
    my_keys_siparis = sorted(top10_siparis, key=top10_siparis.get, reverse=True)[:10]
    for key in my_keys_siparis:
        urun = Urunler.query.filter(Urunler.id == key).first()
        if urun.id in top10_siparis:
            urun.siparis_sayisi = top10_siparis[urun.id]
            top10_siparis_list.append(urun)
    for key in my_keys_model:
        siparis = Siparisler.query.filter(Siparisler.model == key).first()
        if key == siparis.model:
            siparis.aciklama = top10_model[siparis.model]
            top10_model_list.append(siparis)
    for key in my_keys_kullanim:
        siparis = Siparisler.query.filter(Siparisler.tur == key).first()
        if key == siparis.tur:
            siparis.maliyet = top10_kullanim[siparis.tur]
            top10_kullanim_list.append(siparis)
    for musteri in musteriler:
        top10_musteri[musteri.id] = len(musteri.siparisler)
    my_keys_musteri = sorted(top10_musteri, key=top10_musteri.get, reverse=True)[:10]
    for key in my_keys_musteri:
        musteri = Musteriler.query.filter(Musteriler.id == key).first()
        top10_musteri_list.append(musteri)
    top10 = [top10_musteri_list,top10_siparis_list,top10_model_list,top10_kullanim_list]
    return top10

def siparis_bilgileri (siparisler):
    siparis_bilgileri=[]
    for siparis in siparisler:
        for musterisiparis in siparis.musteri:
            siparis.ek1 = musterisiparis.musteri.isim +  "  " + musterisiparis.musteri.soyisim
        for siparisurun in siparis.urunler:
            siparis.ek2 = siparisurun.urun.isim + "   " + siparisurun.urun.boyut
        siparis_bilgileri.append(siparis)
    return siparis_bilgileri

def istatistikler (bugun,sure):
    from dateutil.relativedelta import relativedelta
    istatistikler = {"ay_sayisi": [],"siparis_sayisi":[],"siparis_tutari":[],
                     "siparis_maliyeti":[], "siparis_kari":[],"siparis_kar_oranı":[], 
                     "toplam_siparis_sayisi":0,"toplam_siparis_tutari":0,"toplam_siparis_maliyeti":0,
                     "toplam_siparis_kari":0,"ortalama_siparis_kari":0,"ortalama_siparis_kar_orani":0}  
      
    def siparis_istatistik (ay):
        
        istatistikler["ay_sayisi"] = [i for i in range(ay,0,-1)]
        for i in istatistikler["ay_sayisi"]:
            ilk_tarih = bugun - relativedelta(months=+i)
            siparisler = Siparisler.query.filter(Siparisler.tarih.between(ilk_tarih, (ilk_tarih + relativedelta(months=+1)))).all()
            istatistikler["siparis_sayisi"].append(len(siparisler))
            toplam_tutar = sum(siparis.tutar for siparis in siparisler)
            toplam_maliyet = sum(siparis.maliyet for siparis in siparisler)
            istatistikler["siparis_tutari"].append(toplam_tutar)
            istatistikler["siparis_maliyeti"].append(round(toplam_maliyet,2))
            istatistikler["siparis_kari"].append(round((toplam_tutar - toplam_maliyet),2))
            if not toplam_maliyet == 0:
                istatistikler["siparis_kar_oranı"].append(round(((toplam_tutar - toplam_maliyet)/toplam_tutar*100),2))
            else:
                istatistikler["siparis_kar_oranı"].append(0)
        istatistikler["toplam_siparis_sayisi"] = sum(istatistikler["siparis_sayisi"])
        istatistikler["toplam_siparis_tutari"] = sum(istatistikler["siparis_tutari"])
        istatistikler["toplam_siparis_maliyeti"] = sum(istatistikler["siparis_maliyeti"])
        istatistikler["toplam_siparis_kari"] = sum(istatistikler["siparis_kari"])
        istatistikler["ortalama_siparis_kari"] = sum(istatistikler["siparis_kari"]) / ay
        istatistikler["ortalama_siparis_kar_orani"] = round((sum(istatistikler["siparis_kar_oranı"]) / ay),2)

    if sure == "3 Ay":
        ay = 3
    elif sure == "6 Ay":
        ay = 6
    elif sure == "9 Ay":
        ay = 9
    elif sure == "1 Yıl":
        ay = 12
    elif sure == "2 Yıl":
        ay = 24
    elif sure == "3 Yıl":
        ay = 36
    else:
        ay=48
    
    siparis_istatistik(ay)
                
    return istatistikler
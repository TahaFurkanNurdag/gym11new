from flask import *
from datetime import datetime
from datetime import date
import sqlite3
import hashlib  # sifreleme icin
import os  # upload islemleri icin
# dosya upload işlemleri için dahil edildi
from werkzeug.utils import secure_filename
from datetime import date, timedelta
import calendar  # to check clients days
import shutil  # Backup lib

app = Flask(__name__)
app.secret_key = 'random string'
# upload edilecek fotograflarin dosya konumu belirlendi
UPLOAD_FOLDER = 'static/uploads'
# upload edilecek fotograflarin uzantilari belirlendi
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ERROR CODE 7
# SUCCESS CODE 8
# FAILURE CODE 9


class DatabaseName:
    databaseName = "database.db"


def getLoginDetails():
    with sqlite3.connect(DatabaseName.databaseName) as conn:
        cur = conn.cursor()
        try:
            if 'email' not in session:  # emaile gore giris yapildi mi? yapilmadiysa alttaki satilar
                girildiMi = False  # girilmedigi icin false
                adi = 'Giriş Yapılmadı'  # sitede isim goruntulenmeyec
                userId = '!'
            else:  # giris yapildiysa alttaki satirlar
                girildiMi = True  # giris yapildigi icin true
                cur.execute(
                    "SELECT userId, adi FROM kullanicilar WHERE email = ?", (session['email'], ))
                # yukaridaki sorgudan sirasiyla degiskenlere veri cekildi
                userId, adi = cur.fetchone()
        except Exception as e:
            print(e)
    conn.close()  # connection kapatildi
    return (userId, girildiMi, adi)  # fonksiyonun dondurdugu degiskenler


def is_valid(email, parola, adminMi):  # email ve parola dogru mu kiyasi
    con = sqlite3.connect(DatabaseName.databaseName)
    cur = con.cursor()
    cur.execute('SELECT email, parola, adminMi FROM kullanicilar')
    data = cur.fetchall()
    for row in data:
        if row[0] == email and row[1] == parola:
            adminMi = row[2]
            session['adminMi'] = adminMi
            return True
    return False


def allowed_file(filename):  # fotograf isimlerini duzenli hale getirmek icin
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def parse(data):  # urunleri listelememizde kullandigimiz fonksiyon. birden fazla ayni satir olmasin diye yazildi
    ans = []
    i = 0
    while i < len(data):
        curr = []
        for j in range(7):
            if i >= len(data):
                break
            curr.append(data[i])
            i += 1
        ans.append(curr)
    return ans


'''
@app.route("/changeDatabaseName")  # kategori ekleme sayfasi
def addcategory():
    if 'email' not in session:  # kisi admin degilse yapilacaklar
        adminMi = 0
        session['adminMi'] = adminMi
    if session['adminMi'] == 1:  # kisi adminse yapilacaklar
        girildiMi, adi = getLoginDetails()[1:]

        return redirect(url_for('changeDb'))
    else:
        return redirect(url_for('changeDb'))
'''
@app.route("/")
def root():
    if 'email' not in session:  # giris yapilmadiysa
        adminMi = 0  # admin mi degiskeni sifir olacak
        session['adminMi'] = adminMi  # bu session icine aktarilacak
    # yukarida olusturulan fonksiyondan degerler cekiliyor
    girildiMi, adi = getLoginDetails()[1:]  # userid gereksiz
    with sqlite3.connect(DatabaseName.databaseName) as conn:
        try:
            cur = conn.cursor()
            cur.execute("select adi, soyadi, dogumTarihi from kullanicilar")
            adsoyadgun = cur.fetchall()
            today = date.today()
            people = []
            for i in range(len(adsoyadgun)):
                if str(adsoyadgun[i][2]) == str(today):
                    people.append(adsoyadgun[i][0:2])
            people = str(people).replace("'","").replace(",","").replace("(","").replace("[","").replace("]","")[:-1].split(")")
        except Exception as e:
            print(e)
    conn.close()
    return render_template('root.html', data=people, girildiMi=girildiMi, adi=adi)


@app.route("/addcategory")  # kategori ekleme sayfasi
def addcategory():
    if 'email' not in session:  # kisi admin degilse yapilacaklar
        adminMi = 0
        session['adminMi'] = adminMi
    if session['adminMi'] == 1:  # kisi adminse yapilacaklar
        girildiMi, adi = getLoginDetails()[1:]
        with sqlite3.connect(DatabaseName.databaseName) as conn:
            try:
                cur = conn.cursor() 
                cur.execute("select * from pakettipi")
                tumPaketler = cur.fetchall()
                conn.commit()  # burada kategori veritabanina ekleniyor
            except Exception as e:
                print(e)
                conn.rollback()
        conn.close()
        return render_template('package_add.html',tumPaketler=tumPaketler, girildiMi=girildiMi, adi=adi)
    else:
        return render_template('ERROR.html', msg="You are not authorized. Error Code: 701")


# package_add.html icinden bu sayfa cagiriliyor
@app.route("/addcategoryitem", methods=["GET", "POST"])
def addcategoryitem():
    if request.method == "POST":
        paketadi = request.form['paketadi']
        paketfiyati = request.form['paketfiyati']
        paketgunu = request.form['paketgunu']
        paketsaati = request.form['paketsaati']
        paketaciklamasi = request.form['paketaciklamasi']
        with sqlite3.connect(DatabaseName.databaseName) as conn:
            try:
                cur = conn.cursor()
                cur.execute('''INSERT INTO pakettipi (paketadi,paketgunu,paketsaati,paketfiyati,paketaciklamasi) VALUES (?,?,?,?,?)''',(paketadi,paketgunu,paketsaati, paketfiyati, paketaciklamasi,))
                cur.execute('ALTER TABLE kullanicilar ADD '+paketadi +'GunSayisi  varchar(255) default 0')
                cur.execute('ALTER TABLE kullanicilar ADD '+paketadi +'DersSayisi  varchar(255) default 0')
                conn.commit()  # burada kategori veritabanina ekleniyor
                print("Success. Success Code: 801")
            except Exception as e:
                print(e)
                conn.rollback()
                return render_template('ERROR.html', msg="Local connection error. Error Code: 702")
        conn.close()
        return redirect(url_for('root'))
    else:
        return redirect(url_for('root'))


@app.route("/addcategoryCafe", methods=["GET", "POST"])
def addcategoryCafe():
    if request.method == "POST":
        nameOfProduct = request.form['nameOfProduct']
        stock = request.form['stock']
        with sqlite3.connect(DatabaseName.databaseName) as conn:
            try:
                cur = conn.cursor()
                cur.execute('''INSERT INTO cafeUrunleri (urunAdi,totalStok) VALUES (?,?)''',(nameOfProduct, stock))
                conn.commit()  # burada kategori veritabanina ekleniyor
                print("Success. Success Code: 801")
            except:
                conn.rollback()
                return render_template('ERROR.html', msg="Local connection error. Error Code: 702")
        conn.close()
        return redirect(url_for('addcategory'))
    else:
        return redirect(url_for('root'))

@app.route("/loginForm")  # giris sayfasi
def loginForm():
    if 'email' in session:  # kullanici giris yaptiysa anasayfa ekranina yonlendirir
        return redirect(url_for('root'))
    else:
        return render_template('login_page.html')


@app.route("/incomeForm")  # giris sayfasi
def incomeForm():
    if 'email' not in session:  # kisi admin degilse yapilacaklar
        adminMi = 0
        session['adminMi'] = adminMi
    else:  # kisi adminse yapilacaklar
        girildiMi, adi = getLoginDetails()[1:]
        return render_template('income_details.html',girildiMi=girildiMi, adi=adi)


# login_page.html sayfasindan cagirilir
@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        adminMi = 0
        session['adminMi'] = adminMi
        email = request.form['email']
        parola = request.form['parola']  # email ve parola htmlden alinir
        if is_valid(email, parola, adminMi):
            session['email'] = email
            # giris yapildiginda anasayfaya yonlendirme
            return redirect(url_for('root'))
        else:
            return render_template('ERROR.html', msg="Login failure. Error Code: 703")
    else:
        # url'ye login yazilirsa loginForm'a yonlendirme
        return redirect(url_for('loginForm'))


@app.route("/logout")  # cikis ekrani
def logout():
    if 'email' not in session:  # kisi eger giris yapmamissa anasayfaya yonlendirilir
        return redirect(url_for('root'))
    else:
        session.pop('email', None)  # giris yapan kisiyi hafizadan atma
        return redirect(url_for('root'))  # anasayfaya donus


@app.route("/register", methods=['GET', 'POST'])  # sign_up.html'den cagirilir
def register():
    if request.method == 'POST':
        parola = request.form['parola']
        email = request.form['email']
        adi = request.form['adi']
        soyadi = request.form['soyadi']
        adres1 = request.form['adres1']
        adres2 = request.form['adres2']
        # html'de doldurulan alanlar degiskenlere aktarildi
        tel = request.form['tel']
        boy = request.form['boy']
        kilo = request.form['kilo']
        kayitgunu = request.form['kayitgunu']
        ogretmenMi = request.form['ogretmenMi']
        aktifmi = request.form['aktifmi']
        arkadassayisi = request.form['arkadassayisi']
        kayitEdeninAdi = request.form['kayitEdeninAdi']
        hastalik = request.form['hastalik']
        dogumtarihi= request.form['dogumtarihi']


        if ogretmenMi =='Evet':
            ogretmenMi=1
        elif ogretmenMi=='Hayir':
            ogretmenMi=0

        if aktifmi =='Evet':
            aktifmi=1
        elif aktifmi=='Hayir':
            aktifmi=0


        with sqlite3.connect(DatabaseName.databaseName) as con:
            try:
                cur = con.cursor()
                cur.execute('INSERT INTO kullanicilar (parola, email, adi, soyadi,kayitEdeninAdi,hastalik,dogumtarihi, tel,boy,kilo, adres1, adres2,kayitgunu,aktifmi,katilim,arkadassayisi, ogretmenMi,adminMi) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,1,1)', (
                    parola, email, adi, soyadi,kayitEdeninAdi,hastalik,dogumtarihi,  tel, boy, kilo,adres1, adres2, kayitgunu, aktifmi, arkadassayisi, ogretmenMi))
                con.commit()  # veritabanina kaydedildi
                print("Success. Success Code: 802")
            except Exception as e:
                con.rollback()
                print(f"Failure. Failure Code: 901. Failure is {e}")
                return render_template("ERROR.html", msg="Insertion Failure. Error Code: 704")
        con.close()
        return redirect(url_for('root'))
    else:
        return render_template("ERROR.html", msg="Request Method Violation. Error Code: 705")


@app.route("/registerationForm")  # kaydolma sayfasi
def registrationForm():
    if 'email' not in session:  # bu kisim usttekilerle ayni mantik
        adminMi = 0
        session['adminMi'] = adminMi
    if session['adminMi'] == 0:  # bu kisim usttekilerle ayni mantik
        return redirect(url_for('root'))
    userId, girildiMi, adi = getLoginDetails()
    with sqlite3.connect(DatabaseName.databaseName) as con:
        try:
            cur = con.cursor()
            cur.execute('SELECT paketadi FROM pakettipi')
            data = cur.fetchall()
            cur.execute('SELECT adi FROM kullanicilar where ogretmenMi=1')
            ogretmenIsimleri = cur.fetchall()
        except Exception as e:
            con.rollback()
            print(f"Failure. Failure Code: 902. Failure is {e}")
            return render_template("ERROR.html", msg="Insertion Failure. Error Code: 706")
    con.close()
    if session['adminMi'] == 1:
        return render_template("sign_up.html", ogretmenIsimleri=ogretmenIsimleri ,userId=userId, girildiMi=girildiMi, adi=adi, data=data)
    else:
        # giris yaptiysa kaydolma sayfasi acilmaz anasayfaya yonlendirilir
        return redirect(url_for('root'))


@app.route("/clientsDetails")
def clientsDetails():
    if 'email' not in session:  # bu kisim usttekilerle ayni mantik
        adminMi = 0
        session['adminMi'] = adminMi
    if session['adminMi'] == 0:  # bu kisim usttekilerle ayni mantik
        return redirect(url_for('root'))
    if 'email' not in session:  # bu kisim usttekilerle ayni mantik
        return redirect(url_for('loginForm'))
    with sqlite3.connect(DatabaseName.databaseName) as con:
        try:
            cur = con.cursor()
            cur.execute('SELECT paketadi FROM pakettipi')
            pakettipleri = cur.fetchall()
        except Exception as e:
            con.rollback()
            print(f"Failure. Failure Code: 903. Failure is {e}")
            return render_template("ERROR.html", msg="Fetching Failure. Error Code: 707")
    con.close()
    userId, girildiMi, adi = getLoginDetails()
    con = sqlite3.connect(DatabaseName.databaseName)
    cur = con.cursor()
    cur.execute("SELECT * FROM kullanicilar")
    data = cur.fetchall()  # data from database
    cur.execute("select name from pragma_table_info('kullanicilar')")
    columnName=cur.fetchall()
    columnIsimleri = []
    for i in range(len(columnName)):
        columnIsimleri.append(str(columnName[i])[2:-3])
    print(data)
    return render_template("clients_details.html", columnIsimleri=columnIsimleri , count=len(columnName), value=data, userId=userId, girildiMi=girildiMi, adi=adi, pakettipleri=pakettipleri)


@app.route("/teachersDetails")
def teachersDetails():
    if 'email' not in session:  # bu kisim usttekilerle ayni mantik
        adminMi = 0
        session['adminMi'] = adminMi
    if session['adminMi'] == 0:  # bu kisim usttekilerle ayni mantik
        return render_template("ERROR.html", msg="You are not authorized. Error Code: 708")
    if 'email' not in session:  # bu kisim usttekilerle ayni mantik
        return redirect(url_for('loginForm'))
    with sqlite3.connect(DatabaseName.databaseName) as con:
        try:
            cur = con.cursor()
            cur.execute('SELECT paketadi FROM pakettipi')
            pakettipleri = cur.fetchall()
            cur.execute('SELECT adi FROM kullanicilar where ogretmenMi = 1')
            ogretmenAdi = cur.fetchall()
            cur.execute('SELECT * FROM kullanicilar where ogretmenMi =1')
            ogretmenMi = cur.fetchall()
            cur.execute("SELECT * FROM ogretmenlerinDersleri")
            data = cur.fetchall()  # data from database
            cur.execute('select userId from kullanicilar')
            idler = cur.fetchall()
            cur.execute('select adi,userId from kullanicilar ')
            isimler = cur.fetchall()
            cur.execute('select soyadi,userId from kullanicilar')
            soyadlar = cur.fetchall()

        except Exception as e:
            con.rollback()
            print(f"Failure. Failure Code: 904. Failure is {e}")
            return render_template("ERROR.html", msg="Fetching Failure. Error Code: 709")
    con.close()
    userId, girildiMi, adi = getLoginDetails()
    return render_template("teacher_details.html",idler=idler,isimler=isimler,soyadlar=soyadlar, ogretmenMi=ogretmenMi, ogretmenAdi=ogretmenAdi, value=data, userId=userId, girildiMi=girildiMi, adi=adi, pakettipleri=pakettipleri)


@app.route("/accountingDetails")
def accountingDetails():
    if 'email' not in session:  # bu kisim usttekilerle ayni mantik
        adminMi = 0
        session['adminMi'] = adminMi
    if session['adminMi'] == 0:  # bu kisim usttekilerle ayni mantik
        return redirect(url_for('root'))
    if 'email' not in session:  # bu kisim usttekilerle ayni mantik
        return redirect(url_for('loginForm'))
    userId, girildiMi, adi = getLoginDetails()
    con = sqlite3.connect(DatabaseName.databaseName)
    cur = con.cursor()
    cur.execute("select * from muhasebe")
    data = cur.fetchall()  # data from database

    cur.execute("select * from cafemuhasebe")
    cafedata = cur.fetchall()  # data from database

    cur.execute("select * from alacaklar")
    alacaklar = cur.fetchall()  # data from database

    cur.execute("select price from muhasebe")
    temp_deger_muhasebe = cur.fetchall()

    deger = []
    for i in range(len(temp_deger_muhasebe)):
        deger.append(int(str(temp_deger_muhasebe[i])[1:-2]))
    deger = sum(deger)

    cur.execute("select price from cafemuhasebe")
    temp_deger_cafemuhasebe = cur.fetchall()

    degerCafe = []
    for i in range(len(temp_deger_cafemuhasebe)):
        degerCafe.append(int(str(temp_deger_cafemuhasebe[i])[1:-2]))
    degerCafe = sum(degerCafe)

    cur.execute("select price from alacaklar")
    temp_deger_alacaklar = cur.fetchall()
    con.close()

    degerAlacaklar = []
    for i in range(len(temp_deger_alacaklar)):
        degerAlacaklar.append(int(str(temp_deger_alacaklar[i])[1:-2]))
    degerAlacaklar = sum(degerAlacaklar)

    return render_template("accounting_details.html", degerCafe=degerCafe, degerAlacaklar=degerAlacaklar, cafedata=cafedata, alacaklar=alacaklar, temp_deger_muhasebe=temp_deger_muhasebe, temp_deger_cafemuhasebe=temp_deger_cafemuhasebe, temp_deger_alacaklar=temp_deger_alacaklar, value=data, deger=deger, userId=userId, girildiMi=girildiMi, adi=adi)


@app.route("/copyingPage")
def copyingPage():
    if 'email' not in session:  # bu kisim usttekilerle ayni mantik
        adminMi = 0
        session['adminMi'] = adminMi
        return redirect(url_for('loginForm'))
    if session['adminMi'] == 0:  # bu kisim usttekilerle ayni mantik
        return redirect(url_for('root'))
    girildiMi, adi = getLoginDetails()[1:]
    return render_template('copyingPage.html', girildiMi=girildiMi, adi=adi)


@app.route("/incomeDetails")
def incomeDetails():
    if 'email' not in session:  # bu kisim usttekilerle ayni mantik
        adminMi = 0
        session['adminMi'] = adminMi
        return redirect(url_for('loginForm'))
    if session['adminMi'] == 0:  # bu kisim usttekilerle ayni mantik
        return redirect(url_for('root'))
    girildiMi, adi = getLoginDetails()[1:]
    with sqlite3.connect(DatabaseName.databaseName) as con:
        try:
            cur = con.cursor()
            cur.execute('SELECT paketadi FROM pakettipi')
            pakettipleri = cur.fetchall()
            cur.execute("select * from gelir")
            temp_deger = cur.fetchall()
            cur.execute('select userId from kullanicilar')
            idler = cur.fetchall()
            cur.execute('select adi,userId from kullanicilar ')
            isimler = cur.fetchall()
            cur.execute('select soyadi,userId from kullanicilar')
            soyadlar = cur.fetchall()
        except Exception as e:
            con.rollback()
            print(f"Failure. Failure Code: 905. Failure is {e}")
            return render_template("ERROR.html", msg="Fetching Failure. Error Code: 710")
    con.close()
    return render_template('income_details.html',idler=idler,isimler=isimler,soyadlar=soyadlar, temp_deger=temp_deger, girildiMi=girildiMi, adi=adi, pakettipleri=pakettipleri)


@app.route("/cafeIncomeDetails")
def cafeIncomeDetails():
    if 'email' not in session:  # bu kisim usttekilerle ayni mantik
        adminMi = 0
        session['adminMi'] = adminMi
        return redirect(url_for('loginForm'))
    if session['adminMi'] == 0:  # bu kisim usttekilerle ayni mantik
        return redirect(url_for('root'))
    girildiMi, adi = getLoginDetails()[1:]
    with sqlite3.connect(DatabaseName.databaseName) as con:
        try:
            cur = con.cursor()
            cur.execute('SELECT paketadi FROM pakettipi')
            pakettipleri = cur.fetchall()
            cur.execute("select * from cafe")
            temp_deger = cur.fetchall()
            cur.execute("select urunAdi from cafeUrunleri")
            cafe_urunleri = cur.fetchall()
            cur.execute("select * from cafeUrunleri")
            tumcafe_urunleri = cur.fetchall()
        except Exception as e:
            con.rollback()
            print(f"Failure. Failure Code: 906. Failure is {e}")
            return render_template("ERROR.html", msg="Fetching Failure. Error Code: 711")
    con.close()
    return render_template('cafe_income_details.html',tumcafe_urunleri=tumcafe_urunleri, cafe_urunleri=cafe_urunleri, temp_deger=temp_deger, girildiMi=girildiMi, adi=adi, pakettipleri=pakettipleri)


@app.route("/cafeIncome", methods=['GET', 'POST'])
def cafeIncome():
    if 'email' not in session:  # bu kisim usttekilerle ayni mantik
        adminMi = 0
        session['adminMi'] = adminMi
        return redirect(url_for('loginForm'))
    if session['adminMi'] == 0:  # bu kisim usttekilerle ayni mantik
        return redirect(url_for('root'))
    girildiMi, adi = getLoginDetails()[1:]
    if request.method == 'POST':
        # burasi muhasebe kismi icin

        date = request.form['date']
        price = request.form['urunFiyat']
        # end of muhasebe kismi

        # new accounting kismi
        howMany = request.form['howMany']
        uyeID = request.form['clientId']
        urunAdi = request.form['uruntipi']
        if price and date:
            try:

                print(int(price))
            except Exception as e:
                print(f"Hata {e}, girdi integer değil muhtemelen.")
            with sqlite3.connect(DatabaseName.databaseName) as con:
                try:
                    cur = con.cursor()

                    cur.execute(
                        'INSERT INTO cafe (urunAdi,satilanUrunSayisi,urunFiyat,satinAlanKisiAdi,date) VALUES ( ?,?,?, ?,?)', (urunAdi, howMany, price, uyeID, date))
                    cur.execute('select adi from kullanicilar where userId = ?' , uyeID)
                    satinAlanUyeninIsmi = cur.fetchall()
                    cur.execute('select soyadi from kullanicilar where userId = ?' , uyeID)
                    satinAlanUyeninSoyadi = cur.fetchall()
                    newIsim = str(satinAlanUyeninIsmi)[3:-4]
                    newSoyad = str(satinAlanUyeninSoyadi)[3:-4]
                    if int(price) > 0:
                        cur.execute(
                            'INSERT INTO cafemuhasebe (userId,userName,userSurname,price,date,explanation) VALUES (?, ?,?,?, ?,"KAFE")', (uyeID,newIsim , newSoyad, price, date))  
                        cur.execute('update cafeUrunleri SET  totalStok=totalStok- ? where urunAdi = ?', (howMany, urunAdi))
                        con.commit()  # veritabanina kaydedildi
                    else:
                        cur.execute(
                            'INSERT INTO alacaklar (userId,userName,userSurname,price,date,explanation) VALUES (?, ?,?,?, ?,"KAFE")', (uyeID,newIsim , newSoyad, price, date))  
                        con.commit()  # veritabanina kaydedildi
                    msg = "Kayıt Başarılı"
                except Exception as e:
                    con.rollback()
                    msg = "Hata olustu"
                    print(e)
            con.close()
        else:
            msg = "Kayıt bilgileri eksik"
        return render_template("cafe_income_details.html", error=msg, price=price, date=date, girildiMi=girildiMi, adi=adi) and redirect(url_for('cafeIncomeDetails'))
    else:
        return redirect(url_for('cafeIncomeDetails'))


@app.route("/searchCafe", methods=['GET', 'POST'])
def searchCafe():
    if 'email' not in session:  # bu kisim usttekilerle ayni mantik
        adminMi = 0
        session['adminMi'] = adminMi
    if session['adminMi'] == 0:  # bu kisim usttekilerle ayni mantik
        return redirect(url_for('root'))
    if 'email' not in session:  # bu kisim usttekilerle ayni mantik
        return redirect(url_for('loginForm'))
    userId, girildiMi, adi = getLoginDetails()
    if request.method == 'POST':
        id = request.form['name']
        if True and True:
            try:
                5+2
            except Exception as e:
                print(f"Hata {e}, girdi integer değil muhtemelen.")
            with sqlite3.connect(DatabaseName.databaseName) as con:
                try:
                    cur = con.cursor()
                    cur.execute(
                        'select * from kullanicilar where userId=?', (id))
                    value = cur.fetchall()
                    cur.execute(
                        'select sum(urunFiyat) from cafe where satinAlanKisiAdi=? ', (id))
                    dept = cur.fetchall()
                    cur.execute("select * from cafe")
                    temp_deger = cur.fetchall()
                    con.commit()  # veritabanina kaydedildi
                    msg = "Kayıt Başarılı"
                except Exception as e:
                    con.rollback()
                    msg = "Hata olustu"
                    print(e)
            con.close()
        else:
            msg = "Kayıt bilgileri eksik"
        return render_template("cafe_income_details.html", temp_deger=temp_deger, dept=dept,value=value, error=msg, date=date, girildiMi=girildiMi, adi=adi)
    else:
        return redirect(url_for('root'))


@app.route("/backupProcedure")
def backupProcedure():
    if 'email' not in session:  # bu kisim usttekilerle ayni mantik
        adminMi = 0
        session['adminMi'] = adminMi
    if session['adminMi'] == 0:  # bu kisim usttekilerle ayni mantik
        return redirect(url_for('root'))
    if 'email' not in session:  # bu kisim usttekilerle ayni mantik
        return redirect(url_for('loginForm'))
    try:
        today = date.today()
        now = date.today().weekday()
        if(now == 0):
            now = "Pazartesi"
        elif(now == 1):
            now = "Sali"
        elif(now == 2):
            now = "Carsamba"
        elif(now == 3):
            now = "Persembe"
        elif(now == 4):
            now = "Cuma"
        elif(now == 5):
            now = "Cumartesi"
        else:
            now = "Pazar"
        shutil.copyfile("./database.db",f"./database_backup_{str(today)}_{str(now)}.db")

        with sqlite3.connect(DatabaseName.databaseName) as con:
            try:
                cur = con.cursor()
                # Tabloları temizleme
                cur.execute("DELETE FROM alacaklar")
                cur.execute("DELETE FROM cafe")
                cur.execute("DELETE FROM cafeUrunleri")
                cur.execute("DELETE FROM cafealacaklar")
                cur.execute("DELETE FROM cafemuhasebe")
                cur.execute("DELETE FROM gelir")
                cur.execute("DELETE FROM muhasebe")
                cur.execute("DELETE FROM ogretmenlerinDersleri")
                cur.execute("DELETE FROM hareketler")
                con.commit()
                con.close()
            except Exception as e:
                print(f"Hata oluştu: {e}")

    except Exception as e:
        print(f"Hata oluştu: {e}")
    girildiMi, adi = getLoginDetails()[1:]
    return render_template('root.html', girildiMi=girildiMi, adi=adi)

    
@app.route("/changeDb")
def changeDb():
    if 'email' not in session:  # bu kisim usttekilerle ayni mantik
        adminMi = 0
        session['adminMi'] = adminMi
    if session['adminMi'] == 0:  # bu kisim usttekilerle ayni mantik
        return redirect(url_for('root'))
    if 'email' not in session:  # bu kisim usttekilerle ayni mantik
        return redirect(url_for('loginForm'))
    girildiMi, adi = getLoginDetails()[1:]
    return render_template('change_db.html', girildiMi=girildiMi, adi=adi)



# @app.route("/backupAccounting")
# def backupAccounting():
#     if 'email' not in session:  # bu kisim usttekilerle ayni mantik
#         adminMi = 0
#         session['adminMi'] = adminMi
#     if session['adminMi'] == 0:  # bu kisim usttekilerle ayni mantik
#         return redirect(url_for('root'))
#     if 'email' not in session:  # bu kisim usttekilerle ayni mantik
#         return redirect(url_for('loginForm'))
#     userId, girildiMi, adi = getLoginDetails()
#     try:
#         con = sqlite3.connect(DatabaseName.databaseName)
#         cur = con.cursor()
#         cur.execute("select * from muhasebe")
#         data = cur.fetchall()  # data from database
#         cur.execute("select price from muhasebe")
#         temp_deger = cur.fetchall()
#         deger = []
#         for i in range(len(temp_deger)):
#             deger.append(int(str(temp_deger[i])[1:-2]))
#         deger = sum(deger)
#         today = date.today()
#         now = date.today().weekday()
#         if(now == 0):
#             now = "Pazartesi"
#         if(now == 1):
#             now = "Sali"
#         if(now == 2):
#             now = "Carsamba"
#         if(now == 3):
#             now = "Persembe"
#         if(now == 4):
#             now = "Cuma"
#         if(now == 5):
#             now = "Cumartesi"
#         if(now == 6):
#             now = "Pazar"
# 
#         textfile = open("accountingBackup_"+str(today)+"_" +
#                         str(now)+".txt", "w", encoding="utf-8")
#         textfile.write(f"Toplam: {deger};")
#         for i in data:
#             textfile.write(f"\n{i}")
#         textfile.close()
#         cur.execute("DELETE FROM muhasebe")  # Remove all data
#         con.commit()
#         con.close()
# 
#
# 
#         con = sqlite3.connect(DatabaseName.databaseName)
#         cur = con.cursor()
#         cur.execute("select * from alacaklar")
#         data = cur.fetchall()  # data from database
#         cur.execute("select price from alacaklar")
#         temp_deger2 = cur.fetchall()
#         deger2 = []
#         for i in range(len(temp_deger2)):
#             deger2.append(int(str(temp_deger2[i])[1:-2]))
#         deger2 = sum(deger2)
#         today = date.today()
#         now = date.today().weekday()
#         if(now == 0):
#             now = "Pazartesi"
#         if(now == 1):
#             now = "Sali"
#         if(now == 2):
#             now = "Carsamba"
#         if(now == 3):
#             now = "Persembe"
#         if(now == 4):
#             now = "Cuma"
#         if(now == 5):
#             now = "Cumartesi"
#         if(now == 6):
#             now = "Pazar"
# 
#         textfile = open("accountingBackupAlacaklar_"+str(today)+"_" +
#                         str(now)+".txt", "w", encoding="utf-8")
#         textfile.write(f"Toplam: {deger};")
#         for i in data:
#             textfile.write(f"\n{i}")
#         textfile.close()
#         cur.execute("DELETE FROM alacaklar")  # Remove all data
#         con.commit()
#         con.close()
#
# 
#         con = sqlite3.connect(DatabaseName.databaseName)
#         cur = con.cursor()
#         cur.execute("select * from cafemuhasebe")
#         data = cur.fetchall()  # data from database
#         cur.execute("select price from cafemuhasebe")
#         temp_deger3 = cur.fetchall()
#         deger3 = []
#         for i in range(len(temp_deger3)):
#             deger3.append(int(str(temp_deger3[i])[1:-2]))
#         deger3 = sum(deger3)
#         today = date.today()
#         now = date.today().weekday()
#         if(now == 0):
#             now = "Pazartesi"
#         if(now == 1):
#             now = "Sali"
#         if(now == 2):
#             now = "Carsamba"
#         if(now == 3):
#             now = "Persembe"
#         if(now == 4):
#             now = "Cuma"
#         if(now == 5):
#             now = "Cumartesi"
#         if(now == 6):
#             now = "Pazar"
# 
#         textfile = open("accountingBackupCafeMuhasebe_"+str(today)+"_" +
#                         str(now)+".txt", "w", encoding="utf-8")
#         textfile.write(f"Toplam: {deger};")
#         for i in data:
#             textfile.write(f"\n{i}")
#         textfile.close()
#         cur.execute("DELETE FROM cafemuhasebe")  # Remove all data
#         con.commit()
#         con.close()
# 
#     except Exception as e:
#         print(f"Hata oluştu: {e}")
#     userId, girildiMi, adi = getLoginDetails()
#     return render_template('root.html', girildiMi=girildiMi, adi=adi)


@app.route("/accountingForm")  # kaydolma sayfasi
def accountingForm():
    if 'email' not in session:  # bu kisim usttekilerle ayni mantik
        adminMi = 0
        session['adminMi'] = adminMi
    if session['adminMi'] == 0:  # bu kisim usttekilerle ayni mantik
        return redirect(url_for('root'))
    if 'email' not in session:  # bu kisim usttekilerle ayni mantik
        return redirect(url_for('loginForm'))
    userId, girildiMi, adi = getLoginDetails()
    with sqlite3.connect(DatabaseName.databaseName) as con:
            try:
                cur = con.cursor()
                cur.execute('select userId from kullanicilar')
                idler = cur.fetchall()
                cur.execute('select adi,userId from kullanicilar ')
                isimler = cur.fetchall()
                cur.execute('select soyadi,userId from kullanicilar')
                soyadlar = cur.fetchall()
            except Exception as e:
                con.rollback()
                msg = "Hata olustu"
                print(e)
    con.close()
    return render_template("accounting.html", idler=idler , isimler=isimler ,soyadlar=soyadlar,girildiMi=girildiMi, adi=adi)


@app.route("/income", methods=['GET', 'POST'])
def income():
    if 'email' not in session:  # bu kisim usttekilerle ayni mantik
        adminMi = 0
        session['adminMi'] = adminMi
    if session['adminMi'] == 0:  # bu kisim usttekilerle ayni mantik
        return redirect(url_for('root'))
    if 'email' not in session:  # bu kisim usttekilerle ayni mantik
        return redirect(url_for('loginForm'))
    girildiMi, adi = getLoginDetails()[1:]
    if request.method == 'POST':
        # burasi muhasebe kismi icin

        date = request.form['date']
        price = request.form['ucret']
        explanation = request.form['explanation']
        # end of muhasebe kismi

        # new accounting kismi
        userId = request.form['id']
        uyeadi = request.form['uyeAdi']
        uyeSoyadi = request.form['uyeSoyadi']
        pakettipi = request.form['pakettipi']
        if price and date:
            try:

                print(int(price))
            except Exception as e:
                print(f"Hata {e}, girdi integer değil muhtemelen.")
            with sqlite3.connect(DatabaseName.databaseName) as con:
                try:
                    cur = con.cursor()
                    cur.execute('select paketgunu  from pakettipi where paketadi = ? ' , (pakettipi,))
                    paketgunu=cur.fetchall()
                    paketGunuVerisi = []
                    for i in range(len(paketgunu)):
                        paketGunuVerisi.append(str(paketgunu[i])[2:-3])
                    print(paketGunuVerisi[0])

                    cur.execute('select paketsaati  from pakettipi where paketadi = ? ' , (pakettipi,))
                    paketsaati=cur.fetchall()
                    paketSaatiVerisi = []
                    for i in range(len(paketsaati)):
                        paketSaatiVerisi.append(str(paketsaati[i])[2:-3])
                    print(paketSaatiVerisi[0])
                    if int(price) < 0:
                        cur.execute(
                            'INSERT INTO alacaklar (userId,userName,userSurname,price,date,explanation) VALUES (?,?,?,?, ?,?)', (userId , uyeadi , uyeSoyadi , price , date , explanation))
                        cur.execute(
                            'INSERT INTO gelir(userId , userName,userSurname,price,date,paketadi,aciklama) values (?,?,?,?,?,?,?)', (userId,uyeadi, uyeSoyadi, price, date, pakettipi, explanation))
                        cur.execute('UPDATE kullanicilar SET ' + pakettipi + 'GunSayisi = ' + pakettipi +'GunSayisi + ? , ' + pakettipi + 'DersSayisi = ' + pakettipi +'DersSayisi + ?   where userId =?',(paketGunuVerisi[0],paketSaatiVerisi[0],userId))
                    else:
                        cur.execute(
                            'INSERT INTO gelir(userId ,userName,userSurname,price,date,paketadi,aciklama) values (?,?,?,?,?,?,?)', (userId,uyeadi, uyeSoyadi, price, date, pakettipi, explanation))
                        cur.execute(
                            'INSERT INTO muhasebe (userId,userName,userSurname,price,date,explanation) VALUES (?,?,?,?, ?,?)', (userId , uyeadi , uyeSoyadi , price , date , explanation))
                        cur.execute('UPDATE kullanicilar SET ' + pakettipi + 'GunSayisi = ' + pakettipi +'GunSayisi + ? , ' + pakettipi + 'DersSayisi = ' + pakettipi +'DersSayisi + ?   where userId =?',(paketGunuVerisi[0],paketSaatiVerisi[0],userId))
                    cur.execute("select * from gelir")
                    temp_deger = cur.fetchall()
                    con.commit()  # veritabanina kaydedildi
                    msg = "Kayıt Başarılı"
                except Exception as e:
                    con.rollback()
                    msg = "Hata olustu"
                    print(e)
            con.close()
        else:
            msg = "Kayıt bilgileri eksik"
        return redirect(url_for('incomeDetails'))
    else:
        return redirect(url_for('incomeDetails'))


@app.route("/deletePersonal", methods=['GET', 'POST'])
def deletePersonal():
    if request.method == "POST":
        userId = request.form['userId']
        userName = request.form['userName']
        userSurname = request.form['userSurname']
        price = request.form['price']
        date = request.form['date']
        paketadi = request.form['paketadi']
        aciklama = request.form['aciklama']
        with sqlite3.connect(DatabaseName.databaseName) as con:
            try:
                cur = con.cursor()
                cur.execute(
                    'delete  from gelir where userId=? and userSurname=? and price=? and date=? and paketadi=? and aciklama=?', (userId, userName, userSurname, price, date, paketadi, aciklama, ))
                con.commit()  # veritabanina kaydedildi
                cur.execute(
                    'delete  from muhasebe where price=? and date=? and explanation=?', (price, date, aciklama, ))
                con.commit()  # veritabanina kaydedildi
            except Exception as e:
                con.rollback()
                print(e)
        con.close()
        return redirect(url_for('incomeDetails'))
    else:
        print("error")
        return redirect(url_for('root'))

@app.route("/accounting", methods=['GET', 'POST'])
def totalAmount():
    if 'email' not in session:  # bu kisim usttekilerle ayni mantik
        adminMi = 0
        session['adminMi'] = adminMi
    if session['adminMi'] == 0:  # bu kisim usttekilerle ayni mantik
        return redirect(url_for('root'))
    if 'email' not in session:  # bu kisim usttekilerle ayni mantik
        return redirect(url_for('loginForm'))
    userId, girildiMi, adi = getLoginDetails()
    if request.method == 'POST':
        idx = request.form['id']
        name = request.form['name']
        surname = request.form['surname']
        price = request.form['price']
        date = request.form['date']
        explanation = request.form['explanation']
        if price and date:
            try:
                print(int(price))
            except Exception as e:
                print(f"Hata {e}, girdi integer değil muhtemelen.")
            with sqlite3.connect(DatabaseName.databaseName) as con:
                try:
                    cur = con.cursor()
                    cur.execute('select adi from kullanicilar where adi=?',(name ,))
                    getName = cur.fetchall()
                    cur.execute('select soyadi from kullanicilar where soyadi=?',(surname ,))
                    getSurname = cur.fetchall()
                    cur.execute('select userId from kullanicilar where userId=?',(idx , ))
                    getId = cur.fetchall()
                    if getName and getSurname and getId:
                        print("ifinicinde")
                        cur.execute(
                            'INSERT INTO muhasebe (userId,userName,userSurname,price,date,explanation) VALUES ( ? , ? , ? , ? , ? , ?)', (idx,name,surname,price, date, explanation))
                        con.commit()  # veritabanina kaydedildi
                        msg = "Kayıt Başarılı"
                    else:
                        con.rollback()
                        return render_template('ERROR.html', msg="Wrong input values. Error Code: 702")
                except Exception as e:
                    con.rollback()
                    msg = "Hata olustu"
                    print(e)
            con.close()
        else:
            msg = "Kayıt bilgileri eksik"
        return redirect(url_for('accountingForm'))
    else:
        return redirect(url_for('root'))


@app.route("/increaseOneMonth", methods=['GET', 'POST'])
def addOneMonthToTheUser():
    if request.method == 'POST':
        no = request.form['no']
        gunsayisi = request.form['odemegunu']
        with sqlite3.connect(DatabaseName.databaseName) as con:
            try:
                cur = con.cursor()
                cur.execute(
                    'update kullanicilar SET  odeme=odeme+ ? where userId = ?', (gunsayisi, no))
                con.commit()  # veritabanina kaydedildi
            except Exception as e:
                con.rollback()
                print(e)
        con.close()
        return redirect(url_for('clientsDetails'))
    else:
        return redirect(url_for('root'))
        

@app.route("/decreaseOneDay")
def decreaseOneDay():
    if True == True:
        with sqlite3.connect(DatabaseName.databaseName) as con:
            try:
                cur = con.cursor()
                cur.execute(
                    'update kullanicilar SET  odeme=odeme-1  where userId > 1')
                con.commit()  # veritabanina kaydedildi
            except Exception as e:
                con.rollback()
                print(e)
        con.close()
        return redirect(url_for('clientsDetails'))
    else:
        print("error")
        return redirect(url_for('root'))


@app.route("/increaseOneDay")
def increaseOneDay():
    if True == True:
        with sqlite3.connect(DatabaseName.databaseName) as con:
            try:
                cur = con.cursor()
                cur.execute(
                    'update kullanicilar SET  odeme=odeme+1 where userId > 1')
                con.commit()  # veritabanina kaydedildi
            except Exception as e:
                con.rollback()
                print(e)
        con.close()
        return redirect(url_for('clientsDetails'))
    else:
        print("error")
        return redirect(url_for('root'))


@app.route("/increaseOne", methods=['GET', 'POST'])
def increaseOne():
    if request.method == 'POST':
        no = request.form['no']
        gunsayisi = request.form['odemegunu']
        with sqlite3.connect(DatabaseName.databaseName) as con:
            try:
                cur = con.cursor()
                cur.execute(
                    'UPDATE kullanicilar SET katilim = katilim + ? WHERE userId = ?', (gunsayisi, no))
                con.commit()  # veritabanina kaydedildi
            except Exception as e:
                con.rollback()
                print(e)
        con.close()
        return redirect(url_for('clientsDetails'))
    else:
        return redirect(url_for('root'))

############################################################################# Teacher Functions ########
@app.route("/addTeacherDetails", methods=['GET', 'POST'])
def addTeacherDetails():
    if request.method == 'POST':
        ogretmenAdi = request.form['ogretmenAdi']
        date = request.form['date']
        pakettipi = request.form['pakettipi']
        clientName = request.form['clientName']
        surname = request.form['clientSurname']
        idx = request.form['clientId']
        with sqlite3.connect(DatabaseName.databaseName) as con:
            try:
                cur = con.cursor()
                cur.execute('select adi from kullanicilar where adi=?',(clientName ,))
                getName = cur.fetchall()
                cur.execute('select soyadi from kullanicilar where soyadi=?',(surname ,))
                getSurname = cur.fetchall()
                cur.execute('select userId from kullanicilar where userId=?',(idx , ))
                getId = cur.fetchall()
                if getName and getSurname and getId:
                    print("ifinicinde")
                cur.execute('INSERT INTO ogretmenlerinDersleri (userId,userName,userSurname,ogretmenAdi,date,pakettipi) VALUES (?,?,?,?, ?,?)', (idx,clientName,surname, ogretmenAdi, date, pakettipi))
                cur.execute('UPDATE kullanicilar SET katilim = katilim + 1 , '+ pakettipi +'DersSayisi = '+pakettipi+'DersSayisi-1 WHERE userId = ?', (idx))
                con.commit()  # veritabanina kaydedildi
            except Exception as e:
                con.rollback()
                print(e)
        con.close()
        return redirect(url_for('teachersDetails'))
    else:
        return redirect(url_for('root'))

############################################################################# Package Functions ########
@app.route("/increaseOneMonthForExtraPackage", methods=['GET', 'POST'])
def increaseOneMonthForExtraPackage():
    if request.method == 'POST':
        no = request.form['no']
        ekstrapaketler= request.form['ekstrapaketler']
        with sqlite3.connect(DatabaseName.databaseName) as con:
            try:
                cur = con.cursor()
                cur.execute('select paketgunu  from pakettipi where paketadi = ? ' , (ekstrapaketler,))
                paketgunu=cur.fetchall()
                paketGunuVerisi = []
                for i in range(len(paketgunu)):
                    paketGunuVerisi.append(str(paketgunu[i])[2:-3])
                print(paketGunuVerisi[0])

                cur.execute('select paketsaati  from pakettipi where paketadi = ? ' , (ekstrapaketler,))
                paketsaati=cur.fetchall()
                paketSaatiVerisi = []
                for i in range(len(paketsaati)):
                    paketSaatiVerisi.append(str(paketsaati[i])[2:-3])
                print(paketSaatiVerisi[0])

                cur.execute('UPDATE kullanicilar SET ' + ekstrapaketler + 'GunSayisi = ' + ekstrapaketler +'GunSayisi + ? , ' + ekstrapaketler + 'DersSayisi = ' + ekstrapaketler +'DersSayisi + ?   where userId =?',(paketGunuVerisi[0],paketSaatiVerisi[0],no))
                con.commit()  # veritabanina kaydedildi
            except Exception as e:
                con.rollback()
                print(e)
        con.close()
        return redirect(url_for('clientsDetails'))
    else:
        return redirect(url_for('root'))


@app.route("/decreaseOneDayForExtraPackage")
def decreaseOneDayForExtraPackage():
    try:
        with sqlite3.connect(DatabaseName.databaseName) as con:
            try:
                cur = con.cursor()
                cur.execute('select paketadi from pakettipi')
                paketIsimleri = cur.fetchall()
                paketIsimleriVerisi = []
                for i in range(len(paketIsimleri)):
                    paketIsimleriVerisi.append(str(paketIsimleri[i])[2:-3])
                for counter in range(len(paketIsimleri)):
                    cur.execute('UPDATE kullanicilar SET '+paketIsimleriVerisi[counter]+'Gunsayisi = '+paketIsimleriVerisi[counter]+'Gunsayisi -1' )
                con.commit()  # veritabanina kaydedildi
            except Exception as e:
                con.rollback()
                print(e)
        con.close()
        return redirect(url_for('clientsDetails'))
    except Exception as e:
        print(e)
        return redirect(url_for('root'))


@app.route("/increaseOneDayForExtraPackage")
def increaseOneDayForExtraPackage():
    try:
        with sqlite3.connect(DatabaseName.databaseName) as con:
            try:
                cur = con.cursor()
                cur.execute('select paketadi from pakettipi')
                paketIsimleri = cur.fetchall()
                paketIsimleriVerisi = []
                for i in range(len(paketIsimleri)):
                    paketIsimleriVerisi.append(str(paketIsimleri[i])[2:-3])
                for counter in range(len(paketIsimleri)):
                    cur.execute('UPDATE kullanicilar SET '+paketIsimleriVerisi[counter]+'Gunsayisi = '+paketIsimleriVerisi[counter]+'Gunsayisi +1' )
                con.commit()  # veritabanina kaydedildi
            except Exception as e:
                con.rollback()
                print(e)
        con.close()
        return redirect(url_for('clientsDetails'))
    except Exception as e:
        print(e)
        return redirect(url_for('root'))

############################################################################# Package Functions ########
@app.route("/accountingMain")
def accountingMain():
    if session['adminMi'] == 1:  # admin paneli eger admin mi degiskeni 1 ise goruntulenecek
        userId, girildiMi, adi = getLoginDetails()  # login detaylari cekildi
        return render_template('accountingMain.html', girildiMi=girildiMi, adi=adi)
    else:
        # eger kisi admin degilse bu yazi ile karsilasacak
        return "Bu sayfaya sadece adminler erisebilir..."


@app.route("/clientMain")
def clientMain():
    if session['adminMi'] == 1:  # admin paneli eger admin mi degiskeni 1 ise goruntulenecek
        userId, girildiMi, adi = getLoginDetails()  # login detaylari cekildi
        return render_template('clientMain.html', girildiMi=girildiMi, adi=adi)
    else:
        # eger kisi admin degilse bu yazi ile karsilasacak
        return "Bu sayfaya sadece adminler erisebilir..."


if __name__ == '__main__':
    # 0.0.0.0 localhostta açık sunmak için. Bilgisayarın ipsine 5000. porttan bağlanılıyor
    app.run(debug=True, host='0.0.0.0')

from flask import *
from datetime import datetime 
import sqlite3, hashlib, os #hashlib sifreleme icin, os upload islemleri icin
from werkzeug.utils import secure_filename #dosya upload işlemleri için dahil edildi
from datetime import date, timedelta
import calendar  # to check clients days

app = Flask(__name__)
app.secret_key = 'random string' 
UPLOAD_FOLDER = 'static/uploads' #upload edilecek fotograflarin dosya konumu belirlendi
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif']) #upload edilecek fotograflarin uzantilari belirlendi
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def getLoginDetails():
    with sqlite3.connect('database.db') as conn: 
        cur = conn.cursor()
        try:
            if 'email' not in session: #emaile gore giris yapildi mi? yapilmadiysa alttaki satilar
                girildiMi = False #girilmedigi icin false
                adi = '' #sitede isim goruntulenmeyec
            else: #giris yapildiysa alttaki satirlar
                girildiMi = True #giris yapildigi icin true
                cur.execute("SELECT userId, adi FROM kullanicilar WHERE email = ?", (session['email'], ))
                userId, adi = cur.fetchone() #yukaridaki sorgudan sirasiyla degiskenlere veri cekildi
        except Exception as e:
            print(e)
    conn.close() #connection kapatildi
    return (girildiMi, adi) #fonksiyonun dondurdugu degiskenler


@app.route("/")
def root():
    if 'email' not in session: #giris yapilmadiysa
        adminMi = 0 #admin mi degiskeni sifir olacak
        session['adminMi'] = adminMi #bu session icine aktarilacak
    adminpanel = '' #admin paneli goruntulenmemesi icin
    if session['adminMi'] == 0: #eger giris yapan kisi admin degilse
        adminpanel = 'display: none;' #bu kisiye admin paneli goruntulenmeyecek
    girildiMi, adi = getLoginDetails() #yukarida olusturulan fonksiyondan degerler cekiliyor
    return render_template('anasayfa.html', adminpanel = adminpanel,girildiMi=girildiMi, adi=adi, )

@app.route("/AdminPanel")
def adminpanel():
    if session['adminMi'] == 1: #admin paneli eger admin mi degiskeni 1 ise goruntulenecek
        girildiMi, adi = getLoginDetails() #login detaylari cekildi
        return render_template('AdminPanel.html' , girildiMi=girildiMi, adi=adi) 
    else:
        return "Bu sayfaya sadece adminler erisebilir..." #eger kisi admin degilse bu yazi ile karsilasacak



@app.route("/addcategory") #kategori ekleme sayfasi
def addcategory():
    if 'email' not in session: #kisi admin degilse yapilacaklar
        adminMi = 0
        session['adminMi'] = adminMi 
    if session['adminMi'] == 1: #kisi adminse yapilacaklar
        girildiMi, adi= getLoginDetails()
        return render_template('kategoriEkle.html' , girildiMi=girildiMi, adi=adi)
    else:
        return "Bu sayfaya sadece adminler erisebilir..."
# @app.route("/addcategoryitem", methods=["GET", "POST"]) #kategoriEkle.html icinden bu sayfa cagiriliyor
# def addcategoryitem():
#     if request.method == "POST": 
#         isim = request.form['isim']
#         with sqlite3.connect('database.db') as conn:
#             try:
#                 cur = conn.cursor()
#                 cur.execute('''INSERT INTO kategoriler (isim) VALUES (?)''', (isim,))
#                 conn.commit() #burada kategori veritabanina ekleniyor
#                 msg="Basarili"
#             except:
#                 msg="Hata olustu"
#                 conn.rollback()
#                 return redirect(url_for('root'))
#         conn.close()
#         print(msg)
#         return redirect(url_for('root'))
#     else:
#         return redirect(url_for('root'))



@app.route("/account/profile") #profil sayfasi
def profileHome():
    if 'email' not in session: #bu kisim usttekilerle ayni mantik
        adminMi = 0
        session['adminMi'] = adminMi
    adminpanel = ''
    if session['adminMi'] == 0: #bu kisim usttekilerle ayni mantik
        adminpanel = 'display: none;'
    if 'email' not in session:
        return redirect(url_for('loginForm')) #giris yapilmadiysa login ekranina yonlendirme
    girildiMi, adi = getLoginDetails() #giris yapildiysa detaylari cek ve html'ye aktar
    return render_template("profilSyf.html", adminpanel=adminpanel, girildiMi=girildiMi, adi=adi)


@app.route("/account/profile/edit") #profil bilgilerini duzenleme sayfasi
def editProfile():
    if 'email' not in session: #bu kisim usttekilerle ayni mantik
        adminMi = 0
        session['adminMi'] = adminMi
    adminpanel = ''
    if session['adminMi'] == 0: #bu kisim usttekilerle ayni mantik
        adminpanel = 'display: none;'
    if 'email' not in session:
        return redirect(url_for('loginForm')) #login ekranina yonlendirme
    girildiMi, adi = getLoginDetails()
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM kullanicilar WHERE email = ?", (session['email'], ))
        profilVeri = cur.fetchone() #kullanicinin emailine gore bilgileri degiskene aktarildi html'de duzenlenebilir
    conn.close()
    return render_template("profilDzn.html", adminpanel=adminpanel, profilVeri=profilVeri, girildiMi=girildiMi, adi=adi)

@app.route("/account/profile/view") #profil bilgilerini gorme sayfasi
def viewProfile():
    if 'email' not in session: #bu kisim usttekilerle ayni mantik
        adminMi = 0
        session['adminMi'] = adminMi
    adminpanel = ''
    if session['adminMi'] == 0: #bu kisim usttekilerle ayni mantik
        adminpanel = 'display: none;'
    if 'email' not in session: #bu kisim usttekilerle ayni mantik
        return redirect(url_for('loginForm'))
    girildiMi, adi = getLoginDetails()
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM kullanicilar WHERE email = ?", (session['email'], ))
        profilVeri = cur.fetchone() #kullanicinin emailine gore bilgileri degiskene aktarildi html'de gosterilecek
    conn.close()
    return render_template("profilGrn.html", adminpanel=adminpanel, profilVeri=profilVeri, girildiMi=girildiMi, adi=adi)

@app.route("/account/profile/changePassword", methods=["GET", "POST"])
def changePassword():
    if 'email' not in session: #bu kisim usttekilerle ayni mantik
        adminMi = 0
        session['adminMi'] = adminMi
    adminpanel = ''
    if session['adminMi'] == 0: #bu kisim usttekilerle ayni mantik
        adminpanel = 'display: none;'
    if 'email' not in session: #bu kisim usttekilerle ayni mantik
        return redirect(url_for('loginForm'))
    girildiMi, adi = getLoginDetails()
    if request.method == "POST":
        eskiParola = request.form['eskiParola']
        eskiParola = hashlib.md5(eskiParola.encode()).hexdigest() #eski parola cozulerek degiskene aktarildi
        yeniParola = request.form['yeniParola']
        yeniParola = hashlib.md5(yeniParola.encode()).hexdigest() #yeni parola cozulerek degiskene aktarildi
        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT userId, parola FROM kullanicilar WHERE email = ?", (session['email'], ))
            userId, parola = cur.fetchone() #emaile gore userid ve parolasi alindi
            cur.execute("SELECT userId, email, adi, soyadi, adres1, adres2, postaKodu, ilce, il, ulke, tel FROM kullanicilar WHERE email = ?", (session['email'], ))
            profilVeri = cur.fetchone() # yine giris yapan kisinin emailine gore kisi bilgileri alindi
            if (parola == eskiParola):
                try:
                    cur.execute("UPDATE kullanicilar SET parola = ? WHERE userId = ?", (yeniParola, userId))
                    conn.commit() #yeni parola veritabanina aktarildi
                    msg="Sifre basariyla degistirildi."
                except:
                    conn.rollback()
                    msg = "Sifre degistirme basarisiz"
                return render_template("parolaDgs.html", msg=msg)
            else:
                msg = "Yanlis sifre"
            
        conn.close()
        return render_template("parolaDgs.html", adminpanel=adminpanel, profilVeri=profilVeri, girildiMi=girildiMi, adi=adi, msg=msg)
    else:
        return render_template("parolaDgs.html")

@app.route("/updateProfile", methods=["GET", "POST"]) #profilDzn.html icinden cagirilir
def updateProfile():
    if request.method == 'POST':
        email = request.form['email']
        adi = request.form['adi']
        soyadi = request.form['soyadi']
        adres1 = request.form['adres1']
        adres2 = request.form['adres2']
        postaKodu = request.form['postaKodu']
        ilce = request.form['ilce']
        il = request.form['il']
        ulke = request.form['ulke']
        tel = request.form['tel'] #html icinde doldurulan alanlar degiskenlere aktarildi
        with sqlite3.connect('database.db') as con:
                try:
                    cur = con.cursor()
                    cur.execute('UPDATE kullanicilar SET adi = ?, soyadi = ?, adres1 = ?, adres2 = ?, postaKodu = ?, ilce = ?, il = ?, ulke = ?, tel = ? WHERE email = ?', (adi, soyadi, adres1, adres2, postaKodu, ilce, il, ulke, tel, email))

                    con.commit()
                    msg = "Kayit basarili"
                except:
                    con.rollback()
                    msg = "Hata olustu"
        con.close()
        return redirect(url_for('root')) #islem sonucunda anasayfaya yonlendirme
    else:
        return redirect(url_for('root'))

@app.route("/loginForm") #giris sayfasi
def loginForm():
    if 'email' in session: #kullanici giris yaptiysa anasayfa ekranina yonlendirir
        return redirect(url_for('root'))
    else:
        return render_template('giris.html', error='')

@app.route("/login", methods = ['POST', 'GET']) #giris.html sayfasindan cagirilir
def login():
    if request.method == 'POST':
        adminMi = 0
        session['adminMi'] = adminMi
        email = request.form['email']
        parola = request.form['parola'] #email ve parola htmlden alinir
        if is_valid(email, parola, adminMi):
            session['email'] = email
            return redirect(url_for('root')) #giris yapildiginda anasayfaya yonlendirme
        else:
            error = 'Geçersiz kullanıcı adı veya şifre!'
            return render_template('giris.html', error=error)
    else:
        return redirect(url_for('loginForm')) #url'ye login yazilirsa loginForm'a yonlendirme


@app.route("/logout") #cikis ekrani
def logout():
    if 'email' not in session: #kisi eger giris yapmamissa anasayfaya yonlendirilir
        return redirect(url_for('root'))
    email = session['email']
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT userId FROM kullanicilar WHERE email = ?", (email, ))
        userId = cur.fetchone()[0]  #bu kisim usttekilerle ayni mantik
        try:
            cur.execute("DELETE FROM sepet WHERE sepet.userId = ?", (userId, ))
            conn.commit() #cikis yaparken sepeti silme 
        except:
            conn.rollback()
    conn.close()
    session.pop('email', None) #giris yapan kisiyi hafizadan atma
    return redirect(url_for('root')) #anasayfaya donus

def is_valid(email, parola, adminMi): #email ve parola dogru mu kiyasi
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute('SELECT email, parola, adminMi FROM kullanicilar')
    data = cur.fetchall()
    for row in data:
        if row[0] == email and row[1] == hashlib.md5(parola.encode()).hexdigest():
            adminMi = row[2]
            session['adminMi'] = adminMi
            return True
    return False


@app.route("/register", methods = ['GET', 'POST']) #kaydol.html'den cagirilir
def register():
    if request.method == 'POST':
        parola = request.form['parola']
        email = request.form['email']
        adi = request.form['adi']
        soyadi = request.form['soyadi']
        adres1 = request.form['adres1']
        adres2 = request.form['adres2']
        ilce = request.form['ilce']
        il = request.form['il']
        ulke = request.form['ulke']
        tel = request.form['tel'] #html'de doldurulan alanlar degiskenlere aktarildi
        boy = request.form['boy']
        kilo = request.form['kilo']
        kayitgunu = request.form['kayitgunu']
        pakettipi = request.form['pakettipi']
        aktifmi = request.form['aktifmi']
        arkadassayisi = request.form['arkadassayisi']

        with sqlite3.connect('database.db') as con:
            try:
                cur = con.cursor()
                cur.execute('INSERT INTO kullanicilar (parola, email, adi, soyadi, adres1, adres2, ilce, il, ulke, tel,boy,kilo,kayitgunu,pakettipi,aktifmi,katilim,arkadassayisi, odeme,adminMi) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?, "30",0)', (hashlib.md5(parola.encode()).hexdigest(), email, adi, soyadi, adres1, adres2, ilce, il, ulke, tel,boy,kilo,kayitgunu,pakettipi,aktifmi,arkadassayisi))

                con.commit() #veritabanina kaydedildi

                msg = "Kayıt Başarılı"
            except  Exception as e:
                con.rollback()
                msg = "Hata olustu"
                print (e)
        con.close()
        return render_template("giris.html", error=msg)
    else:
        return redirect(url_for('root'))



@app.route("/registerationForm") #kaydolma sayfasi
def registrationForm():
    if session['adminMi'] == 1 :
        return render_template("kaydol.html")
    else :
        return redirect(url_for('root')) #giris yaptiysa kaydolma sayfasi acilmaz anasayfaya yonlendirilir

def allowed_file(filename): #fotograf isimlerini duzenli hale getirmek icin
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def parse(data): #urunleri listelememizde kullandigimiz fonksiyon. birden fazla ayni satir olmasin diye yazildi
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

@app.route("/clientsDetails")
def clientsDetails():
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute("select * from kullanicilar")
    data = cur.fetchall() #data from database
    return render_template("clients_details.html", value=data)

@app.route("/accountingDetails")
def accountingDetails():
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute("select * from muhasebe")
    data = cur.fetchall() #data from database
    cur.execute("select price from muhasebe")
    temp_deger = cur.fetchall()
    print(temp_deger)
    deger = []
    for i in range(len(temp_deger)):
        deger.append(int(str(temp_deger[i])[1:-2]))
    deger=sum(deger)
	
    return render_template("accounting_details.html", value=data, sums=deger)

@app.route("/accountingForm") #kaydolma sayfasi
def accountingForm():
    if 'email' not in session: #kisi giris yapmadiysa kaydol.html acilir
        return render_template("kaydol.html")
    else:
        return render_template("accounting.html") #giris yaptiysa kaydolma sayfasi acilmaz anasayfaya yonlendirilir

@app.route("/accounting", methods = ['GET', 'POST'])
def totalAmount():
    if 'email' not in session: #bu kisim usttekilerle ayni mantik
        adminMi = 0
        session['adminMi'] = adminMi
    adminpanel = ''
    if session['adminMi'] == 0: #bu kisim usttekilerle ayni mantik
        adminpanel = 'display: none;'
        return redirect(url_for('root'))
    if 'email' not in session: #bu kisim usttekilerle ayni mantik
        return redirect(url_for('loginForm'))
    girildiMi, adi = getLoginDetails()
    if request.method == 'POST':
        price = request.form['price']
        date = request.form['date']
        explanation=request.form['explanation']
        if price and date:
            with sqlite3.connect('database.db') as con:
                try:
                    cur = con.cursor()
                    cur.execute('INSERT INTO muhasebe (price,date,explanation) VALUES ( ?, ?,?)', (price,date,explanation))
                    con.commit() #veritabanina kaydedildi
                    msg = "Kayıt Başarılı"
                except  Exception as e:
                    con.rollback()
                    msg = "Hata olustu"
                    print (e)
            con.close()
        else:
            msg = "Kayıt bilgileri eksik"
        return render_template("accounting.html", error=msg , price=price , date=date)
    else:
        return redirect(url_for('root'))


@app.route("/increaseOneMonth", methods = ['GET', 'POST'])
def addOneMonthToTheUser():
    if request.method == 'POST':
        email = request.form['email']
        gunsayisi = request.form['odemegunu']
        with sqlite3.connect('database.db') as con:
            try:
                cur = con.cursor()
                cur.execute('update kullanicilar SET  odeme=odeme+ ? where email = ?',(gunsayisi,email))
                con.commit() #veritabanina kaydedildi    
            except  Exception as e:
                con.rollback()
                print (e)
        con.close()
        return render_template("AdminPanel.html")
    else:
        return redirect(url_for('root'))

@app.route("/decreaseOneDay")
def decreaseOneDay():
    print("-1yarrak")
    if True == True:
        with sqlite3.connect('database.db') as con:
            print("yarrak")
            try:
                print("yarra1k")
                cur = con.cursor()
                cur.execute('update kullanicilar SET  odeme=odeme-1 where userId > 1')
                con.commit() #veritabanina kaydedildi    
            except  Exception as e:
                con.rollback()
                print (e)
        con.close()
        return render_template("AdminPanel.html")
    else:
        print("error")
        return redirect(url_for('root'))

@app.route("/increaseOneDay")
def increaseOneDay():
    print("-1yarrak")
    if True == True:
        with sqlite3.connect('database.db') as con:
            print("yarrak")
            try:
                print("yarra1k")
                cur = con.cursor()
                cur.execute('update kullanicilar SET  odeme=odeme+1 where userId > 1')
                con.commit() #veritabanina kaydedildi    
            except  Exception as e:
                con.rollback()
                print (e)
        con.close()
        return render_template("AdminPanel.html")
    else:
        print("error")
        return redirect(url_for('root'))


if __name__ == '__main__':
    app.run(debug=True, host= '0.0.0.0') #0.0.0.0 localhostta açık sunmak için. Bilgisayarın ipsine 5000. porttan bağlanılıyor

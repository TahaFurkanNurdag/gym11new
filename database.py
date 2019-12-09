import sqlite3

#Veri tabani acma
conn = sqlite3.connect('database.db')

#Tablolari olusturma
conn.execute('''CREATE TABLE `kullanicilar` (
	`userId`	INTEGER,
	`parola`	TEXT,
	`email`	TEXT,
	`adi`	TEXT,
	`soyadi`	TEXT,
	`adres1`	TEXT,
	`adres2`	TEXT,
	`il`	TEXT,
	`ilce`	TEXT,
	`ulke`	TEXT,
	`tel`	TEXT,
	`boy`   INTEGER,
	`kilo`  INTEGER,
	`kayitgunu` DATE,
	`pakettipi` TEXT,
	`ekstrapaketler` TEXT,
	`paketkalangunsayisi` INTEGER,
	`aktifmi`   INTEGER,
	`katilim`   INTEGER,
	`arkadassayisi` INTEGER,
	`odeme`    INTEGER,
	`ogretmenMi`	INTEGER,
	`adminMi`	INTEGER,
	PRIMARY KEY(`userId`)
		)''')

conn.execute('''CREATE TABLE `muhasebe` (
	`id`	INTEGER,
	`userId` INTEGER,
	`userName` TEXT,
	`userSurname` TEXT,
	`price` INTEGER,
	`date`  DATE,
	`explanation` TEXT,
	FOREIGN KEY(`userId`) REFERENCES `kullanicilar`(`userId`),
	FOREIGN KEY(`userName`) REFERENCES `kullanicilar`(`adi`),
	FOREIGN KEY(`userSurname`) REFERENCES `kullanicilar`(`soyadi`),
	PRIMARY KEY(`id`)
		)''')
		
conn.execute('''CREATE TABLE `cafemuhasebe` (
	`id`	INTEGER,
	`userId` INTEGER,
	`userName` TEXT,
	`userSurname` TEXT,
	`price` INTEGER,
	`date`  DATE,
	`explanation` TEXT,
	FOREIGN KEY(`userId`) REFERENCES `kullanicilar`(`userId`),
	FOREIGN KEY(`userName`) REFERENCES `kullanicilar`(`adi`),
	FOREIGN KEY(`userSurname`) REFERENCES `kullanicilar`(`soyadi`),
	PRIMARY KEY(`id`)
		)''')
		
conn.execute('''CREATE TABLE `alacaklar` (
	`id`	INTEGER,
	`userId` INTEGER,
	`userName` TEXT,
	`userSurname` TEXT,
	`price` INTEGER,
	`date`  DATE,
	`explanation` TEXT,
	FOREIGN KEY(`userId`) REFERENCES `kullanicilar`(`userId`),
	FOREIGN KEY(`userName`) REFERENCES `kullanicilar`(`adi`),
	FOREIGN KEY(`userSurname`) REFERENCES `kullanicilar`(`soyadi`),
	PRIMARY KEY(`id`)
		)''')
		
		
conn.execute('''CREATE TABLE `ogretmenlerinDersleri` (
	`id`	INTEGER,
	`userId` INTEGER,
	`userName` TEXT,
	`userSurname` TEXT,
	`ogretmenAdi` TEXT,
	`date`  DATE,
	`pakettipi` TEXT,
	PRIMARY KEY(`id`)
		)''')
		
conn.execute('''CREATE TABLE `hareketler` (
	`id`	INTEGER,
	`name`	TEXT,
	`description`	TEXT,
	`video`	TEXT,
	PRIMARY KEY(`id`)
		)''')
		
conn.execute('''CREATE TABLE `pakettipi` (
	`id`	INTEGER,
	`paketadi`	TEXT,
	`paketfiyati`	INTEGER,
	`paketaciklamasi` TEXT,
	PRIMARY KEY(`id`)
		)''')

conn.execute('''CREATE TABLE `kategoriler` (
	`categoryId`	INTEGER,
	`isim`	TEXT,
	PRIMARY KEY(`categoryId`)
		)''')
		
conn.execute('''CREATE TABLE `gelir` (
	`id` INTEGER,
	`userId`	INTEGER,
	`userName`	TEXT,
	`userSurname`	TEXT,
	`price`	TEXT,
	`date`	DATE,
	`paketadi`	TEXT,
	`aciklama`	TEXT,
	FOREIGN KEY(`userId`) REFERENCES `kullanicilar`(`userId`),
	PRIMARY KEY(`id`)
		)''')
		
conn.execute('''CREATE TABLE `cafe` (
	`urunId`	INTEGER,
	`urunAdi`	TEXT,
	`satilanUrunSayisi`	TEXT,
	`urunFiyat`	TEXT,
	`satinAlanKisiAdi`	TEXT,
	`date`	DATE,
	PRIMARY KEY(`urunId`)
		)''')
		
conn.execute('''CREATE TABLE `cafeUrunleri` (
	`urunId`	INTEGER,
	`urunAdi`	TEXT,
	`totalStok`	INTEGER,
	PRIMARY KEY(`urunId`)
		)''')
		
conn.execute('''INSERT INTO "main"."kullanicilar" ("userId", "parola", "email", "adi", "soyadi", "adres1", "adres2", "il", "ilce", "ulke", "tel", "boy", "kilo", "kayitgunu", "pakettipi", "ekstrapaketler", "paketkalangunsayisi", "aktifmi", "katilim", "arkadassayisi", "odeme", "ogretmenMi", "adminMi") VALUES ('1', 'tfn', 'tfn@tfn', 'TFN', 'TFN', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1')''')
conn.execute('''INSERT INTO "main"."kullanicilar" ("userId", "parola", "email", "adi", "soyadi", "adres1", "adres2", "il", "ilce", "ulke", "tel", "boy", "kilo", "kayitgunu", "pakettipi", "ekstrapaketler", "paketkalangunsayisi", "aktifmi", "katilim", "arkadassayisi", "odeme", "ogretmenMi", "adminMi") VALUES ('2', 'tfn', 'ozgur@ozgur', 'OZGUR', 'OZGUR', '1', '1', '1', '1', '1', '1', '2', '2', '2019-12-02', '1', '1', '0', '1', '0', '1', '30', '0', '0')''')
conn.execute('''INSERT INTO "main"."pakettipi" ("id", "paketadi", "paketfiyati", "paketaciklamasi") VALUES ('1', 'Spinning', '200', 'xxx tl yeni')''')
conn.execute('''INSERT INTO "main"."ogretmenlerinDersleri" ("id", "userId", "userName", "userSurname", "ogretmenAdi", "date", "pakettipi") VALUES ('1', '2', 'OZGUR', 'OZGUR', 'TFN', '0222-02-22', 'Spinning')''')
conn.execute('''INSERT INTO "main"."cafeUrunleri" ("urunId", "urunAdi", "totalStok") VALUES ('1', 'Makarna', '100')''')
conn.execute('''INSERT INTO "main"."gelir" ("id", "userId", "userName", "userSurname", "price", "date", "paketadi", "aciklama") VALUES ('1', '2', 'TFN', 'TFN', '3333', '0003-03-22', 'Spinning', '2')''')

conn.commit()

conn.close()
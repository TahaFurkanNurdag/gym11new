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
	`kayitEdeninAdi` TEXT,
	`hastalik` TEXT,
	`dogumTarihi` DATE,
	`tel`	TEXT,
	`boy`   INTEGER,
	`kilo`  INTEGER,
	`adres1` TEXT,
	`adres2` TEXT,
	`kayitgunu` DATE,
	`aktifmi`   INTEGER,
	`katilim`   INTEGER,
	`arkadassayisi` INTEGER,
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
	`paketgunu`	TEXT,
	`paketsaati`	TEXT,
	`paketfiyati`	INTEGER,
	`paketaciklamasi` TEXT,
	PRIMARY KEY(`id`)
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


conn.execute('''CREATE TABLE `cafealacaklar` (
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
		
		
conn.execute('''INSERT INTO "main"."kullanicilar" ("userId", "parola", "email", "adi", "soyadi", "kayitEdeninAdi", "hastalik","dogumTarihi", "tel", "boy", "kilo", "adres1", "adres2", "kayitgunu", "aktifmi", "katilim", "arkadassayisi", "ogretmenMi", "adminMi") VALUES ('1', 'tfn', 'tfn@tfn', 'Taha Furkan', 'Nurdag', 'TFN', 'Yok',"1997-09-26", '05350363646', '181', '85', 'EvAdresi', 'IsAdresi', '2019-12-17', '1', '0', '0', '1', '1')''')
conn.execute('''INSERT INTO "main"."kullanicilar" ("userId", "parola", "email", "adi", "soyadi", "kayitEdeninAdi", "hastalik","dogumTarihi", "tel", "boy", "kilo", "adres1", "adres2", "kayitgunu", "aktifmi", "katilim", "arkadassayisi", "ogretmenMi", "adminMi") VALUES ('2', 'ozgur', 'ozgur@ozbek', 'Ozgur', 'Ozbek', 'TFN', 'Yok',"1997-09-26", '05062545050', '180', '85', 'EvAdresi', 'IsAdresi', '2019-12-17', '1', '0', '1', '1', '1') ''')
conn.execute('''INSERT INTO "main"."kullanicilar" ("userId", "parola", "email", "adi", "soyadi", "kayitEdeninAdi", "hastalik","dogumTarihi", "tel", "boy", "kilo", "adres1", "adres2", "kayitgunu", "aktifmi", "katilim", "arkadassayisi", "ogretmenMi", "adminMi") VALUES ('3', 'DışKaynak', 'DışKaynak@DışKaynak', 'DışKaynak', 'DışKaynak', 'DışKaynak', 'DışKaynak',"1997-09-26", '0000000', '000', '0000', '0000', '0000', '12-12-12', '0', '0', '0', '0', '0') ''')

conn.commit()

conn.close()
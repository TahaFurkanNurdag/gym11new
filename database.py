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
	`pakettipi` INTEGER,
	`aktifmi`   INTEGER,
	`katilim`   INTEGER,
	`arkadassayisi` INTEGER,
	`odeme`    TEXT,
	`adminMi`	INTEGER,
	PRIMARY KEY(`userId`)
		)''')

conn.execute('''CREATE TABLE `muhasebe` (
	`id`	INTEGER,
	`price` INTEGER,
	`date`  DATE,
	`explanation` TEXT,
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

conn.commit()

#ilk veriler
cur = conn.cursor()	
cur.execute('''INSERT INTO kategoriler (isim) VALUES ("deneme")''')
cur.execute('''INSERT INTO kullanicilar (parola,email,adi,soyadi,adres1,adres2,il,ilce,ulke,tel,boy,kilo,kayitgunu,pakettipi,aktifmi,katilim,arkadassayisi,odeme,adminMi) 	VALUES ("deneme", "deneme@deneme.com", "deneme", "deneme","deneme",  "deneme", "deneme","deneme", "deneme", "deneme",123,321,26.09.2019,1,1,23,90,"hayir", 1)''')


cur.execute('''INSERT INTO kullanicilar (
	parola,
	email,
	adi,
	soyadi,
	adres1,
	adres2,
	il,
	ilce,
	ulke,
	tel,
	boy,
	kilo,
	kayitgunu,
	pakettipi,
	aktifmi,
	katilim,
	arkadassayisi,
	adminMi) VALUES ("a","a@a","tahafurkan","nurdag","kuckbakkalkoyadres","atasehiradres","istanbul","atasehirilce","turkiye","05350363656",123,1234,26.05.1995,1,1,50,1)''')

	
conn.commit()
conn.close()
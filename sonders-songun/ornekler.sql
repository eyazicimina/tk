
-- select id, ST_AsText(geom) from parsel limit 10;
SELECT * FROM parsel LIMIT 10;


-- Tum parsellerin alanlari
SELECT ST_Area( geom )
FROM parsel;

-- Tum parsellerin alanlarinin ortalamasi
SELECT AVG(ST_Area( geom ))
FROM parsel;

-- Tum parsellerin alanlarinin ortalamasi, max ve min
SELECT AVG(ST_Area( geom )), MAX(ST_Area( geom )), MIN(ST_Area( geom ))
FROM parsel;

-- Tum parsellerin toplam alani
SELECT SUM(ST_Area( geom, True ))
FROM parsel;

-- Dunyanin cevresi 40.000 KM, Capi = 12.800, Yari Capi = 6400 KM
-- Dunyanin alani = Kurenin alani, 4 * pi * r2
-- Dunyanin alani = 514.457.600 KM2
-- Turkiyenin alani = 783000 KM2

-- Tum parsellerin toplam alani
SELECT SUM(ST_Area( geom, True )) / 783000000000,
	SUM(ST_Area( geom, True )) / 514457600000000
FROM parsel;

--- 1.4522019786426896e-05	2.2102388015595957e-08

-- int(3.4) ==> 3
-- str(3)   ==> "3"
-- CAST( ... AS integer )
-- Mahalle bazinda (toplam parsel alanlari)
SELECT mahallead, CAST(SUM( ST_Area( geom, True ) ) AS integer)
FROM parsel
GROUP BY mahallead;

/*
	"DİKMEN"	10190233
	"ÖVEÇLER"	 1180509
*/


SELECT mahallead, CAST(AVG( ST_Area( geom, True ) ) AS integer)
FROM parsel
GROUP BY mahallead;

/*
"DİKMEN"	10761
"ÖVEÇLER"	01171
*/

select * from parsel limit 1;

SELECT tapucinsaciklama, AVG(ST_Area(geom, True)), COUNT(*)
FROM parsel
GROUP BY tapucinsaciklama
ORDER BY 3 DESC;

/*
"-Apartman--Beton-"	911.5515422572097	232
"Arsa"	25658.085980173233	218
"BAĞ"	1500.7131878017171	186
"TARLA"	5960.065596593973	181
"ARSA"	3273.2907610542393	179
"Apartman - Beton"	1189.3337930232813	111
"KARGİR APARTMAN"	2356.459978563218	94
"BETONARME APARTMAN"	1173.4040874771126	64
"KIRAÇ TARLA"	18127.857416407256	56
"Beton Apartman"	1056.3035572579324	38
"BETONARME KARKAS BİNA"	1707.132190729022	33
*/

SELECT tapucinsaciklama, AVG(ST_Area(geom, True)) * COUNT(*)
FROM parsel
GROUP BY tapucinsaciklama;


SELECT tapucinsaciklama FROM parsel 
WHERE 
	(tapucinsaciklama LIKE '% arsa%') OR
	(tapucinsaciklama LIKE 'arsa%');

/*
UPDATE parsel SET tapucinsaciklama = REPLACE(tapucinsaciklama, 'I', 'ı');
UPDATE parsel SET tapucinsaciklama = REPLACE(tapucinsaciklama, 'İ', 'i');
UPDATE parsel SET tapucinsaciklama = REPLACE(tapucinsaciklama, 'Ş', 'ş');
UPDATE parsel SET tapucinsaciklama = REPLACE(tapucinsaciklama, 'Ğ', 'ğ');
UPDATE parsel SET tapucinsaciklama = REPLACE(tapucinsaciklama, 'Ü', 'ü');
UPDATE parsel SET tapucinsaciklama = REPLACE(tapucinsaciklama, 'Ö', 'ö');
UPDATE parsel SET tapucinsaciklama = REPLACE(tapucinsaciklama, 'Ç', 'ç');

UPDATE parsel SET tapucinsaciklama = LOWER(tapucinsaciklama);
*/

-- I => i
-- I => ı
-- İ => 
-- ı => 

SELECT tapucinsaciklama, AVG(ST_Area(geom)), COUNT(*) FROM parsel 
WHERE 
	(tapucinsaciklama LIKE '% arsa%') OR
	(tapucinsaciklama LIKE 'arsa%')
GROUP BY tapucinsaciklama
HAVING COUNT(*) > 1
ORDER BY 3 DESC;

select tapucinsaciklama, avg(tapualan - kadastroalan) from parsel
group by tapucinsaciklama
order by 2 asc;


select tapucinsaciklama, tapualan, kadastroalan, tapualan - kadastroalan 
from parsel where tapualan - kadastroalan > 30
order by tapualan - kadastroalan DESC;

SELECT tapualan, kadastroalan, ST_Area(geom, True), 
	ABS(ST_Area(geom, True) - tapualan) 
	+ 
	ABS(ST_Area(geom, True) - kadastroalan)
	AS 
	Error
FROM parsel
ORDER BY 4 DESC;

SELECT 
	tapucinsaciklama, tapualan, kadastroalan, tapualan - kadastroalan as Fark
FROM 
	parsel 
WHERE 
	tapualan - kadastroalan > 30
ORDER BY 
	tapualan - kadastroalan DESC;






SELECT 
	tapucinsaciklama, tapualan, kadastroalan, tapualan - kadastroalan as Fark
FROM 
	parsel 
WHERE 
	tapualan - kadastroalan > 30
UNION 
SELECT 
	tapucinsaciklama, tapualan, kadastroalan, tapualan - kadastroalan as Fark
FROM 
	parsel 
WHERE 
	tapualan < 1
	
	

DROP VIEW HataliParseller;
CREATE VIEW HataliParseller AS
SELECT 
	tapucinsaciklama, tapualan, kadastroalan, tapualan - kadastroalan as Fark
FROM 
	parsel 
WHERE 
	(tapualan - kadastroalan > 30)
	OR
	(tapualan < 1)
	OR
	LENGTH(tapucinsaciklama) < 1;


SELECT * FROM HataliParseller;	
	
	

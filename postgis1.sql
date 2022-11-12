
-- create extension postgis;

SELECT ST_GeomFromText('POINT(120 100)');

-- EPSG
SELECT ST_GeomFromText('POINT(120 100)', 4326);

SELECT ST_MakePoint(26.45, 36.42);



CREATE TABLE IF NOT EXISTS geometries (name varchar, geom geometry);
-- INSERT INTO geometries (...) VALUES (...);
-- INSERT INTO geometries VALUES (...);

DELETE FROM geometries;
SELECT COUNT(*) FROM geometries;

INSERT INTO geometries VALUES ('Point', 'POINT(100 200)');
INSERT INTO geometries VALUES ('LineString', 'LINESTRING(0 0, 1 1, 2 1, 2 2)');
INSERT INTO geometries VALUES ('Polygon', 'POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))');
INSERT INTO geometries VALUES ('PolygonWithHole', 
'POLYGON((0 0, 10 0, 10 10, 0 10, 0 0), (1 1, 1 2, 2 2, 2 1, 1 1))');

SELECT COUNT(*) FROM geometries;

--SELECT name, ST_AsText(geom) FROM geometries limit 10 offset 3000;



--ST_GeomFromText x ST_AsText
SELECT ST_AsText(ST_GeomFromText('POINT(100 200)'))

SELECT ST_AsText(ST_MakePoint(26.45, 36.42)), ST_MakePoint(26.45, 36.42);



select ST_GeometryType(geom) from geometries
WHERE ST_GeometryType(geom) = 'ST_LineString';


SELECT ST_GeometryType(geom), COUNT(*)
FROM geometries
GROUP BY ST_GeometryType(geom);



SELECT ST_SRID(
	ST_GeomFromText(
		ST_AsText(
			ST_GeomFromText(
				'POINT(120 100)'
			)
		), 
		4326
	)
);






-- -----------------------------
SELECT ST_GeometryType(geom), ST_SRID(geom), ST_NDims(geom), ST_X(geom), ST_Y(geom)
FROM geometries
-- WHERE ST_NDims(geom) != 2
WHERE ST_GeometryType(geom) = 'ST_Point'
ORDER BY random() -- df.sample(n = 10)
LIMIT 20;


-- -----------------------------
-- 30 birimden uzun olan en uzun caddelerden 20 tane
SELECT ST_Astext(geom), ST_Length(geom)
FROM geometries
WHERE ST_GeometryType(geom) = 'ST_LineString'
AND ST_Length(geom) > 30
ORDER BY ST_Length(geom) DESC
LIMIT 20;

-- Ortalama ve maksimum doğrultu uzunluğu nedir
SELECT avg(ST_Length(geom)), max(ST_Length(geom))
FROM geometries
WHERE ST_GeometryType(geom) = 'ST_LineString'


-- Bir doğrultunun, başlangıç ve bitiş noktası
SELECT ST_Astext(geom), ST_Length(geom), 
	ST_AsText(ST_StartPoint(geom)) as "Başlangıç",
	ST_AsText(ST_EndPoint(geom)) as "Bitiş"	
FROM geometries
WHERE ST_GeometryType(geom) = 'ST_LineString'
AND ST_Length(geom) > 30
ORDER BY ST_Length(geom) DESC
LIMIT 20;



-- Bir doğrultunun, başlangıç ve bitiş noktası
SELECT ST_Astext(geom), ST_Length(geom), 
	ST_AsText(ST_StartPoint(geom)) as "Başlangıç",
	ST_AsText(ST_EndPoint(geom)) as "Bitiş",
	ST_NPoints(geom) as "Kaç nokta"
	
FROM geometries
WHERE ST_GeometryType(geom) = 'ST_LineString'
AND ST_Length(geom) > 30
ORDER BY  RANDOM()
LIMIT 20;




SELECT ST_AsText(geom),ST_NPoints(geom) as "Kaç nokta"
FROM geometries
WHERE ST_GeometryType(geom) = 'ST_Polygon'
ORDER BY  RANDOM()
LIMIT 20;



SELECT ST_GeometryType(geom),  ST_NPoints(geom) as "Kaç nokta", ST_Area(geom)
FROM geometries
WHERE ST_GeometryType(geom) = 'ST_Polygon'
ORDER BY  RANDOM()
LIMIT 20;


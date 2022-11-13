
select mahallead, count(*)
from kadastro
where abs(tapualan - kadastroalan) > 5
group by mahallead;



SELECT 
	tapualan - kadastroalan AS Fark
FROM 
	kadastro
WHERE tapualan - kadastroalan < 0;



SELECT SIGN(-3435234.33453)
SELECT SIGN(0)
SELECT SIGN(2345453533)


SELECT 
	SIGN(tapualan - kadastroalan), COUNT(*)
FROM 
	kadastro
GROUP BY SIGN(tapualan - kadastroalan);

select sum(abs(tapualan-kadastroalan)) / count(*)
from kadastro;


select avg(abs(tapualan-kadastroalan)) 
from kadastro;


select 
	avg(abs(ST_Area(geom,True) - tapualan) / ST_Area(geom,True)), 
	avg(abs(ST_Area(geom,True) - kadastroalan) / ST_Area(geom,True))
from kadastro;


select ST_Astext(geom), ST_NPoints(geom) 
from kadastro order by  ST_NPoints(geom) desc;






SELECT ST_NPoints(geom)
	, COUNT(*)
FROM 
	kadastro
GROUP BY ST_NPoints(geom)
order by 2 DESC
LIMIT 1;

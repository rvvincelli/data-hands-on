```
     _   _    ____  ____  
    | | / \  |  _ \/ ___| 
 _  | |/ _ \ | | | \___ \ 
| |_| / ___ \| |_| |___) |
 \___/_/   \_\____/|____/ 
                          
 _   _    _    _   _ ____  ____     ___  _   _   ____    _  _____  _    
| | | |  / \  | \ | |  _ \/ ___|   / _ \| \ | | |  _ \  / \|_   _|/ \   
| |_| | / _ \ |  \| | | | \___ \  | | | |  \| | | | | |/ _ \ | | / _ \  
|  _  |/ ___ \| |\  | |_| |___) | | |_| | |\  | | |_| / ___ \| |/ ___ \ 
|_| |_/_/   \_\_| \_|____/|____/   \___/|_| \_| |____/_/   \_\_/_/   \_\

```

## The bike quest

The key to understanding how Amsterdam neighborhoods really friendly are is to measure it according to some effective metric, under reasonable assumptions. Let us say:

* To begin with, the more bikepath surface an area has the more bike friendly we expect it to be; relaxing things a little even if a surface field is provided, let us reason on the lines alone, no width.

* This is true, but it is kind of misleading if we take the large wasteland areas such as Westpoort: we must take the area into account too. Again, things like population and age should also matter, but let us give it a try like this - and we do not have that data anyway.

* This metric returns a little number for each neighborhood; what institutions like CBS (Centraal Bureau Statistiek) do is to reduce it into a one to five stars scale - that makes it easier to deal with.

* Once we have found a good result, we will save it for further processing. In our case, we will try to build the game matrix on it.

## Geometries

Input this query:

```sql
SELECT wkb_geometry FROM fietsnetwerk;
```

What does this column represent? This the geometry column, it actually encodes the shape of the line in the space, according to a specified coordinate reference system. These are numbers which uniquely position the line element on the map. In particular a standard format, the well-known binary (WKB) is used. To see things you have to convert it to the WKT (text) format.

Intuitively, to answer the unanswered question from the last exercise, for each patch of city we have to sum the length of the bikepath lines falling into it. Easier said than done. We would need something like:

```sql
SELECT p.name, ST_LENGTH(ST_Intersection(p.geom, l.geom))
FROM patches p, lines l
WHERE ST_IsValid(p.geom) AND ST_IsValid(l.geom) AND ST_Intersects(p.geom, l.geom);
```
Do not worry about the `ST` functions - those are PostGIS own geometrical functions, there for us to use. What happens if you pull out either `ST_IsValid` checks, or both? You will always get dirty data in real life!

Try to translate the query above into our tables: rename the template accordingly to come to the answer.

Hey are we missing something? We would like the total per neighborhood!

And further, normalize it by area; for simplicity, you may just divide by the area, `ST_Area`, then we can rescale from 1 to 5.
CEILING([COUNT] * 10.0 / (SELECT MAX([Count])  - MIN([Count]) + 1 FROM #Scale)) AS [Scale]

How does the final query look like?


## Bike-friendliness graph

then export to a csv
the read into spark
then apply prims mst

Ready? OK, time to create a table with the so-called CTAS syntax.

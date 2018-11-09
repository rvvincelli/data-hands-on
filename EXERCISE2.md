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

Try to translate the query above into our tables: rename the template accordingly to come to the answer. When you get the first version, add the following:

* the total per neighborhood
* normalize by area (use `ST_Area`)
* make it a `VIEW`

We are now ready to create a table with this; as the last refinement, let us rescale everything between 1 and 5; the general SQL for rescaling in `[1, N]` is:
`CEILING(<VALUE_TO_RESCALE> * <N-1> / ((SELECT MAX(<VALUE_TO_RESCALE>) FROM <TABLE>)  - (SELECT MIN(<VALUE_TO_RESCALE>) FROM <TABLE>))) AS <RESCALED_VALUE>`


## Bike-friendliness graph

To prepare for the next exercise, let us create a graph. A graph is a collection `G=(V,E)` where `V` are the vertices or nodes and `E` the relations or pairs between them. Actually we will create more than one graph, a collection. 

Our table entries will be of the form `A, B, bf_X, bf_X` for `X in 1 ... 5`: two neighborhoods are connected if they are next to each other on the map and they share the same bike friendliness.

To create this table:

```sql
CREATE TABLE hood_graphs AS SELECT a.hood AS a_hood, b.hood AS b_hood, a.bike_friend_scale AS a_scale, b.bike_friend_scale AS b_scale FROM bike_friendliness a CROSS JOIN bike_friendliness b WHERE a.hood != b.hood AND ST_Distance(a.hood_poly, b.hood_poly) < 0.01 AND a.bike_friend_scale = b.bike_friend_scale;
```

## Save the data

To close this exercise, we will save this data result. We did not setup the PostGIS container to be permanent which means that tables will be gone if we close it.

This is easily achieved with the following command in PostGIS:
`COPY hood_graphs TO '/media/host/data/bike_graphs.csv' DELIMITER ',' CSV HEADER;`

In the data directory, the CSV file will appear.

## See you soon

We can now move on to the next exercise!

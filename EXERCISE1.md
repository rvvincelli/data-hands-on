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

## Usage disclaimer

Everything has been tested on osx; in principle, a modern Docker setup on Windows is also fine, but your mileage, in terms of spaces, quotes and in general command-line things, may vary. Please do get in touch in case you get stuck!

## The story

The goal of your first data assignment is to support a new up and coming food delivery startup, *Slang-the-food.com* in taking an informed decision on what is the best strategy to enter the Amsterdam market.
Their fleet is entirely composed of bikes, so they would like to take over bike-friendly neighborhoods first.

A sworn enemy, *Deliver Foo*, does exactly the opposite by using Apecar's to deliver, and they would rather start from a car-friendly, or better bike-unfriendly, area.

Our goal is to come to supporting the client in finding an optimal takeover strategy, with the help of intuition and data.

## Exercise 1

In this exercise our goal is to create a data container starting from the data we have already. The container database will have a new table which we will create from the existing ones we import. This will represent the starting point of further investigation.

### Setup

The input data is a couple of publicly available datasets from Gemeente Amsterdam, see [here](https://data.amsterdam.nl/). They are in a well-known format for geographic information systems (GIS), the ESRI ShapeFile format. Such data may also be visualized, sliced and diced, played with special software, but let us take that for the end of the afternoon.

Other than a running Docker system on your computer, check perhaps that everying is up with a `docker container ls` you do not need anything else. Just to be sure, `docker stop` and `docker rm` any container you do not need.

We will use an all-in image containing among others:

* PostGIS. This is a GIS extension to the known PostgreSQL database system. It is the reference for databases containing geographical data, it supports a lot queries for example bounding boxes, location-based selections, coordinate transforms etc

* GDAL. Geospatial Data Abstraction Library is a Python library to manipulate geographical information. This means for example reading a shapefile and applying a function to each value of a data field, or extract the bounding lines of the polygon shapes.

## Booting the image

Let us try out a simple command on the container:

`docker run -t -i baffolobill/postgis-gdal -- ls`

You should see some known directories listed.

Now we will boot the image with two extra options - make sure you run this from the project root:

`docker run --name postgis -p 5432:5432 -v ./data:/media/host/data -d baffolobill/postgis-gdal`

or replace `.\data` with the right full path eg `"C:\Documents\somewhere\data"`.

Now perhaps you know it already, but the interesting options are:

* `-p <LOCAL_PORT>:<CONTAINER_PORT>` redirects the specified port on the host (your computer) to the specified port on the container; we will not need this but it is useful to know

* `-v <LOCAL_PATH>:<REMOTE_PATH>` mounts the specified local path on the container at a specified mount point; we will use this to make the data available on the container

* `-d` runs as a daemon (in the background, so that we can use the same terminal)

## Database: check

See what is inside the geo database:

`docker run -it --link <POSTGIS_CONTAINER_ID>:postgres --rm postgres sh -c "exec psql -h "$POSTGRES_PORT_5432_TCP_ADDR" -p "$POSTGRES_PORT_5432_TCP_PORT" -U postgres"`

without getting too complicated on this, we want to connect to the running database by using the standard client, so we run another instance attaching to our main one. Replace `<POSTGRES_CONTAINER_ID` with the id you see under `docker container ls`. The password is: `postgres`.

Now that you are in:

```
psql (11.0 (Debian 11.0-1.pgdg90+2))
Type "help" for help.

postgres=#
```

make yourself home! For example `\d` to list the current tables (there should be none). See where we ended up in with:
```sql
SELECT current_database();
```

## GDAL tooling: check

Let's get a shell on the running container:

`docker exec -it <POSTGIS_CONTAINER_ID> /bin/bash`

Now give:

`ogrinfo --formats | grep SQL`

you will see that PostgreSQL is a supported format.

## Our first import

Addition - data copy (fix for Windows not allowing the mount, perhaps ITS security; give this on your laptop black window):

`docker cp C:\Users\path\to\data <POSTGIS_CONTAINER_ID>:/media/host/data`

From the container shell, give:

`ls /media/host/data`

and see the shapefiles of two datasets, `buurten` and `fietsnetwerk`, containing the official Amsterdam neighborhoods and the bike paths network. One is made of polygons the other of lines.

The general syntax of the command to import our first table can be given as follows:
`ogr2ogr <MODE_1> <MODE_2> ... <MODE_N> -f <FORMAT> PG:"<CONNECTION_STRING>" <FILE_TO_IMPORT> -nln <DESTINATION_TABLE> -a_srs <COORDINATE_REFERENCE_SYSTEM>`

Full reference is available with `man ogr2ogr`. Some hints on how to fill this in:

* We want to `update` the destination database, `append`ing should it exist already
* A handy option to add after the modes is `-progress` to show a progress bar
* The format you have seen it above in the GDAL tool check
* Filepath: it must be absolute, for example `/abs/path/to/my.shp`
* Object names should always be meaningful, especially when you are sharing the data
* Use the modern dutch coordinate system `EPSG:28992`

A connection string for Postgres is of the following form: `dbname='<DATABASE_NAME>' host='<HOSTNAME>' port='<PORT>' user='<USER>' password='<PASSWORD>'`. You already know the user and password for the feel-yourself-home container command from above; database name too. `5432` is the default Postgres port. And finally, remind that the database is running locally - what is the hostname of `127.0.0.1`?

Finally keep in mind that typically command line tools in Linux and friends use `-s` (single dash) for short options and `--for-long-option`s (double dash); but sometimes tools still use ``-i-miss-one-dash` - the GDAL tools make this mistake too.

Once you found the right command, save it somewhere. Anyway it will stay in your shell history - pay attention to this when you are typing in passwords and secrets, no matter on your computer or a container.

If you cannot really get the switch right, see `secret_commands.txt` for the right command to import.

When you get it right you should see:
`0...10...20...30...40...50...60...70...80...90...100 - done.`

You may import the other table too - it does not matter which one you start with.

## Select all the stars

Get to the Postgres prompt again and type `\d` again: now you should see our two tables (the database has created two system tables too but that does not matter).

Give a classic:

```sql
SELECT * FROM buurten;
```

and you will see a bloat of text still to be made sense of. After the SQL lesson the most declarative language of them all has no secret for you. Would you then answer the following questions for me:

* How many neighborhoods does Amsterdam count?
* How many kilometers of bike paths in total can amsterdammers enjoy?
* Which is the neighborhood most bike-friendly neighborhood?

Now, the first two queries should go smooth, but what about the third? That sounds more complicated and indeed it is, because it leverages on the geometry of the tables as lines and polygons.

## On to the next

Very good team, it is time to go home since it is ten o'clock PM. Tomorrow we will start at 6:00 AM sharp with the second exercise.

In the Docker container, try this:

`sleep 1000`



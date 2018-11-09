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

## Where shall we start to colonize?

*Slang-the-food.com* wants to increases the chances of success in his Amsterdam adventure by focusing on selected areas where bikes are first-class citizens. We modeled bike friendliness by defining a specific coefficient.

A designated neighborhood is rather small in Amsterdam though, that is why we would like to suggest the client, at different bike-friendliness scales, wider areas, that is streaks of neighborhoods: in this way, having a larger areas, they can have potentially larger margins and route optimizations.

## Starting data

What we created in SQL is a collection of graphs: for a given bike friendliness scale, say 2, we have a number of rows representing friendly neighborhoods, they border each other and have the same bike friendliness 2.

We are interested, for given scale, possibly a high one like 5 or 4, to find *paths* connecting the different neighborhoods. This problem we are trying to solve can be reduced to a known one in graph theory, the largest clique problem: we want to find such group of connected neighborhoods, the largest one. It is known problem with a known solution - no need to reinvent the wheel, an implementation is out there. 

## Carrying out the computation

Our computation engine will be based on Docker again, and we will use `Apache Spark` as the large-scale framework. In our case it is just a few rows so no big data, but the code we will write will behave exactly the same on a large Spark cluster too - it will just go faster.

There is a lot to be said about Spark and the very-mentioned Hadoop, also in relation with Docker itself, but let us park it for now.

Boot and test the image with the sample Pi digits program:
`docker run --rm -it -p 4040:4040 gettyimages/spark bin/run-example SparkPi 10`

If all went well, you should see the string:
`Pi is roughly 3.1415111415111414`

We are now ready to import or graphs and find the most promising areas.

Setup a Spark in the background, pointing to our data directory:
`docker run --rm -it -p 4040:4040 -v $(pwd)/data:/media/host/data -d gettyimages/spark`

Get a shell on it, this time using the funny name entry under `NAMES` in the container list:
`docker exec -it <CONTAINER_FUNNY_NAME> /bin/bash`

Start `pyspark`: this is the Python Spark interactive console; pretty much like `python` but with the Spark backend and libraries.

We will now read the data into a data structure called Resilient Distribution Dataset (RDD). This is pretty much a big chunked array, with the chunks distributed around the nodes of our cluster. Sometimes you may want to use a more advanced form of RDD called Dataframe.

To import the data, follow this template:

```python
>>> bike_graphs = sc.textFile('/path/to/csv/file.csv', 4).map(lambda line: line.split("<SEPARATOR_CHARACTER>"))
```

What does the `4` mean? The minimum number of partitions. As we said, this is a partitioned structure. Each partition will be assigned to a cluster node. There is no fixed formula to decide how to split the data but, if we look at the table itself, we may take the educated guess that the 5th class is (very) small, and the others pretty equal in number. Do you agree? You may check and, eventually, adjust the number. In this example we have one single cluster node, so we ignore the cluster factor. But in a generic cluster, that must be taken into account, because they get distributed as we said.

Data is in:

```python
>>> bike_graphs
```

Question: could you print all the rows? Hint: `foreach` function and Python `lambda`.

At a first glance it looks like there are no class 5 or 4 islands: *Slang-the-food.com* will have to hand-pick those isolated neighborhoods and see if it is worth to focus in those little secluded neighborhoods.

As 1 is for really bike-unfriendly neighborhoods, where *Deliver Foo* is king, let us focus our efforts on class 3. Our task is to found the maximum graph cliques in these classes.
 
Can you create new RDD, keeping only the class 2 and 3 pairs? Use `filter`, again accepting a lambda. Recall that we imported everything in the string type.

```python
>>> bike_graphs_input = bike_graphs.filter(...
```

We can now apply the algorithm. We will present a result for class 3 first:

```python
>>> bike_graphs_input_three = bike_graphs_input.filter(...
```

The algorithm expects to have a the graph as a matrix called adjacency list:
`A_ij = 1 if v=(i,j) in E`

So we will have a square matrix of the size of our list of class-three neighborhoods and we will have a 1 whenever a pair of neigbhorhoods is known.

Check out the `bk.py` file in data; you may copy paste its functions.

## Summing it up

Next to the clique algorithm implementation, we have a few other helper functions.

Copy paste all of them, maybe one by one. Then give:

```python
>>> index_lookup = create_lookup(bike_graphs_input_three)
```

```python
>>> adjacency_matrix = create_matrix(bike_graphs_input_three, index_lookup)
```

```python
>>> nodes = list(index_lookup.values())
>>> nodes.sort()
```

```python
best_class_three_areas = bronk(adjacency_matrix, [], nodes, [])
```

Can you help me finding back the name of the areas?

```python
from_code_to_neighborhood = dict(zip(list(index_lookup.values()), list(index_lookup.keys())))
```
Now it is a matter of going down `best_class_three_areas` with two for cycles.

## That's it!

This ends the exercise as well as the advisory assignment to *Slang-the-food.com*!

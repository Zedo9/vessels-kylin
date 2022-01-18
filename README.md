# Vessels Voyages

AIS Data manipulation and OLAP Analysis using Apache Kylin.

## Getting started

1. Download a sample dataset to work on. The list of available datasets is listed [here](http://web.ais.dk/aisdata/) and updated daily (the shell script provided under `input` will default to the data of 2021-12-23).

2. Navigate to `input` and generate the required CSV files for each table (Make sure to update the `filepath` variable inside the python script, depending on the file you downloaded)

```sh
$ python3 generate_csvs.py
```

3. Run `docker-compose up` in the root directory of this repo and give it at least a full minute for all the services to load properly.

4. Once the `Apache Kylin` container is properly started, we will access it using bash from another terminal by running

```sh
$ docker exec -it kylin bash
```

5. We will now create the Database and needed tables on hive as well as insert data into them. From inside the container run

```sh
$ hive -f /input/hive-setup.sh
```

6. Your data is now fully setup and you can use Kylin by navigating to `http://localhost:7070/kylin/login`. You will be able to create a new project, import the AIS Database and start building you cubes (Use [this](http://kylin.incubator.apache.org/docs/tutorial/create_cube.html) guide on the official documentation for the cube and model wizard).

- _The default credentials for logging in to the Apache Kylin Dashboard are : username : ADMIN | password : KYLIN_
- _When creating the cube and model, make sure to setup the proper joins on foreign keys_ :
  - `id` from the `vessels` table with `vessel_id` from the `trips` table
  - `trip_id` from the `trip_trajectory` table with `id` from the `trips` table

7. If you want to perform calculations such as trip duration, distance, avg speeds... you will need to setup the ESRI Hadoop libraries in Hive. From inside the container run

```sh
$ chmod +x /input/esri-setup.sh
$ /input/esri-setup.sh
```

and let it download its dependencies and build the required jars (It may take up to 25-30 minutes - **If the script fails when downloading dependencies just rerun it (The issue is caused by Maven servers)**).

Once the build is finished, from inside the Kylin container run `hive` and paste the following sql script, it will load the ESRI libraries and generate useful functions :

```sql
use ais;

CREATE FUNCTION ST_Aggr_ConvexHull AS  "com.esri.hadoop.hive.ST_Aggr_ConvexHull" ;
CREATE FUNCTION ST_Aggr_Intersection    AS  "com.esri.hadoop.hive.ST_Aggr_Intersection"   ;
CREATE FUNCTION ST_Aggr_Union   AS  "com.esri.hadoop.hive.ST_Aggr_Union"  ;
CREATE FUNCTION ST_Area AS  "com.esri.hadoop.hive.ST_Area"    ;
CREATE FUNCTION ST_AsBinary AS  "com.esri.hadoop.hive.ST_AsBinary"    ;
CREATE FUNCTION ST_AsGeoJson    AS  "com.esri.hadoop.hive.ST_AsGeoJson"   ;
CREATE FUNCTION ST_AsJson   AS  "com.esri.hadoop.hive.ST_AsJson"  ;
CREATE FUNCTION ST_AsShape  AS  "com.esri.hadoop.hive.ST_AsShape" ;
CREATE FUNCTION ST_AsText   AS  "com.esri.hadoop.hive.ST_AsText"  ;
CREATE FUNCTION ST_Bin  AS  "com.esri.hadoop.hive.ST_Bin" ;
CREATE FUNCTION ST_BinEnvelope  AS  "com.esri.hadoop.hive.ST_BinEnvelope" ;
CREATE FUNCTION ST_Boundary AS  "com.esri.hadoop.hive.ST_Boundary"    ;
CREATE FUNCTION ST_Buffer   AS  "com.esri.hadoop.hive.ST_Buffer"  ;
CREATE FUNCTION ST_Centroid AS  "com.esri.hadoop.hive.ST_Centroid"    ;
CREATE FUNCTION ST_Contains AS  "com.esri.hadoop.hive.ST_Contains"    ;
CREATE FUNCTION ST_ConvexHull   AS  "com.esri.hadoop.hive.ST_ConvexHull"  ;
CREATE FUNCTION ST_CoordDim AS  "com.esri.hadoop.hive.ST_CoordDim"    ;
CREATE FUNCTION ST_Crosses  AS  "com.esri.hadoop.hive.ST_Crosses" ;
CREATE FUNCTION ST_Difference   AS  "com.esri.hadoop.hive.ST_Difference"  ;
CREATE FUNCTION ST_Dimension    AS  "com.esri.hadoop.hive.ST_Dimension"   ;
CREATE FUNCTION ST_Disjoint AS  "com.esri.hadoop.hive.ST_Disjoint"    ;
CREATE FUNCTION ST_Distance AS  "com.esri.hadoop.hive.ST_Distance"    ;
CREATE FUNCTION ST_EndPoint AS  "com.esri.hadoop.hive.ST_EndPoint"    ;
CREATE FUNCTION ST_Envelope AS  "com.esri.hadoop.hive.ST_Envelope"    ;
CREATE FUNCTION ST_EnvIntersects    AS  "com.esri.hadoop.hive.ST_EnvIntersects"   ;
CREATE FUNCTION ST_Equals   AS  "com.esri.hadoop.hive.ST_Equals"  ;
CREATE FUNCTION ST_ExteriorRing AS  "com.esri.hadoop.hive.ST_ExteriorRing"    ;
CREATE FUNCTION ST_GeodesicLengthWGS84  AS  "com.esri.hadoop.hive.ST_GeodesicLengthWGS84" ;
CREATE FUNCTION ST_GeomCollection   AS  "com.esri.hadoop.hive.ST_GeomCollection"  ;
CREATE FUNCTION ST_Geometry AS  "com.esri.hadoop.hive.ST_Geometry"    ;
CREATE FUNCTION ST_GeometryN    AS  "com.esri.hadoop.hive.ST_GeometryN"   ;
CREATE FUNCTION ST_GeometryType AS  "com.esri.hadoop.hive.ST_GeometryType"    ;
CREATE FUNCTION ST_GeomFromGeoJson  AS  "com.esri.hadoop.hive.ST_GeomFromGeoJson" ;
CREATE FUNCTION ST_GeomFromJson AS  "com.esri.hadoop.hive.ST_GeomFromJson"    ;
CREATE FUNCTION ST_GeomFromShape    AS  "com.esri.hadoop.hive.ST_GeomFromShape"   ;
CREATE FUNCTION ST_GeomFromText AS  "com.esri.hadoop.hive.ST_GeomFromText"    ;
CREATE FUNCTION ST_GeomFromWKB  AS  "com.esri.hadoop.hive.ST_GeomFromWKB" ;
CREATE FUNCTION ST_InteriorRingN    AS  "com.esri.hadoop.hive.ST_InteriorRingN"   ;
CREATE FUNCTION ST_Intersection AS  "com.esri.hadoop.hive.ST_Intersection"    ;
CREATE FUNCTION ST_Intersects   AS  "com.esri.hadoop.hive.ST_Intersects"  ;
CREATE FUNCTION ST_Is3D AS  "com.esri.hadoop.hive.ST_Is3D"    ;
CREATE FUNCTION ST_IsClosed AS  "com.esri.hadoop.hive.ST_IsClosed"    ;
CREATE FUNCTION ST_IsEmpty  AS  "com.esri.hadoop.hive.ST_IsEmpty" ;
CREATE FUNCTION ST_IsMeasured   AS  "com.esri.hadoop.hive.ST_IsMeasured"  ;
CREATE FUNCTION ST_IsRing   AS  "com.esri.hadoop.hive.ST_IsRing"  ;
CREATE FUNCTION ST_IsSimple AS  "com.esri.hadoop.hive.ST_IsSimple"    ;
CREATE FUNCTION ST_Length   AS  "com.esri.hadoop.hive.ST_Length"  ;
CREATE FUNCTION ST_LineFromWKB  AS  "com.esri.hadoop.hive.ST_LineFromWKB" ;
CREATE FUNCTION ST_LineString   AS  "com.esri.hadoop.hive.ST_LineString"  ;
CREATE FUNCTION ST_M    AS  "com.esri.hadoop.hive.ST_M"   ;
CREATE FUNCTION ST_MaxM AS  "com.esri.hadoop.hive.ST_MaxM"    ;
CREATE FUNCTION ST_MaxX AS  "com.esri.hadoop.hive.ST_MaxX"    ;
CREATE FUNCTION ST_MaxY AS  "com.esri.hadoop.hive.ST_MaxY"    ;
CREATE FUNCTION ST_MaxZ AS  "com.esri.hadoop.hive.ST_MaxZ"    ;
CREATE FUNCTION ST_MinM AS  "com.esri.hadoop.hive.ST_MinM"    ;
CREATE FUNCTION ST_MinX AS  "com.esri.hadoop.hive.ST_MinX"    ;
CREATE FUNCTION ST_MinY AS  "com.esri.hadoop.hive.ST_MinY"    ;
CREATE FUNCTION ST_MinZ AS  "com.esri.hadoop.hive.ST_MinZ"    ;
CREATE FUNCTION ST_MLineFromWKB AS  "com.esri.hadoop.hive.ST_MLineFromWKB"    ;
CREATE FUNCTION ST_MPointFromWKB    AS  "com.esri.hadoop.hive.ST_MPointFromWKB"   ;
CREATE FUNCTION ST_MPolyFromWKB AS  "com.esri.hadoop.hive.ST_MPolyFromWKB"    ;
CREATE FUNCTION ST_MultiLineString  AS  "com.esri.hadoop.hive.ST_MultiLineString" ;
CREATE FUNCTION ST_MultiPoint   AS  "com.esri.hadoop.hive.ST_MultiPoint"  ;
CREATE FUNCTION ST_MultiPolygon AS  "com.esri.hadoop.hive.ST_MultiPolygon"    ;
CREATE FUNCTION ST_NumGeometries    AS  "com.esri.hadoop.hive.ST_NumGeometries"   ;
CREATE FUNCTION ST_NumInteriorRing  AS  "com.esri.hadoop.hive.ST_NumInteriorRing" ;
CREATE FUNCTION ST_NumPoints    AS  "com.esri.hadoop.hive.ST_NumPoints"   ;
CREATE FUNCTION ST_Overlaps AS  "com.esri.hadoop.hive.ST_Overlaps"    ;
CREATE FUNCTION ST_Point    AS  "com.esri.hadoop.hive.ST_Point"   ;
CREATE FUNCTION ST_PointFromWKB AS  "com.esri.hadoop.hive.ST_PointFromWKB"    ;
CREATE FUNCTION ST_PointN   AS  "com.esri.hadoop.hive.ST_PointN"  ;
CREATE FUNCTION ST_PointZ   AS  "com.esri.hadoop.hive.ST_PointZ"  ;
CREATE FUNCTION ST_PolyFromWKB  AS  "com.esri.hadoop.hive.ST_PolyFromWKB" ;
CREATE FUNCTION ST_Polygon  AS  "com.esri.hadoop.hive.ST_Polygon" ;
CREATE FUNCTION ST_Relate   AS  "com.esri.hadoop.hive.ST_Relate"  ;
CREATE FUNCTION ST_SetSRID  AS  "com.esri.hadoop.hive.ST_SetSRID" ;
CREATE FUNCTION ST_SRID AS  "com.esri.hadoop.hive.ST_SRID"    ;
CREATE FUNCTION ST_StartPoint   AS  "com.esri.hadoop.hive.ST_StartPoint"  ;
CREATE FUNCTION ST_SymmetricDiff    AS  "com.esri.hadoop.hive.ST_SymmetricDiff"   ;
CREATE FUNCTION ST_Touches  AS  "com.esri.hadoop.hive.ST_Touches" ;
CREATE FUNCTION ST_Union    AS  "com.esri.hadoop.hive.ST_Union"   ;
CREATE FUNCTION ST_Within   AS  "com.esri.hadoop.hive.ST_Within"  ;
CREATE FUNCTION ST_X    AS  "com.esri.hadoop.hive.ST_X"   ;
CREATE FUNCTION ST_Y    AS  "com.esri.hadoop.hive.ST_Y"   ;
CREATE FUNCTION ST_Z    AS  "com.esri.hadoop.hive.ST_Z"   ;

add jar hdfs:///lib/spatial-sdk-hive.jar;
add jar hdfs:///lib/spatial-sdk-json.jar;
add jar hdfs:///lib/esri-geometry-api.jar;
```

You can test that your functions have been correctly generated by running one of the queries in the `queries` folder.

## Drawing trip trajectories on a map

You can use the `jupyter` container to draw trip trajectories and perform further analysis (Make sure you heave created a project on Kylin with the name `ais` and imported the database first). Sample code is provided in the `notebooks\mynotebook.ipynb`. You can use it directly by navigating to the jupyter Web page.

- Find the URL containing the token by running on your machine

```sh
$ docker logs jupyter
```

and use the link starting with `http://127.0.0.1:8888/?token=*************`.

## Useful links

- [Apache Kylin v4 Documentation](https://kylin.apache.org/docs/index.html)
- [Geo spatial data support for Hive](https://www.oraylis.de/blog/2015/geo-spatial-data-support-for-hive)
- [Open source geospatial UDFs](https://www.alibabacloud.com/help/doc-detail/147156.htm)
- [Hive SQL](https://www.tutorialspoint.com/hive/index.htm)
- [ipyleaflet Documentation](https://ipyleaflet.readthedocs.io/en/latest/)
- [Hive Examples](https://sparkbyexamples.com/apache-hive/hive-load-csv-file-into-table/)
- [Kylin Python Client](https://kylin.apache.org/docs/tutorial/kylin_client_tool.html)
- [Running Kylin on Docker](https://kylin.apache.org/docs/install/kylin_docker.html)

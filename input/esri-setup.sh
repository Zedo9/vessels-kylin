#!/bin/sh

cd /tmp
mkdir gis
cd gis
mkdir framework
mkdir api

# download and build framework
hdfs dfs -mkdir /lib
cd framework
wget https://github.com/Esri/spatial-framework-for-hadoop/archive/master.zip
unzip master
cd spatial-framework-for-hadoop-master
mvn clean package -DskipTests -P java-8,hadoop-2.8
mv hive/target/spatial-sdk-hive-2.2.1-SNAPSHOT.jar /hive/target/spatial-sdk-hive.jar
cp hive/target/spatial-sdk-hive.jar /home/admin/apache-hive-1.2.1-bin/lib/spatial-sdk-hive.jar

mv json/target/spatial-sdk-json-2.2.1-SNAPSHOT.jar json/target/spatial-sdk-json.jar
cp json/target/spatial-sdk-json.jar /home/admin/apache-hive-1.2.1-bin/lib/spatial-sdk-json.jar

hdfs dfs -put hive/target/spatial-sdk-hive-2.2.1-SNAPSHOT.jar /lib
hdfs dfs -put json/target/spatial-sdk-json-2.2.1-SNAPSHOT.jar /lib

# download and build api
cd /tmp/gis/api
wget https://repo1.maven.org/maven2/com/esri/geometry/esri-geometry-api/2.2.1/esri-geometry-api-2.2.1.jar
mv esri-geometry-api-2.2.1.jar esri-geometry-api.jar
cp esri-geometry-api.jar /home/admin/apache-hive-1.2.1-bin/lib/esri-geometry-api.jar

hdfs dfs -put esri-geometry-api.jar /lib
# clean up
cd /tmp
rm -rf gis
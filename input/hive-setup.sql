CREATE DATABASE if not exists AIS;

use AIS;

CREATE TABLE IF NOT EXISTS trips (
 id BIGINT,
 vessel_id BIGINT,
 destination string,
 ETA timestamp,
 source string,
 duration double,
 distance double
 )
 ROW FORMAT DELIMITED
 FIELDS TERMINATED BY ','
 TBLPROPERTIES("skip.header.line.count"="1");


CREATE TABLE IF NOT EXISTS vessels (
 id BIGINT,
 mmsi string,
 imo string,
 callsign string,
 vessel_name string,
 ship_type string,
 cargo_type string,
 width double,
 height double,
 size_A double,
 size_B double,
 size_C double,
 size_D double
 )
 ROW FORMAT DELIMITED
 FIELDS TERMINATED BY ','
 TBLPROPERTIES("skip.header.line.count"="1");


CREATE TABLE IF NOT EXISTS trip_trajectory (
 id BIGINT,
 trip_id BIGINT,
 ts timestamp,
 lat double,
 lon double,
 stat string,
 ROT double,
 SOG double,
 COG double,
 heading double
 )
 ROW FORMAT DELIMITED
 FIELDS TERMINATED BY ','
 TBLPROPERTIES("skip.header.line.count"="1");



LOAD DATA LOCAL INPATH '/input/vessels.csv' INTO TABLE vessels;
LOAD DATA LOCAL INPATH '/input/trips.csv' INTO TABLE trips;
LOAD DATA LOCAL INPATH '/input/trip_snapshots.csv' INTO TABLE trip_trajectory;
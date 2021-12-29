select trip_id, min(ts) start_time, max(ts) end_time, Sum(Distance) distance, Sum(Distance)/1000 * (3600.0/Sum(time_passed)) avg_speed
from (
  select trip_id, ts, time_passed, ST_GeodesicLengthWGS84(ST_SetSRID(L,4326)) Distance
  from (
    select trip_id, ts, unix_timestamp(ts) - unix_timestamp(lag(ts,1) over (partition by trip_id order by ts)) time_passed, lat, lon, ST_LineString(prev_longitude, prev_latitude, lon, lat) L
    from (
      select trip_id, ts, lat, lon, 
        lag(lat,1) over (partition by trip_id order by ts) prev_latitude, 
        lag(lon,1) over (partition by trip_id order by ts) prev_longitude 
      from trip_trajectory
    ) Sub
  ) Sub1
) Sub2
group by trip_id;
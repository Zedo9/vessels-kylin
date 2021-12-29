select trip_id, unix_timestamp(ts) - unix_timestamp(ts_first) trip_duration
from (
  select trip_id,ts, first_value(ts) over (partition by trip_id order by ts) ts_first, row_number() over (partition by trip_id order by ts desc) lnr
  from trip_trajectory
) Sub
Where lnr=1;


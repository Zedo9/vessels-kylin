import csv

# Function used to convert timestamp to a proper format suppored by hive
def convert_timestamp(ts_string:str):
    date = ts_string.split(" ")[0]
    splitted_date = date.split("/")
    day = splitted_date[0]
    month = splitted_date[1]
    year = splitted_date[2]
    new_date = "{}-{}-{}".format(year,month,day)
    return "{} {}".format(new_date, ts_string.split(" ")[1])


# This class is used to ensure that every trip with the same destination, vessel and ETA is only saved once
class trip :
    def __init__(self, eta, destination, mmsi):
        self.eta = eta
        self.destination = destination
        self.mmsi = mmsi
    def __hash__(self):
        return hash(str(self.eta+self.destination+self.mmsi))

    def __eq__(self, other):
        return (self.eta == other.eta and self.destination == other.destination and self.mmsi == other.mmsi)

filepath = "aisdk-2021-12-23.csv"
# filepath = "minimal.csv"
vessels_data = {}
trips_data = {}
trip_snapshots = {}
vessels_count = 0
trips_count = 0
trips_snapshots_count = 0

"""
1. Timestamp   Timestamp from the AIS basestation, format: 31/12/2015 23:59:59 
2. Type of mobile   Describes what type of target this message is received from (class A AIS Vessel, Class B AIS vessel, etc)
* 3. MMSI    MMSI number of vessel
4. Latitude   Latitude of message report (e.g. 57,8794)
5. Longitude   Longitude of message report (e.g. 17,9125)
6. Navigational status  Navigational status from AIS message if available, e.g.: 'Engaged in fishing', 'Under way using engine', mv.
7. ROT    Rot of turn from AIS message if available
8. SOG    Speed over ground from AIS message if available
9. COG    Course over ground from AIS message if available
10. Heading   Heading from AIS message if available
* 11. IMO    IMO number of the vessel
* 12. Callsign   Callsign of the vessel 
* 13. Name    Name of the vessel
* 14. Ship type   Describes the AIS ship type of this vessel 
15. Cargo type   Type of cargo from the AIS message 
* 16. Width    Width of the vessel
* 17. Length    Lenght of the vessel 
18. Type of position fixing device Type of positional fixing device from the AIS message 
19. Draught   Draugth field from AIS message
20. Destination   Destination from AIS message
21. ETA    Estimated Time of Arrival, if available  
22. Data source type  Data source type, e.g. AIS
* 23. Size A    Length from GPS to the bow
* 24. Size B    Length from GPS to the stern
* 25. Size C    Length from GPS to starboard side
* 26. Size D    Length from GPS to port side
"""

vessel_csv_cols = ('id','mmsi','imo', 'callsign', 'name', 'ship_type', 'cargo_type', 'width', 'length', 'size_A', 'size_B', 'size_C', 'size_D')

trip_csv_rows = ('id', 'vessel_id', 'destination', 'ETA', 'source', 'duration', 'distance')

trip_trajectory_csv_rows = ('id', 'trip_id', 'timestamp', 'lat', 'lon', 'status', 'ROT', 'SOG', 'COG', 'heading')

with open(filepath, "r") as source:
    reader = csv.reader(source)
    for r in reader:
        # ignore first header row
        if (r[0] == "# Timestamp") :
            continue
        # Check if destination is defined
        if r[19] not in ('', 'UNKNOWN', ':', '0') and r[5] != 'Unknown value' :
            # Check if we already saved the vessel data
            if (vessels_data.get(r[2]) == None) :
                vessels_data[r[2]] = {
                    'id' : vessels_count,
                    'mmsi' : r[2],
                    'imo' : r[10],
                    'callsign' : r[11],
                    'name' : r[12], 
                    'ship_type' : r[13],
                    'cargo_type' : r[14],
                    'width' : r[15],
                    'length' : r[16],
                    'size_A' : r[22],
                    'size_B' : r[23],
                    'size_C' : r[24],
                    'size_D' : r[25]
                }                
                vessels_count += 1
            # Check if we already saved a trip with this destination
            current_trip = trip(r[20], r[19], r[2])
            if trips_data.get(current_trip) == None :
                timestamp = r[20]
                if (timestamp != '') :
                    timestamp = convert_timestamp(timestamp)
                trips_data[current_trip]= {
                    'id' : trips_count,
                    'vessel_id': vessels_data[r[2]]['id'],
                    'destination' : r[19],
                    'ETA' : timestamp
                }
                trips_count += 1
            timestamp = r[0]
            if (timestamp != '') :
                timestamp = convert_timestamp(timestamp)
            trip_snapshots[trips_snapshots_count]= {
                'id':trips_snapshots_count,
                'trip_id':trips_data[current_trip]['id'],
                'timestamp':timestamp,
                'lat': r[3],
                'lon':r[4],
                'status':r[5],
                'ROT':r[6],
                'SOG':r[7],
                'COG':r[8],
                'heading':r[9]
            }
            trips_snapshots_count += 1

# create vessels csv
with open("vessels.csv", "w") as result:
        writer = csv.writer(result)
        writer.writerow(vessel_csv_cols)
        for mmsi in vessels_data.keys():
            writer.writerow((vessels_data[mmsi][column] for column in vessel_csv_cols))

# create trips csv
with open("trips.csv", "w") as result:
        writer = csv.writer(result)
        writer.writerow(trip_csv_rows)
        for i_trip in trips_data.values():
            writer.writerow((i_trip['id'], i_trip['vessel_id'], i_trip['destination'], i_trip['ETA']))

# create trip_snapshots csv
with open("trip_snapshots.csv", "w") as result:
        writer = csv.writer(result)
        writer.writerow(trip_trajectory_csv_rows)
        for snapshot in trip_snapshots.values():
            writer.writerow((snapshot[col] for col in trip_trajectory_csv_rows ))
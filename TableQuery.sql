CREATE OR REPLACE TABLE caramel-brook-436419-s4.taxi_data_id.table_data AS (
SELECT 
  f.VendorID,
  -- Directly cast ISO 8601 datetime strings to DATETIME
  CAST(d.tpep_pickup_datetime AS DATETIME) AS tpep_pickup_datetime,
  CAST(d.tpep_dropoff_datetime AS DATETIME) AS tpep_dropoff_datetime,
  p.passenger_count,
  t.trip_distance,
  r.RatecodeName,
  pick.PULocationID,
  dp.DOLocationID,
  pay.PaymentType,
  f.fare_amount,
  f.extra,
  f.mta_tax,
  f.tip_amount,
  f.tolls_amount,
  f.improvement_surcharge,
  f.total_amount
FROM 
  `caramel-brook-436419-s4.taxi_data_id.fact_table` f
JOIN `caramel-brook-436419-s4.taxi_data_id.datetime_dim` d ON f.datetime_id=d.datetime_id
JOIN `caramel-brook-436419-s4.taxi_data_id.passenger_count_dim` p ON p.passenger_count_id=f.passenger_count_id  
JOIN `caramel-brook-436419-s4.taxi_data_id.trip_distance_dim` t ON t.trip_distance_id=f.trip_distance_id  
JOIN `caramel-brook-436419-s4.taxi_data_id.rate_code_dim` r ON r.rate_code_id=f.rate_code_id  
JOIN `caramel-brook-436419-s4.taxi_data_id.PULocationId_dim` pick ON pick.pu_location_id = f.pu_location_id
JOIN `caramel-brook-436419-s4.taxi_data_id.DOLocationId_dim` dp ON dp.do_location_id = f.do_location_id
JOIN `caramel-brook-436419-s4.taxi_data_id.payment_type_dim` pay ON pay.payment_type_id=f.payment_type_id
);

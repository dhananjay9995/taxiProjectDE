import pandas as pd
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(df, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your transformation logic here
    #reducing to 10% because of memory and cpu issue
   #df = df.sample(frac=0.1, random_state=1) 

    df['tpep_pickup_datetime']= pd.to_datetime(df['tpep_pickup_datetime'])
    df['tpep_dropoff_datetime']= pd.to_datetime(df['tpep_dropoff_datetime'])

    df= df.drop_duplicates().reset_index(drop=True)

    df['trip_id']=df.index

    datetime_dim = df[['tpep_pickup_datetime','tpep_dropoff_datetime']].drop_duplicates().reset_index(drop=True)
    datetime_dim['pickup_day']= datetime_dim['tpep_pickup_datetime'].dt.day
    datetime_dim['pickup_month']= datetime_dim['tpep_pickup_datetime'].dt.month
    datetime_dim['pickup_year']= datetime_dim['tpep_pickup_datetime'].dt.year
    datetime_dim['pickup_hour']= datetime_dim['tpep_pickup_datetime'].dt.hour
    datetime_dim['pickup_weekday']= datetime_dim['tpep_pickup_datetime'].dt.weekday
    datetime_dim['dropoff_day']= datetime_dim['tpep_dropoff_datetime'].dt.day
    datetime_dim['dropoff_month']= datetime_dim['tpep_dropoff_datetime'].dt.month
    datetime_dim['dropoff_year']= datetime_dim['tpep_dropoff_datetime'].dt.year
    datetime_dim['dropoff_hour']= datetime_dim['tpep_dropoff_datetime'].dt.hour
    datetime_dim['dropoff_weekday']= datetime_dim['tpep_dropoff_datetime'].dt.weekday

    datetime_dim['datetime_id'] = datetime_dim.index

    passenger_count_dim = df[['passenger_count']].drop_duplicates().reset_index(drop=True)
    passenger_count_dim['passenger_count_id'] = passenger_count_dim.index
    passenger_count_dim = passenger_count_dim[['passenger_count_id','passenger_count']]

    trip_distance_dim = df[['trip_distance']].drop_duplicates().reset_index(drop=True)
    trip_distance_dim['trip_distance_id'] = trip_distance_dim.index
    trip_distance_dim = trip_distance_dim[['trip_distance_id','trip_distance']]

    RateCodeID = {
        1: "Standard rate",
        2: "JFK",
        3: "Newark",
        4: "Nassau or Westchester",
        5: "Negotiated fare",
        6: "Group ride"
    }
    rate_code_dim = df[['RatecodeID']].drop_duplicates().reset_index(drop=True)
    rate_code_dim['RatecodeName'] = rate_code_dim['RatecodeID'].map(RateCodeID)
    rate_code_dim['rate_code_id'] = rate_code_dim.index
    rate_code_dim = rate_code_dim[['rate_code_id','RatecodeID','RatecodeName']]

    payment_type_dic = {
        1: "Credit card",
        2: "Cash",
        3: "No charge",
        4: "Disputer",
        5: "Unknown",
        6: "Voided trip"
    }
    payment_type_dim = df[['payment_type']].drop_duplicates().reset_index(drop=True)
    payment_type_dim['PaymentType'] = payment_type_dim['payment_type'].map(payment_type_dic)
    payment_type_dim['payment_type_id'] = payment_type_dim.index
    payment_type_dim = payment_type_dim[['payment_type_id','payment_type','PaymentType']]

    PULocationId_dim = df[['PULocationID']].drop_duplicates().reset_index(drop=True)
    PULocationId_dim['pu_location_id'] = PULocationId_dim.index
    PULocationId_dim = PULocationId_dim[['pu_location_id','PULocationID']]

    DOLocationId_dim = df[['DOLocationID']].drop_duplicates().reset_index(drop=True)
    DOLocationId_dim['do_location_id'] = DOLocationId_dim.index
    DOLocationId_dim = DOLocationId_dim[['do_location_id','DOLocationID']]

    fact_table =df.merge(datetime_dim,on=['tpep_pickup_datetime'])\
                .merge(passenger_count_dim,on='passenger_count')\
                .merge(trip_distance_dim,on='trip_distance')\
                .merge(rate_code_dim,on='RatecodeID')\
                .merge(payment_type_dim,on='payment_type')\
                .merge(PULocationId_dim,on='PULocationID')\
                .merge(DOLocationId_dim,on='DOLocationID')\
                [['VendorID','datetime_id','passenger_count_id','trip_distance_id','pu_location_id','do_location_id','rate_code_id',
                'payment_type_id','fare_amount','store_and_fwd_flag','extra','mta_tax','tip_amount','tolls_amount',
                'improvement_surcharge','total_amount','congestion_surcharge','Airport_fee']]
    
    
    return {
        "fact_table": fact_table,
        "datetime_dim": datetime_dim,
        "passenger_count_dim": passenger_count_dim,
        "trip_distance_dim": trip_distance_dim,
        "rate_code_dim": rate_code_dim,
        "payment_type_dim": payment_type_dim,
        "PULocationId_dim": PULocationId_dim,
        "DOLocationId_dim": DOLocationId_dim,
    }
    print(fact_table)


    

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'

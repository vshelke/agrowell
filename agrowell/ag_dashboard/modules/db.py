import rethinkdb as r
from . import formula 
import pandas as pd
import json, datetime, time

# make sure the database is indexed
host = 'localhost'
port = 28015
db = 'farm'
batch = 950

conn = r.connect(host=host, port=port, db=db)

def streamData(plant):
    yield "["
    for chunk in r.table(plant).order_by('timestamp').run(conn):
        data = { 'time': chunk['timestamp'], 'moisture': chunk['moisture'] }
        yield json.dumps(data) + ',' 
    yield json.dumps(data) + "]"

def getDF(plant, start, end):
    data = []
    try:
        for chunk in r.table(plant).between(start, end, index='timestamp').order_by('timestamp').run(conn):
            data.append({'time': chunk['timestamp'], 'moisture': chunk['moisture'],
                        'temperature': chunk['temperature'], 'humidity': chunk['humidity'],
                        'day': chunk['day']})
        df = pd.DataFrame(data, columns=['time', 'moisture', 'temperature', 'humidity', 'day'])
        df['moisture'] = df['moisture'].apply(lambda x: ((x/1023) * 100)) # revisit this for new plant
    except:
        return []
    return df
    
def getData(plant, date):
    end = date + datetime.timedelta(days=1)
    start = date - datetime.timedelta(days=1)
    df_present = getDF(plant, time2epoch(date), time2epoch(end))
    df_previous = getDF(plant, time2epoch(start), time2epoch(date))
    if not df_present.empty and not df_previous.empty:
        raw = df_present
        df_present = df_present.loc[::batch]
        df_previous = df_previous.loc[::batch]
        _, coef_previous = formula.getPredicted(df_previous)
        predict_present, coef_present = formula.getPredicted(df_present)
        growth = formula.getGrowthRate(coef_present, coef_previous)
        transpiration = formula.getTranspirationRate(raw)
        suitable = formula.getSuitability(raw)
        stamp = pd.to_datetime(df_present['time'], unit='s').to_json(orient='records')
        dump = {
            'status': 'success',
            'growth': growth,
            'transpiration': transpiration,
            'suitable': suitable,
            'time': json.loads(stamp),
            'moisture': json.loads(df_present['moisture'].to_json(orient='records')),
            'temperature': json.loads(df_present['temperature'].to_json(orient='records')),
            'humidity': json.loads(df_present['humidity'].to_json(orient='records')),
            'day': json.loads(df_present['day'].to_json(orient='records')),
            'predicted': json.loads(predict_present.to_json(orient='records')),
        }
        return json.dumps(dump)
    else:
        return json.dumps({
            'status': 'fail',
            'message': 'Error occured!'
        })

def time2epoch(x):
    return int(time.mktime(x.timetuple()))

import psycopg2
import os

DB_HOST = os.getenv('DB_HOST', 'postgresql://urluser:testing@localhost:5432/test')

conn = psycopg2.connect(DB_HOST)
conn.autocommit = True

def runQuery(query, data=()):
    cur = conn.cursor()
    cur.execute(query, data)
    return cur.fetchall()
    

# adding aditional params directly cause that's the best I can do :P
def addQueryParams(query, params):
    query += f"or grossing=\'{params['searchToken']}\'"
    return query


def dbsearch(params):
    query = (
        "select * from movies where name ilike '%%' || (%s) || '%%' "
    )
    data = (params['name'],)

    # parse additional params
    query = addQueryParams(query, params)
    res = []
    try:
        res = list(runQuery(query, data))
        if len(res) == 0:
            return [{'err': "Couldn't find anything... sadness :("}]
    except psycopg2.Error as e:
        print(e)
        return [{'err': "Error occurred in postgres db"}]

    # convert back to json
    res = [{'name': sequel[1], 'key': sequel[0], 'val': sequel[2]} for sequel in res]
    return res
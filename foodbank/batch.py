import psycopg2
import psycopg2.extras
from dateutil.relativedelta import relativedelta
from datetime import datetime
import pytz

tz = pytz.timezone('Asia/Kolkata')

conn = psycopg2.connect(database="foodbank", user = "postgres", password = "postgres", host = "localhost")
cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
query="select * from food_lock"
cur.execute(query)
result = cur.fetchall()
for i in result:
    query="select * from foodinfo where foodid=%s"
    cur.execute(query,(i['fid'],))
    info = cur.fetchone()
    info[5]=info[5].astimezone(tz)
    print(info[5])
    print(datetime.now(tz))
    if datetime.now(tz) > (info['created_timestamp']+ relativedelta(hours=i['timelimit'])):
        if i['status'] == 'not_picked':
            query="select quantity from food_unlock where fid=%s"
            cur.execute(query,(i['fid'],))
            food=cur.fetchone()
            query="update food_unlock set quantity=%s where fid=%s"
            food[0]=food[0]+i['food_quantity']
            cur.execute(query,(food[0],i['fid']))
            cur.execute('commit')
            query="update food_lock set status='obsolete' where fid=%s and lock_id=%s"
            cur.execute(query,(i['fid'],i['lock_id']))
            cur.execute('commit')
    else:
        pass

cur.close()
conn.close()

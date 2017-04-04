from flask import Flask
app = Flask(__name__)
import psycopg2
import traceback
app.config.from_pyfile('_config.py')

while True:
    query = """
    INSERT into public_page_views (uuid, data) (
WITH already_published_uuids
     AS (SELECT uuid
         FROM   public_page_views),
     first_time_arrives
     AS (SELECT 'session_public_uuid' AS what_uuid,
                session_public_uuid   AS uuid,
                Min(time_arrived)     AS first_time_arrived
         FROM   (SELECT data ->> 'session_public_uuid' AS session_public_uuid,
                        data ->> 'time_arrived'        AS time_arrived
                 FROM   page_views) AS pv
         WHERE  session_public_uuid IS NOT NULL
         GROUP  BY session_public_uuid
         UNION
         SELECT 'user_uuid'       AS what_uuid,
                user_uuid         AS uuid,
                Min(time_arrived) AS first_time_arrived
         FROM   (SELECT data ->> 'user_uuid'    AS user_uuid,
                        data ->> 'time_arrived' AS time_arrived
                 FROM   page_views) AS pv
         WHERE  user_uuid IS NOT NULL
         GROUP  BY user_uuid)
SELECT uuid,
       data
FROM   page_views
WHERE  uuid NOT IN (SELECT uuid FROM already_published_uuids)
       AND data ->> 'time_arrived' IS NOT NULL
       AND ( Date_part('epoch', Now()) * 1000 > (SELECT first_time_arrived ::
                                                              bigint +
                                                        60 * 30 * 1000
                                                 FROM   first_time_arrives
                                                 WHERE
             what_uuid = 'session_public_uuid'
             AND
                   uuid = data ->> 'session_public_uuid')
              OR ( Date_part('epoch', Now()) * 1000 > (SELECT
                   first_time_arrived ::
                         bigint +
                   60 * 30 * 1000
                                                       FROM   first_time_arrives
                                                       WHERE
                   what_uuid = 'user_uuid'
                   AND uuid = data ->>
                       'user_uuid'
                                                      )
                   AND data ->> 'user_uuid' IS NOT NULL ) )); """
    try:
        conn = psycopg2.connect("dbname='megatransparency' user='%s' host='localhost' password='%s'" % (app.config['USERNAME'], app.config['PASSWORD']))
    except:
        print "can't connect to database"
    try:
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        query = """UPDATE public_page_views
SET
    data=private.data
FROM public_page_views AS public JOIN page_views AS private ON public.uuid = private.uuid WHERE uuid = public.uuid AND public.data != private.data;"""
        cur.execute(query)
        conn.commit()
        cur.close()
        conn.close()
    except Exception, e:
        print traceback.format_exc()
import psycopg2 as pg2
from psycopg2.extras import RealDictCursor
import pandas as pd


def create_schema():
    
    try:
        query_to_dataframe('SELECT * FROM articles')
        print('Schema already exists!')
    except:
        schema = '''
        CREATE TABLE articles (
            article_id INTEGER PRIMARY KEY,
            article_title TEXT,
            article_content TEXT);

        CREATE TABLE categories (
            category_id INTEGER PRIMARY KEY,
            category_title TEXT);

        CREATE TABLE article_category(
            article_id INTEGER PRIMARY KEY,
            category_id INTEGER,
            FOREIGN KEY (article_id) REFERENCES articles (article_id),
            FOREIGN KEY (category_id) REFERENCES categories (category_id)
        );
        '''

        conn = pg2.connect("dbname=wikipedia user=amirk password=amirk") 
        c = conn.cursor(cursor_factory=RealDictCursor)
        c.execute(schema)
        conn.commit()
        conn.close()
        
    return None
    

def connect_to_db():
    con = pg2.connect("dbname=wikipedia user=amirk password=amirk")
    cur = con.cursor(cursor_factory=RealDictCursor)
    return con, cur


def query_to_dataframe(query, fetch_res=True):
    con, cur = connect_to_db()
    cur.execute(query)
    if fetch_res:
        results = cur.fetchall()
    else:
        results = None
    con.close()
    
    return pd.DataFrame(results)


def insert_to_db(query):
    con, cur = connect_to_db()
    cur.execute(query)
    con.commit()
    con.close()
    return None


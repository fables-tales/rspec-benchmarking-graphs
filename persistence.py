import os
import psycopg2
import time
import urlparse

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

def make_conn():
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )

    return conn

def add_result(mean, deviation, app):
    conn = make_conn()
    cur = conn.cursor()
    cur.execute("INSERT into master_results values (%s, %s, %s, %s)", (app, mean, deviation, time.time()))
    conn.commit()

def add_pr_result(mean, deviation, app, branch):
    conn = make_conn()
    cur = conn.cursor()
    cur.execute("INSERT into pr_results values (%s, %s, %s, %s, %s)", (app, branch, mean, deviation, time.time()))
    conn.commit()

def most_recent_result(app):
    conn = make_conn()
    cur = conn.cursor()
    cur.execute("SELECT mean,deviation from master_results order by time desc limit 1")
    return list(cur.fetchone())

def pr_results(app):
    conn = make_conn()
    cur = conn.cursor()
    cur.execute("SELECT mean,deviation,branch from pr_results where app=%s order by time desc limit 50", (app,))
    return list(cur)

def all_results(app):
    conn = make_conn()
    cur = conn.cursor()
    cur.execute("SELECT mean,deviation from master_results where app=%s order by time", (app,))
    return list(cur)

def all_apps():
    conn = make_conn()
    cur = conn.cursor()
    cur.execute("SELECT distinct app from master_results")
    return [x[0] for x in cur]

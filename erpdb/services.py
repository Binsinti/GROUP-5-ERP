# erp/services.py
from django.db import connection
from psycopg2 import sql

def get_top_customers(limit=5):
    with connection.cursor() as cursor:
        query = sql.SQL("""
            SELECT c.name, SUM(i.quantity * i.price) as total_spent
            FROM erp_customer c
            JOIN erp_salesorder so ON c.id = so.customer_id
            JOIN erp_salesorderitem i ON so.id = i.order_id
            GROUP BY c.name
            ORDER BY total_spent DESC
            LIMIT %s
        """)
        cursor.execute(query, [limit])
        return cursor.fetchall()

"""Скрипт для заполнения данными таблиц в БД Postgres."""
from datetime import datetime
import psycopg2, os, csv

with psycopg2.connect(database="north",user="postgres",password=os.getenv('PASSWORD')) as conn:
    with conn.cursor() as cur:
        with open('north_data/customers_data.csv', 'r') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                customer_id, company_name, contact_name = row
                cur.execute("INSERT INTO customers (customer_id, company_name, contact_name) VALUES (%s, %s, %s)", (customer_id, company_name, contact_name))

        with open('north_data/employees_data.csv', 'r') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                first_name, last_name, title, birth_date, notes = row
                date_obj = datetime.strptime(birth_date, '%Y-%m-%d').date()
                cur.execute("INSERT INTO employees (first_name, last_name, title, birth_date, notes) VALUES (%s, %s, %s, %s, %s)", (first_name, last_name, title, date_obj, notes))

        with open('north_data/orders_data.csv', 'r') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                order_id, customer_id, employee_id, order_date, ship_city = row
                order_id = int(order_id)
                employee_id = int(employee_id)
                date_obj = datetime.strptime(order_date, '%Y-%m-%d').date()
                cur.execute("INSERT INTO orders (order_id, customer_id, employee_id, order_date, ship_city) VALUES (%s, %s, %s, %s, %s)", (order_id, customer_id, employee_id, date_obj, ship_city))


conn.close()
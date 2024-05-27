import sqlite3
import csv

def csv_to_sqlite(csv_file, db_file, table_name):
    with open(csv_file, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)  
        data = list(reader)

    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()

        column_types = ['TEXT', 'TEXT', 'TEXT', 'TEXT' ]

        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join([f'{header} {type}' for header, type in zip(headers, column_types)])})"
        cursor.execute(create_table_query)

        insert_query = f"INSERT INTO {table_name} VALUES ({', '.join(['?']*len(headers))})"
        cursor.executemany(insert_query, data)

        conn.commit()

csv_file = r'C:\Users\Asus\PycharmProjects\la2\la2\la2\output.csv'
db_file = 'faculty_data.db'
table_name = 'information'

csv_to_sqlite(csv_file, db_file, table_name)

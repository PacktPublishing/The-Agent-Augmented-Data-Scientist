"""Run CG purchase metrics on CSVs using standard-library SQLite."""
import argparse
import csv
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path
import sqlite3

HERE = Path(__file__).resolve().parent
DATA = HERE.parents[1] / 'data'


def validate_group(group):
    if group not in ('orders', 'basket'):
        raise ValueError('Choose the orders or basket metric group.')


def calculate(connection, start_date, end_date, group='orders'):
    validate_group(group)
    start, end = date.fromisoformat(start_date), date.fromisoformat(end_date)
    if start.isoformat() != start_date or end.isoformat() != end_date or start >= end:
        raise ValueError('Use YYYY-MM-DD dates with start_date before end_date.')
    # Reject unknown exclusion signals instead of silently classifying accounts.
    invalid = connection.execute("""
        SELECT COUNT(*) FROM customers
        WHERE is_test_account IS NULL
           OR lower(trim(CAST(is_test_account AS TEXT))) NOT IN ('true','false','1','0')
           OR email_domain IS NULL OR trim(email_domain) = ''
    """).fetchone()[0]
    if invalid:
        raise ValueError('Customer exclusion inputs are missing or invalid; resolve before calculating.')
    query = 'order_metrics.sql' if group == 'orders' else 'basket_metrics.sql'
    cursor = connection.execute(
        (HERE / query).read_text(),
        {'start_date': start_date, 'end_date': end_date},
    )
    return dict(zip((column[0] for column in cursor.description), cursor.fetchone()))


def load_data(connection, directory, group='orders'):
    validate_group(group)
    columns = {
        'customers': ['customer_id', 'is_test_account', 'email_domain'],
        'orders': ['order_id', 'customer_id', 'order_status', 'order_date'],
    }
    if group == 'orders':
        columns['orders'].append('adjusted_revenue')
    else:
        columns['order_items'] = ['order_item_id', 'order_id', 'quantity']
    for table, fields in columns.items():
        connection.execute(f"CREATE TABLE {table} ({', '.join(f'{f} TEXT' for f in fields)})")
        with (directory / f'{table}.csv').open(newline='') as source:
            reader = csv.DictReader(source)
            if not set(fields).issubset(reader.fieldnames or []):
                raise ValueError(f'Missing required columns in {table}.csv')
            connection.executemany(
                f"INSERT INTO {table} VALUES ({','.join('?' for _ in fields)})",
                ([row[f] for f in fields] for row in reader),
            )
    keys = {'customers': 'customer_id', 'orders': 'order_id', 'order_items': 'order_item_id'}
    for table in columns:
        key = keys[table]
        rows, populated, distinct = connection.execute(
            f"SELECT COUNT(*), COUNT(NULLIF(trim({key}),'')), COUNT(DISTINCT {key}) FROM {table}"
        ).fetchone()
        if rows != populated or rows != distinct:
            raise ValueError(f'{table}.{key} must be populated and unique.')
    if connection.execute('''SELECT COUNT(*) FROM orders o LEFT JOIN customers c
        ON o.customer_id=c.customer_id WHERE c.customer_id IS NULL''').fetchone()[0]:
        raise ValueError('Orders contain unmatched customer references.')
    if group == 'orders':
        for (value,) in connection.execute('SELECT DISTINCT adjusted_revenue FROM orders'):
            try:
                valid = value is not None and Decimal(value).is_finite()
            except InvalidOperation:
                valid = False
            if not valid:
                raise ValueError('Adjusted revenue must be a finite monetary amount.')
    else:
        if connection.execute("""SELECT COUNT(*) FROM order_items i LEFT JOIN orders o
            ON i.order_id=o.order_id WHERE o.order_id IS NULL""").fetchone()[0]:
            raise ValueError('Order items contain unmatched order references.')
        for (value,) in connection.execute('SELECT DISTINCT quantity FROM order_items'):
            if value is None or not value.isdigit() or int(value) <= 0:
                raise ValueError('Item quantities must be positive integers.')
    for (value,) in connection.execute('SELECT DISTINCT order_date FROM orders'):
        if date.fromisoformat(value).isoformat() != value:
            raise ValueError('Order dates must use YYYY-MM-DD.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--group', choices=['orders', 'basket'], required=True)
    parser.add_argument('--start-date', required=True)
    parser.add_argument('--end-date', required=True, help='Exclusive upper bound')
    parser.add_argument('--data-dir', type=Path, default=DATA)
    args = parser.parse_args()
    with sqlite3.connect(':memory:') as connection:
        load_data(connection, args.data_dir, args.group)
        for name, value in calculate(connection, args.start_date, args.end_date, args.group).items():
            print(f'{name}: {value}')

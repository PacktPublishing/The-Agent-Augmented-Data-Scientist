"""Hand-checkable metric cases, independent of the CG data generator."""
import importlib.util
from pathlib import Path
import sqlite3
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'execution/metrics/run_purchase_metrics.py'
spec = importlib.util.spec_from_file_location('metric', SCRIPT)
metric = importlib.util.module_from_spec(spec)
spec.loader.exec_module(metric)


class PurchaseMetricsChecks(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(':memory:')
        self.addCleanup(self.db.close)
        self.db.executescript('''
            CREATE TABLE customers(customer_id TEXT, is_test_account TEXT, email_domain TEXT);
            CREATE TABLE orders(order_id TEXT, customer_id TEXT, order_status TEXT,
                                order_date TEXT, revenue REAL, refund_amount REAL, adjusted_revenue REAL);
            CREATE TABLE order_items(order_item_id TEXT, order_id TEXT, quantity INTEGER, return_quantity INTEGER);
            INSERT INTO customers VALUES ('buyer', 'False', 'gmail.com');
        ''')

    def order(self, key, customer='buyer', status='Completed', day='2025-01-15', refund=0, quantities=(1,)):
        self.db.execute('INSERT INTO orders VALUES (?,?,?,?,100,?,?)',
                        (key, customer, status, day, refund, 100-refund if status == 'Completed' else 0))
        for index, quantity in enumerate(quantities):
            self.db.execute('INSERT INTO order_items VALUES (?,?,?,?)',
                            (f'{key}-{index}', key, quantity, quantity if refund == 100 else 0))

    def count(self):
        return {**metric.calculate(self.db, '2025-01-01', '2025-02-01', 'orders'),
                **metric.calculate(self.db, '2025-01-01', '2025-02-01', 'basket')}

    def test_refunds_preserve_purchase_events(self):
        for key, refund in [('normal', 0), ('partial', 40), ('full', 100)]:
            self.order(key, refund=refund)
        self.assertEqual(self.count(), {'completed_orders': 3, 'purchasing_customers': 1, 'units_per_transaction': 1.0, 'net_average_order_value': 160 / 3})

    def test_pending_and_cancelled_do_not_count(self):
        self.order('pending', status='Pending')
        self.order('cancelled', status='Cancelled')
        self.assertEqual(self.count(), {'completed_orders': 0, 'purchasing_customers': 0, 'units_per_transaction': None, 'net_average_order_value': None})

    def test_either_exclusion_signal_is_sufficient(self):
        for cid, flag, domain in [('flag', 'True', 'gmail.com'),
                                  ('internal', 'False', ' CascadeGoods.COM '),
                                  ('qa', 'False', 'QA.CASCADEGOODS.TEST')]:
            self.db.execute('INSERT INTO customers VALUES (?,?,?)', (cid, flag, domain))
            self.order(cid, customer=cid)
        self.order('valid')
        self.assertEqual(self.count(), {'completed_orders': 1, 'purchasing_customers': 1, 'units_per_transaction': 1.0, 'net_average_order_value': 100.0})

    def test_date_boundaries_and_multiple_orders_per_customer(self):
        for key, day in [('before','2024-12-31'), ('start','2025-01-01'),
                         ('last','2025-01-31'), ('end','2025-02-01')]:
            self.order(key, day=day)
        self.assertEqual(self.count(), {'completed_orders': 2, 'purchasing_customers': 1, 'units_per_transaction': 1.0, 'net_average_order_value': 100.0})

    def test_multiple_customers_and_refunded_only_customers(self):
        for cid, refund in [('partial', 40), ('full', 100)]:
            self.db.execute('INSERT INTO customers VALUES (?, ?, ?)', (cid, 'False', 'gmail.com'))
            self.order(cid, customer=cid, refund=refund)
        self.order('first')
        self.order('second')
        self.assertEqual(self.count(), {'completed_orders': 4, 'purchasing_customers': 3, 'units_per_transaction': 1.0, 'net_average_order_value': 65.0})

    def test_empty_period(self):
        self.assertEqual(self.count(), {'completed_orders': 0, 'purchasing_customers': 0, 'units_per_transaction': None, 'net_average_order_value': None})

    def test_multiple_lines_and_units_preserve_order_grain(self):
        self.order('basket', quantities=(2, 3), refund=100)
        self.order('single', quantities=(2,))
        self.assertEqual(self.count(), {'completed_orders': 2, 'purchasing_customers': 1,
                                        'units_per_transaction': 3.5, 'net_average_order_value': 50.0})

    def test_missing_lines_do_not_silently_drop_orders(self):
        self.order('missing', quantities=())
        self.order('present')
        self.assertEqual(self.count(), {'completed_orders': 2, 'purchasing_customers': 1,
                                        'units_per_transaction': None, 'net_average_order_value': 100.0})

    def test_order_revenue_is_not_multiplied_by_lines(self):
        self.order('basket', quantities=(2, 3), refund=40)
        self.order('single')
        self.assertEqual(self.count()['net_average_order_value'], 80.0)

    def test_fully_refunded_period_has_zero_value(self):
        self.order('returned', refund=100)
        self.assertEqual(self.count()['net_average_order_value'], 0.0)

    def test_order_group_without_item_file(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)
            (path / 'customers.csv').write_text('customer_id,is_test_account,email_domain\nc,False,gmail.com\n')
            (path / 'orders.csv').write_text('order_id,customer_id,order_status,order_date,adjusted_revenue\no,c,Completed,2025-01-10,75.50\n')
            with sqlite3.connect(':memory:') as db:
                metric.load_data(db, path, 'orders')
                self.assertEqual(metric.calculate(db, '2025-01-01', '2025-02-01', 'orders'),
                                 {'completed_orders': 1, 'purchasing_customers': 1,
                                  'net_average_order_value': 75.5})
                self.assertIsNone(db.execute("SELECT name FROM sqlite_master WHERE name='order_items'").fetchone())

    def test_basket_group_without_revenue_column(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)
            (path / 'customers.csv').write_text('customer_id,is_test_account,email_domain\nc,False,gmail.com\n')
            (path / 'orders.csv').write_text('order_id,customer_id,order_status,order_date\no,c,Completed,2025-01-10\n')
            (path / 'order_items.csv').write_text('order_item_id,order_id,quantity\ni,o,3\n')
            with sqlite3.connect(':memory:') as db:
                metric.load_data(db, path, 'basket')
                self.assertEqual(metric.calculate(db, '2025-01-01', '2025-02-01', 'basket'),
                                 {'units_per_transaction': 3.0})

    def test_invalid_period(self):
        with self.assertRaises(ValueError):
            metric.calculate(self.db, '2025-02-01', '2025-01-01')

    def test_unknown_exclusion_inputs_require_resolution(self):
        self.db.execute("UPDATE customers SET is_test_account=NULL")
        with self.assertRaises(ValueError):
            self.count()


if __name__ == '__main__':
    unittest.main()

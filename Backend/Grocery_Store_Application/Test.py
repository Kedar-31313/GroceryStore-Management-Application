from datetime import datetime
from sql_connection import get_sql_connection

def insert_order(connection, request_payload):
    cursor = connection.cursor()
    insert_order_query = "INSERT INTO orders (customer_id, order_date, total) VALUES (%s, %s, %s)"
    cursor.execute(insert_order_query, (request_payload['customer_id'], request_payload['order_date'], request_payload['total']))
    order_id = cursor.lastrowid

    if 'orders_details' in request_payload:
        for order_detail_record in request_payload['orders_details']:
            insert_order_detail_query = "INSERT INTO order_details (order_id, product_id, quantity) VALUES (%s, %s, %s)"
            cursor.execute(insert_order_detail_query, (order_id, order_detail_record['product_id'], order_detail_record['quantity']))

    connection.commit()
    cursor.close()

    return order_id


if __name__ == '__main__':
    connection = get_sql_connection()
    print(insert_order(connection, {
        'customer_name': 'par',
        'total': '90',
        'datetime': datetime.now(),
        'orders_details': [
            {
                'product_id': 10,
                'quantity': 1,
                'total_price': 30
            },
            {
                'product_id': 11,
                'quantity': 1,
                'total_price': 60
            }
        ]
    }))
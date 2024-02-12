from datetime import datetime
from sql_connection import get_sql_connection

def insert_order(connection, order):
    cursor = connection.cursor()

    order_query = ("INSERT INTO orders (customer_name, total, datetime) VALUES (%s, %s, %s)")
    order_data = (order['customer_name'], order['total'], datetime.now())

    cursor.execute(order_query, order_data)
    order_id = cursor.lastrowid

    order_details_query = ("INSERT INTO orders_details (order_id, product_id, quantity, total_price) VALUES (%s, %s, %s, %s);")

    order_details_data = []
    for order_detail_record in order['orders_details']:
        order_details_data.append([
            order_id,
            int(order_detail_record['product_id']),
            float(order_detail_record['quantity']),
            float(order_detail_record['total_price'])
        ])
    cursor.executemany(order_details_query, order_details_data)

    connection.commit()

    return order_id

def get_order_details(connection, order_id):
    cursor = connection.cursor()

    query = "SELECT * from orders_details where order_id = %s"

    query = "select order_id, quantity, total_price, name, price_per_unit from orders_details " \
            "left join products on orders_details.product_id = products.product_id where orders_details.order_id = %s;"

    data = (order_id, )

    cursor.execute(query, data)

    records = []
    for (order_id, quantity, total_price, name, price_per_unit) in cursor:
        records.append({
            'order_id': order_id,
            'quantity': quantity,
            'total_price': total_price,
            'name': name,
            'price_per_unit': price_per_unit
        })

    cursor.close()

    return records

def get_all_orders(connection):
    cursor = connection.cursor()
    query = ("SELECT * FROM orders")
    cursor.execute(query)
    response = []
    for (order_id, customer_name, total, dt) in cursor:
        response.append({
            'order_id': order_id,
            'customer_name': customer_name,
            'total': total,
            'datetime': dt,
        })

    cursor.close()

    # append order details in each order
    for record in response:
        record['order_details'] = get_order_details(connection, record['order_id'])

    return response

if __name__ == '__main__':
    connection = get_sql_connection()
    # print(get_all_orders(connection))
    # print(get_order_details(connection,3))
    print(insert_order(connection, {
         'customer_name': 'Manohar',
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
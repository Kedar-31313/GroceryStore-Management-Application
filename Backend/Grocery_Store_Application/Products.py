from sql_connection import get_sql_connection


def get_all_products(connection):
    cursor = connection.cursor()
    query = ("select product_id, name, uom, price_per_unit,uom_name from products join uom on products.uom=uom.uom_id;")
    cursor.execute(query)
    response = []
    for (product_id, name, uom, price_per_unit, uom_name) in cursor:
        response.append({
            'product_id': product_id,
            'name': name,
            'uom': uom,
            'price_per_unit': price_per_unit,
            'uom_name': uom_name
        })
    return response

def insert_new_product(connection, product):
    cursor = connection.cursor()
    query = ("INSERT INTO products (name, uom, price_per_unit) VALUES ( %s, %s, %s);")
    data = (product['name'], product['uom'], product['price_per_unit'])

    cursor.execute(query, data)
    connection.commit()
    return cursor.lastrowid

def delete_product(connection, product_id):
    cursor = connection.cursor()
    query = "DELETE FROM products where product_id= %s"
    data=(product_id,)
    cursor.execute(query,data)
    connection.commit()

    return cursor.lastrowid

if __name__ == '__main__':
    connection = get_sql_connection()
    #print(get_all_products(connection))

    #print(delete_product(connection,3))

    print(insert_new_product(connection, {
        'name': 'Milk',
        'uom': '3',
        'price_per_unit': 60
     }))
import mysql.connector

cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="pandeyji_eatery"
)


def insert_order_tracking (order_id , status ):
    cursor = cnx.cursor()
    query = "INSERT INTO order_tracking(order_id , status) VALUES (%s ,%s)"
    cursor.execute(query, (order_id,status))
    cnx.commit()
    cursor.close()


def insert_order_item(food_item, quantity, order_id):
    try:
        cursor = cnx.cursor()
        cursor.callproc('insert_order_item', (food_item, quantity, order_id))
        cnx.commit()
        cursor.close()
        return 1
    except mysql.connector.Error as err:
        print(f"Error inserting order item : {err}")
        cnx.rollback()
        return -1
    except Exception as e:
        print(f"AN error occurred :{e} ")
        cnx.rollback()
        return -1


def get_next_order_id():
    cursor = cnx.cursor()
    query = "SELECT MAX(order_id) FROM orders"
    cursor.execute(query)
    result = cursor.fetchone()[0]
    cursor.close()
    if result is None:
        return 1
    else:
        return result + 1


def get_total_order_price(order_id):
    cursor = cnx.cursor()
    query = f"SELECT get_total_order_price({order_id})"
    cursor.execute(query)
    result = cursor.fetchone()[0]
    cursor.close()
    return result


def get_order_status(order_id: int):
    cusor = cnx.cursor()
    query = (f"SELECT status FROM order_tracking WHERE order_id= {order_id}")
    cusor.execute(query)
    result = cusor.fetchone()
    cusor.close()

    if result is not None:
        return result[0]
    else:
        return None

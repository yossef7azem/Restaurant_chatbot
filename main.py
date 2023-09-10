from fastapi import FastAPI
from fastapi import Request
from starlette.responses import JSONResponse
import generic_helper
import DB

app = FastAPI()

inprogress_orders = {}

@app.post("/")
async def handle_request(request: Request):
    payload = await request.json()

    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    output_contexts = payload['queryResult']['outputContexts']
    session_id = generic_helper.extract_session_id(output_contexts[0]["name"])
    intent_dict = {
        'order.remove - context:ongoing-order': remove_from_order,
        'Oredr.add - contxt : ongoing-order': add_to_order,
        'order.completed - context : ongoing-order': complete_order,
        'track.order - context :ongoing-tracking': track_order
    }
    return intent_dict[intent](parameters , session_id)


def remove_from_order(parameters: dict, session_id: str):
    if session_id not in inprogress_orders:
        return JSONResponse(content={"fulfillmentText" : "Cant't find your order try again with correct order ID"})
    current_order = inprogress_orders[session_id]
    food_items = parameters["food-item"]
    removed_item=[]
    no_such_items =[]
    for item in food_items:
        if item not in current_order:
            no_such_items.append(item)
        else:
            removed_item.append(item)
            del current_order[item]
    if len(removed_item)>0:
        fulfillment_text = f'Removed {",".join(removed_item)} from your order'
    if len(no_such_items)>0:
        fulfillment_text = f'Your order doesn not have {",".join(no_such_items)} '
    if len(current_order.keys()) ==0 :
        fulfillment_text += "Your order is empty!"
    else:
        order_str = generic_helper.get_str_from_food_dict(current_order)
        fulfillment_text += f"HERE is what is left in your order :{order_str}"
    return JSONResponse(content={"fulfillmentText": fulfillment_text})


def complete_order (parameters: dict, session_id: str):
    if session_id not in inprogress_orders:
        fulfillment_text = "Your order no found , you can type order id correct or place new order !"
    else:
        order = inprogress_orders[session_id]
        order_id = save_to_db(order)
        if order_id ==-1 :
            fulfillment_text = "sorry ! the order not processed "
        else :
            order_total=DB.get_total_order_price (order_id)
            fulfillment_text = f"Awesome ! we placed your order"\
                               f"Here is your order id # {order_id} "\
                               f"Your order total price is : {order_total}"
        del inprogress_orders[session_id]
    return JSONResponse(content= {"fulfillmentText" :fulfillment_text})


def save_to_db (order:dict):
    next_order_id = DB.get_next_order_id()
    for food_item,quantity in order.items():
        rcode = DB.insert_order_item (
            food_item ,
            quantity ,
            next_order_id
        )
        if rcode ==-1 :
            return -1
    DB.insert_order_tracking(next_order_id , "in progress")
    return next_order_id


def add_to_order(parameters: dict, session_id :str):
    food_items = parameters["food-item"]
    quantities = parameters["number"]
    if len(food_items) != len(quantities):
        fulfillment_text = "sorry  , please specify food items and quantities clear "
    else:
        new_food_dic = dict(zip(food_items , quantities))
        if session_id in inprogress_orders:
            current_food_dict = inprogress_orders[session_id]
            current_food_dict.update(new_food_dic)
        else:
            inprogress_orders[session_id] = new_food_dic

        order_string = generic_helper.get_str_from_food_dict(inprogress_orders[session_id])
        fulfillment_text = f"YOU HAVE {order_string} > Do you want any thing else ? "
    return JSONResponse(content={
        "fulfillmentText": fulfillment_text})


def track_order(parameters: dict, session_id:str):
    order_id = int(parameters['number'])
    order_status = DB.get_order_status(order_id)
    if order_status:
        fulfillment_text = f"The order status for order id :{order_id} is : {order_status}"
    else:
        fulfillment_text = f"no order found with no {order_id}"
    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })

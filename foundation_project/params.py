#query parameter and path parameter
from fastapi import FastAPI, Query

app = FastAPI()

#path parameter
@app.get("/items/{item_id}")
def read_item(item_id):
    return {"item_id": item_id}

#multiple path parameter
@app.get("/users/{user_id}/orders/{order_id}")
def get_order(user_id, order_id):
    return{
        "user_id": user_id,
        "order_id": order_id
    }

#query parameter
@app.get("/items/")
def read_items(
    q: str= Query(None, min_length=3, max_length=50)
):
    return {"q": q}


# 🧠 Best Practice Rule

# ✔ Use path parameter → when identifying a specific resource
# ✔ Use query parameter → for filtering, sorting, pagination

# Example:

# /users/5          ✅ path
# /users?active=1   ✅ query
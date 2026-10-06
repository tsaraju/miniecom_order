from decimal import Decimal
from enum import Enum

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="Order API")


# ----- Models -----

class ProductCreate(BaseModel):
    name: str = Field(min_length=1)
    price: Decimal = Field(gt=0, max_digits=10, decimal_places=2)


class Product(ProductCreate):
    id: int


class OrderStatus(str, Enum):
    PLACED = "PLACED"
    PROCESSING = "PROCESSING"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"


class OrderItemRequest(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)


class OrderCreate(BaseModel):
    customer: str = Field(min_length=1)
    items: list[OrderItemRequest] = Field(min_length=1)


class OrderItem(BaseModel):
    product_id: int
    product_name: str
    quantity: int
    unit_price: Decimal
    subtotal: Decimal


class Order(BaseModel):
    id: int
    customer: str
    products: list[OrderItem]
    total_amount: Decimal
    status: OrderStatus


class OrderStatusUpdate(BaseModel):
    status: OrderStatus


# ----- In-memory storage -----
# Data is lost whenever the application stops.

products: dict[int, Product] = {}
orders: dict[int, Order] = {}

next_product_id = 1
next_order_id = 1


# ----- Product endpoints -----

@app.post("/products", response_model=Product, status_code=status.HTTP_201_CREATED)
def create_product(product_data: ProductCreate):
    global next_product_id

    product = Product(id=next_product_id, **product_data.model_dump())
    products[product.id] = product
    next_product_id += 1

    return product


@app.get("/products", response_model=list[Product])
def get_products():
    return list(products.values())


# ----- Order endpoints -----

@app.post("/orders", response_model=Order, status_code=status.HTTP_201_CREATED)
def create_order(order_data: OrderCreate):
    global next_order_id

    seen_product_ids = set()
    order_items = []

    for requested_item in order_data.items:
        if requested_item.product_id in seen_product_ids:
            raise HTTPException(
                status_code=400,
                detail=f"Product {requested_item.product_id} appears more than once",
            )
        seen_product_ids.add(requested_item.product_id)

        product = products.get(requested_item.product_id)
        if product is None:
            raise HTTPException(
                status_code=404,
                detail=f"Product {requested_item.product_id} not found",
            )

        subtotal = product.price * requested_item.quantity

        order_items.append(
            OrderItem(
                product_id=product.id,
                product_name=product.name,
                quantity=requested_item.quantity,
                unit_price=product.price,
                subtotal=subtotal,
            )
        )

    # The server calculates the total; clients cannot supply it.
    total_amount = sum(
        (item.subtotal for item in order_items),
        Decimal("0.00"),
    )

    order = Order(
        id=next_order_id,
        customer=order_data.customer,
        products=order_items,
        total_amount=total_amount,
        status=OrderStatus.PLACED,
    )

    orders[order.id] = order
    next_order_id += 1

    return order


@app.get("/orders", response_model=list[Order])
def get_orders():
    return list(orders.values())


@app.get("/orders/{order_id}", response_model=Order)
def get_order(order_id: int):
    order = orders.get(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    return order


@app.put("/orders/{order_id}/status", response_model=Order)
def update_order_status(order_id: int, update: OrderStatusUpdate):
    order = orders.get(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    next_status = {
        OrderStatus.PLACED: OrderStatus.PROCESSING,
        OrderStatus.PROCESSING: OrderStatus.SHIPPED,
        OrderStatus.SHIPPED: OrderStatus.DELIVERED,
    }

    expected_status = next_status.get(order.status)
    if update.status != expected_status:
        expected = expected_status.value if expected_status else "no further status"
        raise HTTPException(
            status_code=409,
            detail=f"Order is {order.status.value}; next status must be {expected}",
        )

    updated_order = order.model_copy(update={"status": update.status})
    orders[order_id] = updated_order

    return updated_order
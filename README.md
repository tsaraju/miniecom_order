Mini E-Commerce Order API

What to build
Build a small FastAPI backend for placing orders.

Create APIs such as

POST /products

GET /products

POST /orders

GET /orders

GET /orders/{order_id}

PUT /orders/{order_id}/status

An order should contain a customer, products, quantities, total amount, and status such as:

PLACED → PROCESSING → SHIPPED → DELIVERED

Validate that the requested product exists and the quantity is valid. Calculate the total order amount on the server, rather than accepting the final amount directly from the client.

Sample Output:
PS F:\Euron\GitHub\api\miniecom_order> uv run uvicorn main:app --reload
INFO:     Will watch for changes in these directories: ['F:\\Euron\\GitHub\\api\\miniecom_order']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [7596] using WatchFiles
INFO:     Started server process [12924]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:54753 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:54753 - "GET /openapi.json HTTP/1.1" 200 OK
INFO:     127.0.0.1:49899 - "POST /products HTTP/1.1" 201 Created
INFO:     127.0.0.1:60020 - "POST /products HTTP/1.1" 201 Created
INFO:     127.0.0.1:54523 - "POST /products HTTP/1.1" 201 Created
INFO:     127.0.0.1:61835 - "GET /products HTTP/1.1" 200 OK
INFO:     127.0.0.1:54249 - "POST /orders HTTP/1.1" 422 Unprocessable Content
INFO:     127.0.0.1:50390 - "POST /orders HTTP/1.1" 422 Unprocessable Content
INFO:     127.0.0.1:52748 - "POST /orders HTTP/1.1" 201 Created
INFO:     127.0.0.1:52037 - "GET /orders/2 HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:65326 - "GET /orders/1 HTTP/1.1" 200 OK
INFO:     127.0.0.1:61234 - "GET /orders HTTP/1.1" 200 OK
INFO:     127.0.0.1:59162 - "POST /orders HTTP/1.1" 201 Created
INFO:     127.0.0.1:55525 - "GET /orders HTTP/1.1" 200 OK
INFO:     127.0.0.1:54927 - "POST /orders HTTP/1.1" 201 Created
INFO:     127.0.0.1:63737 - "GET /orders HTTP/1.1" 200 OK
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [12924]
INFO:     Stopping reloader process [7596]
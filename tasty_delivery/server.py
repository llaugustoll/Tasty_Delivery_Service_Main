from fastapi import FastAPI
from fastapi.exceptions import ResponseValidationError
from fastapi.responses import PlainTextResponse
from pydantic import ValidationError

from adapter.api.controllers.auth_user_controller import AuthController
from adapter.api.controllers.auth_client_controller import AuthClientController
from adapter.api.controllers.category_controller import CategoryController
from adapter.api.controllers.client_controller import ClientController
from adapter.api.controllers.product_controller import ProductController
from adapter.api.controllers.user_controller import UserController
from adapter.api.controllers.order_controller import OrderController

from core.application.use_cases.category.category_case import CategoryCase
from core.application.use_cases.client.client_case import ClientCase
from core.application.use_cases.product.product_case import ProductCase
from core.application.use_cases.user.user_case import UserCase
from core.application.use_cases.order.order_case import OrderCase

from scripts.populate_database import populate

app = FastAPI(title="Tasty Delivery")


@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=422)


@app.exception_handler(ResponseValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=422)


# Users
user_controller = UserController(UserCase)

# Categories
category_controller = CategoryController(CategoryCase)

# Products
products_controller = ProductController(ProductCase)

# Clients
clients_controller = ClientController(ClientCase)

# Orders
order_controller = OrderController(OrderCase)

# Authentication
auth_client_controller = AuthClientController()
auth_user_controller = AuthController()

app.include_router(clients_controller.router)
app.include_router(user_controller.router)
app.include_router(category_controller.router)
app.include_router(products_controller.router)
app.include_router(auth_client_controller.router)
app.include_router(auth_user_controller.router)
app.include_router(order_controller.router)


@app.on_event("startup")
async def populate_database():
    populate()

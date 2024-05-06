from sqlalchemy.exc import IntegrityError

from adapter.database.models.client import Client as ClientDB
from adapter.database.models.order import Order as OrderDB
from adapter.database.models.order_product_association import OrderProductAssociation
from adapter.repositories.order_repository import OrderRepository
from adapter.repositories.product_repository import ProductRepository
from core.application.use_cases.order.iorder_case import IOrderCase
from core.domain.entities.category import CategoryOUT
from core.domain.entities.order import OrderIN, OrderOUT, OrderUpdate, Product
from core.domain.entities.product import ProductOUT
from core.domain.exceptions.exception import DuplicateObject, ObjectNotFound, InvalidStatus
from core.domain.value_objects.order_status import OrderStatus
from logger import logger
from security.base import has_permission
from adapter.webhook.webhook import send_webhook


class OrderCase(IOrderCase):
    RECEBIDO = OrderStatus.RECEBIDO.name
    EM_PREPARACAO = OrderStatus.EM_PREPARACAO.name
    PRONTO = OrderStatus.PRONTO.name
    FINALIZADO = OrderStatus.FINALIZADO.name

    AVAILABLE_STATUS = (RECEBIDO, EM_PREPARACAO, PRONTO, FINALIZADO)

    def __init__(self,
                 db=None,
                 current_client: ClientDB = None,
                 current_user=None):
        self.repository = OrderRepository(db)
        self.product_repository = ProductRepository(db)
        self.session = db
        self.current_client = current_client
        self.current_user = current_user

    def get_all(self):
        results = self.repository.get_all()
        saida = []

        for order in results:
            products_out = []

            order_out = {
                "order_id": order.id,
                "client_id": order.client_id,
                "discount": order.discount,
                "total": order.total,
                "status": order.status
            }

            for product in order.products:
                products_out.append({
                    "product_id": product.id,
                    "price": product.price,
                    "quantity": product.order_association[0].quantity,
                    "obs": product.order_association[0].obs,
                })

            saida.append(
                OrderOUT(**order_out, products=products_out)
            )

        return saida

    def get_by_id(self, id):
        result = self.repository.get_by_id(id)
        if not result:
            msg = f"Pedido {id} não encontrado."
            logger.warning(msg)
            raise ObjectNotFound(msg, 404)

        products_out = []

        order_out = {
            "order_id": result.id,
            "client_id": result.client_id,
            "discount": result.discount,
            "total": result.total,
            "status": result.status
        }

        for product in result.products:
            products_out.append({
                "product_id": product.id,
                "price": product.price,
                "quantity": product.order_association[0].quantity,
                "obs": product.order_association[0].obs,
            })

        return OrderOUT(**order_out, products=products_out)

    def get_by_client(self, client_id):
        orders = []
        produtos = []

        if not client_id:
            return

        results = self.repository.get_by_client(client_id)
        for result in results:
            for produto in result.products:
                produto = ProductOUT(
                    name=produto.name,
                    description=produto.description,
                    price=produto.price,
                    category=CategoryOUT(**vars(produto.category))
                )
                produto = Product(
                    product_id=result.product_association[0].product_id,
                    quantity=result.product_association[0].quantity,
                    price=produto.price,
                    obs=result.product_association[0].obs
                )
                produtos.append(produto)

            order = OrderOUT(
                order_id=result.id,
                client_id=result.client_id,
                discount=result.discount,
                total=result.total,
                status=result.status,
                products=produtos
            )
            orders.append(order)

        return orders

    @has_permission(permission=['client'])
    def create(self, order: OrderIN) -> OrderOUT:
        associations = []
        client_id = self.current_client.id if self.current_client else None
        try:
            orderdb = OrderDB(
                total=order.total,
                discount=order.discount,
                status=OrderCase.RECEBIDO,
                client_id=client_id,
            )

            for product in order.products:
                association = OrderProductAssociation(
                    order=orderdb,
                    product=self.product_repository.get_by_id(product.product_id),
                    quantity=product.quantity,
                    obs=product.obs
                )
                associations.append(association)

            result = self.repository.create(associations)

            webhook_msg = (f"Pedido {result[0].order_id} criado com sucesso - "
                           f"Status {orderdb.status}")

            if client_id:
                webhook_msg += f" - Cliente {self.current_client.name}"

            send_webhook(webhook_msg)

            return OrderOUT(
                order_id=result[0].order_id,
                client_id=orderdb.client_id,
                discount=orderdb.discount,
                total=orderdb.total,
                status=orderdb.status,
                products=order.products
            )

        except IntegrityError as e:
            msg = "Pedido já existente criado na base de dados."
            logger.warning(msg)
            raise DuplicateObject(msg, 409)
        except Exception as e:
            raise e

    @has_permission(permission=['admin'])
    def update_status(self, id, status: str) -> OrderOUT:
        new_status = status.upper()

        if new_status not in OrderCase.AVAILABLE_STATUS:
            raise InvalidStatus(status_code=400, msg=f"Status {status} não é valido.")
        result = self.repository.update_status(
            id,
            {"status": new_status, "updated_by": self.current_user.id}
        )

        webhook_msg = f"Pedido {result.id} atualizado - Status {result.status}"

        send_webhook(webhook_msg)

        return OrderOUT(
            order_id=result.id,
            client_id=result.client_id,
            discount=result.discount,
            total=result.total,
            status=result.status,
            products=[
                Product(
                    product_id=product.id,
                    price=product.price,
                    quantity=product.order_association[0].quantity,
                    obs=product.order_association[0].obs
                ) for product in result.products
            ]
        )

    @has_permission(permission=['admin'])
    def update(self, id, new_values: OrderUpdate) -> OrderOUT:
        order = self.repository.update(id, new_values.model_dump(exclude_unset=True))
        if order:
            return self.get_by_id(id)
        else:
            raise ObjectNotFound(f"Pedido {id} não encontrado.", 404)

    @has_permission(permission=['admin'])
    def delete(self, id):
        self.repository.delete(id, self.current_user)

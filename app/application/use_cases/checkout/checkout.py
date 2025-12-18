from app.application.dto.checkout_dto import CheckoutDTO
from app.domain.uow.unit_of_work import UnitOfWork
from app.domain.repositories.cart_repository import CartRepository
from app.domain.repositories.product_repository import ProductRepository
from app.domain.repositories.inventory_repository import InventoryRepository
from app.domain.entities.inventory import InventoryReservation


class CheckoutUseCase:
    def __init__(
        self,
        uow: UnitOfWork,
        cart_repo: CartRepository,
        product_repo: ProductRepository,
        inventory_repo: InventoryRepository,
    ):
        self.uow = uow
        self.carts = cart_repo
        self.products = product_repo
        self.inventory = inventory_repo

    async def execute(self, dto: CheckoutDTO):
        async with self.uow:
            cart = await self.carts.get_by_user_id(dto.user_id)

            if not cart or not cart.items:
                raise ValueError("Cart is empty")

            reservations = []

            for item in cart.items:
                product = await self.products.get_by_id(item.product_id)

                if not product:
                    raise ValueError("Product not found")

                # доменная логика
                product.reserve(item.quantity)

                reservation = InventoryReservation.create(
                    product_id=product.id,
                    quantity=item.quantity
                )

                await self.inventory.create(reservation)

                reservations.append(reservation)
                await self.products.update(product)

            cart.clear()
            await self.carts.update(cart)

            return reservations

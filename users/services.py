import stripe

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(name: str) -> str:
    """Создает продукт в страйпе."""

    product = stripe.Product.create(name=name)
    return product.id


def create_stripe_price(product_id: str, amount: int, currency: str) -> str:
    """Создает цену в страйпе."""

    price = stripe.Price.create(
        currency=currency,
        unit_amount=int(amount * 100),
        product=product_id,
    )
    return price.id


def create_stripe_session(price_id: str) -> dict:
    session = stripe.checkout.Session.create(
        success_url="http://localhost:8000/lms/courses/",
        line_items=[{"price": price_id, "quantity": 1}],
        mode="payment",
        payment_method_types=["card"],
    )
    return {"session_id": session.id, "url": session.url}


def retrieve_checkout_session(session_id: str) -> dict:
    session = stripe.checkout.Session.retrieve(
        session_id,
    )
    return session

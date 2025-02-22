import uuid

from fastapi import APIRouter

from ..clients import yookassa
from ..db import Orders
from ..models import CheckPaymentResponse, CreatePaymentRequest, CreatePaymentResponse


router = APIRouter(tags=["Payment"],prefix="/payment")

# Создание Платежа
@router.post("",response_model=CreatePaymentResponse, description="Создание Платежа")
async def create_payment(payment: CreatePaymentRequest):
    
    order = await Orders.create(
        order_id=str(uuid.uuid4()),
        amount=payment.amount,
        description=payment.description,
    )  # Заказ в базе данных

    payment_info = await yookassa.post(
        "/payments",
        json={
            "amount": {
                "value": payment.amount,
                "currency": "RUB",
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "http://localhost:8000/check?order_id=" + order.order_id,
            },
            "save_payment_method": True,
            "capture": True,
            "description": payment.description,
        },
        headers={"Idempotence-Key": order.order_id},
    )  # Платеж в Юкассе

    order.yookassa_id = payment_info.json()["id"]
    await order.save()

    return CreatePaymentResponse(
        link=payment_info.json()["confirmation"]["confirmation_url"]
    )


# Проверка Платежа
@router.get("", response_model=CheckPaymentResponse, description="Проверка платежа")
async def check_payment(order_id: str):
    
    order = await Orders.get_or_none(order_id=order_id)
    
    if order is None:
        return CheckPaymentResponse(is_paid=False, payment_link=None)

    payment_link = "https://yoomoney.ru/checkout/payments/v2/contract?orderId=" + order.yookassa_id

    if order.is_paid:
        return CheckPaymentResponse(is_paid=True, payment_link=payment_link)

    payment_info = await yookassa.get(
        f"/payments/{order.yookassa_id}"
    )  # Информация о платеже из Юкассы

    is_paid = payment_info.json()["status"] == "succeeded"
    
    if is_paid:
        order.is_paid = True
        order.payment_method_id = payment_info.json()["payment_method"]["id"]
        await order.save()

    return CheckPaymentResponse(
        is_paid=is_paid,
        payment_link=payment_link,
    )


# Возврат Платежа
@router.post("/refund/{order_id}", description="Возврат платежа")
async def refund_payment(order_id: str) -> bool:
    
    order = await Orders.get_or_none(order_id=order_id)
    
    if order is None:
        return False

    refund_info = await yookassa.post(
        "/refunds",
        json={
            "payment_id": order.yookassa_id,
            "amount": {
                "value": order.amount,
                "currency": "RUB",
            },
        },
        headers={"Idempotence-Key": str(uuid.uuid4())},
    )
    print(refund_info.json())

    return refund_info.json()["status"] == "succeeded"
from ..clients import yookassa
from ..db import Orders

async def recurrent_worker():
    orders = await Orders.filter(is_paid=True)
    for order in orders:
        payment_info = await yookassa.post(
            "/payments",
            json={
                "amount": {
                    "value": order.amount,
                    "currency": "RUB",
                },
                "capture": True,
                "description": order.description,
                "payment_method_id": order.payment_method_id,
            },
        )
        payment_info = payment_info.json()
        if payment_info["status"] == "succeeded":
            print(
                f"Платеж на сумму {order.amount} с ID {order.yookassa_id} успешно списан"
            )
        else:
            print(
                f"Ошибка при списании платежа на сумму {order.amount} с ID {order.yookassa_id} "
                + {payment_info.get("cancelation_details", {}).get("reason")}
            )
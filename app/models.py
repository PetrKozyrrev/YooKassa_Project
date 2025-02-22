from pydantic import BaseModel

# Модель ответа на создание платежа
class CreatePaymentResponse(BaseModel):  
    link: str  # Ссылка на оплату

# Модель запроса на создание платежа
class CreatePaymentRequest(BaseModel):  
    amount: int  # Сумма платежа
    description: str  # Описание платежа

# Модель ответа на проверку платежа
class CheckPaymentResponse(BaseModel):  
    is_paid: bool  # Статус платежа
    payment_link: str  # Ссылка на оплату


# Модель запроса на проверку платежа
class CheckPaymentRequest(BaseModel):  
    order_id: str  # Идентификатор заказа
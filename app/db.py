from tortoise import fields, models

# Модель базы данных для заказов
class Orders(models.Model):  
    id = fields.IntField(True)
    order_id = fields.CharField(max_length=255)
    yookassa_id = fields.CharField(max_length=255, null=True)
    amount = fields.IntField()
    description = fields.TextField()
    is_paid = fields.BooleanField(default=False)
    payment_method_id = fields.CharField(max_length=255, null=True)

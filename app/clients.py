from httpx import AsyncClient

from .settings import script_settings, yookassa_settings

yookassa = AsyncClient(
    base_url="https://api.yookassa.ru/v3",
    auth=(
        yookassa_settings.shop_id,
        yookassa_settings.secret_key.get_secret_value(),
    ),
)

TORTOISE_ORM = {
    "connections": {"default": script_settings.db.get_secret_value()},
    "apps": {
        "models": {
            "models": ["app.db", "aerich.models"],
            "default_connection": "default",
        }
    },
}
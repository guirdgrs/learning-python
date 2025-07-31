from store.schemas.product import ProductIn
import pytest
from pydantic import ValidationError
from tests.factories import product_data


def test_schemas_return_success():
    data = product_data()
    product = ProductIn.model_validate(data)

    assert product.name == "Iphone 14"


def test_schemas_return_raise():
    data = {"name": "Iphone 14", "quantity": 10, "price": 8.500}

    with pytest.raises(ValidationError) as err:
        ProductIn.model_validate(data)

        assert err.value.errors()[0] == {
            "type": "missing",
            "loc": ("status",),
            "msg": "Field required",
            "input": {"name": "Iphone 14", "quantity": 10, "price": "8.500"},
            "url": "https://errors.pydantic.dev/2.0/v/field-required",
        }

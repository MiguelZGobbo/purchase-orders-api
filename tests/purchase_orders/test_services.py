"""Testes unitários para as regras de negócio de purchase_orders."""

import pytest

from exceptions.exceptions import QuantityException
from purchase_orders.services import PurchaseOrdersServices


@pytest.mark.nocleardb
def test_check_quantity_less_then_miminum():
    """Deve lançar exceção ao informar quantidade abaixo do mínimo permitido."""
    with pytest.raises(QuantityException) as ex:
        PurchaseOrdersServices()._check_quantity(30)
    assert ex.value.code == 400
    assert ex.value.description == 'A quantidade deve ser entre 50 e 150 itens'


@pytest.mark.nocleardb
def test_check_quantity_greater_then_maximum():
    """Deve lançar exceção ao informar quantidade acima do máximo permitido."""
    with pytest.raises(QuantityException) as ex:
        PurchaseOrdersServices()._check_quantity(151)
    assert ex.value.code == 400
    assert ex.value.description == 'A quantidade deve ser entre 50 e 150 itens'

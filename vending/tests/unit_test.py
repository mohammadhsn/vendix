import pytest
from seedwork.test_utils import marks
from domain.models import Inventory, Machine
from domain.errors import OutOfStock, ChoosingItemRequiresEnoughCoin
from domain.valueobjects import State

from .fixtures import soda, coffee, inventory, idle_machine, out_stock_coffe # noqa

COFFEE_PRICE: int = 5
SODA_PRICE: int = 8


@marks("unit")
def test_cash_in_leads_to_change_state(idle_machine: Machine):
    idle_machine.cash_in(COFFEE_PRICE)
    assert idle_machine.state is State.Choosing


@marks("unit")
def test_it_keeps_entered_coin_amount(idle_machine: Machine):
    idle_machine.cash_in(COFFEE_PRICE)
    assert idle_machine.coin == COFFEE_PRICE


@marks("unit")
def test_choosing_an_expensive_item(idle_machine: Machine):
    idle_machine.cash_in(COFFEE_PRICE - 1)
    with pytest.raises(ChoosingItemRequiresEnoughCoin):
        idle_machine.choose('soda')


@marks("unit")
def test_choosing_an_out_of_stock_product(idle_machine: Machine, out_stock_coffe: Inventory):
    idle_machine.inventory = out_stock_coffe
    idle_machine.cash_in(COFFEE_PRICE)
    with pytest.raises(OutOfStock):
        idle_machine.choose('coffee')


@marks("unit")
def test_choosing_item_leads_to_consume_coin(idle_machine: Machine):
    idle_machine.cash_in(COFFEE_PRICE)
    current_cash = idle_machine.cash_desk
    idle_machine.choose('coffee')
    assert idle_machine.cash_desk == current_cash + COFFEE_PRICE
    assert idle_machine.coin == 0


@marks("unit")
def test_choosing_item_leads_to_idling_the_machine(idle_machine: Machine):
    idle_machine.cash_in(COFFEE_PRICE)
    idle_machine.choose('coffee')
    assert idle_machine.state is State.Idle


@marks("unit")
def test_choosing_item_leads_to_deducting_stock(idle_machine: Machine):
    idle_machine.cash_in(COFFEE_PRICE)
    _, current_stock = idle_machine.inventory.find('coffee')
    idle_machine.choose('coffee')
    _, stock = idle_machine.inventory.find('coffee')
    assert stock == current_stock - 1

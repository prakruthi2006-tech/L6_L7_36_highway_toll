import pytest
from highway_toll import toll_for, toll_charge, pass_advice


# ---- Example tests from the starter file ----
def test_ambulance_is_exempt():
    assert toll_charge("ambulance", 2, False, False) == 0


def test_two_axle_base_toll():
    assert toll_for(2, False, False) == 100


# ---- Added tests for LINE coverage (every line executed at least once) ----
def test_invalid_axle_count_raises():
    with pytest.raises(ValueError, match="invalid axle count"):
        toll_for(1, False, False)


def test_three_axle_base_toll():
    assert toll_for(3, False, False) == 150


def test_four_axle_base_toll():
    assert toll_for(4, False, False) == 250


def test_more_than_four_axles_uses_default_toll():
    assert toll_for(5, False, False) == 400


def test_peak_hour_adds_25_percent():
    assert toll_for(2, True, False) == pytest.approx(125.0)


def test_fastag_two_axle_discount_is_10_percent():
    assert toll_for(2, False, True) == pytest.approx(90.0)


def test_fastag_other_axle_discount_is_5_percent():
    assert toll_for(3, False, True) == pytest.approx(142.5)


def test_pass_advice_buy_pass():
    trips = [(False, False), (False, False)]  # 2 x 100 = 200
    assert pass_advice(trips, 2, 150) == "buy_pass"


def test_pass_advice_pay_per_trip():
    trips = [(False, False), (False, False)]  # 200
    assert pass_advice(trips, 2, 500) == "pay_per_trip"

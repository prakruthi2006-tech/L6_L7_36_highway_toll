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


def test_fire_engine_is_exempt():
    assert toll_charge("fire_engine", 3, True, True) == 0


def test_regular_vehicle_is_charged():
    assert toll_charge("truck", 3, False, False) == 150


def test_pass_advice_buy_pass():
    trips = [(False, False), (False, False)]  # 2 x 100 = 200
    assert pass_advice(trips, 2, 150) == "buy_pass"


def test_pass_advice_either():
    trips = [(False, False), (False, False)]  # 200
    assert pass_advice(trips, 2, 200) == "either"


def test_pass_advice_pay_per_trip():
    trips = [(False, False), (False, False)]  # 200
    assert pass_advice(trips, 2, 500) == "pay_per_trip"


# ---- Added tests for BRANCH coverage (every decision both True and False) ----
@pytest.mark.parametrize("axles", [0, -1, -10])
def test_invalid_axle_counts_all_raise(axles):
    with pytest.raises(ValueError):
        toll_for(axles, True, True)


def test_two_axles_is_the_smallest_valid_count():
    assert toll_for(2, False, False) == 100  # boundary: axles < 2 is False


@pytest.mark.parametrize("axles, expected", [(2, 100), (3, 150), (4, 250), (5, 400), (10, 400)])
def test_base_toll_in_and_out_of_table(axles, expected):
    assert toll_for(axles, False, False) == expected


def test_peak_and_off_peak_differ():
    assert toll_for(3, True, False) == pytest.approx(187.5)
    assert toll_for(3, False, False) == 150


def test_no_fastag_means_no_discount():
    assert toll_for(2, True, False) == pytest.approx(125.0)
    assert toll_for(4, False, False) == 250


def test_peak_and_fastag_combined_two_axle():
    assert toll_for(2, True, True) == pytest.approx(112.5)


def test_peak_and_fastag_combined_other_axle():
    assert toll_for(3, True, True) == pytest.approx(178.13, abs=0.01)
    assert toll_for(6, True, True) == pytest.approx(475.0)


def test_result_is_rounded_to_two_decimals():
    assert toll_for(4, True, True) == pytest.approx(296.88, abs=0.01)


def test_exempt_vehicles_skip_axle_validation():
    assert toll_charge("ambulance", 1, True, True) == 0
    assert toll_charge("fire_engine", 0, False, False) == 0


def test_non_exempt_vehicle_with_invalid_axles_raises():
    with pytest.raises(ValueError):
        toll_charge("car", 1, False, False)


def test_unknown_vehicle_is_not_exempt():
    assert toll_charge("bus", 2, False, False) == 100
    assert toll_charge("", 2, False, False) == 100


def test_pass_advice_with_no_trips():
    assert pass_advice([], 2, 100) == "pay_per_trip"   # loop never runs
    assert pass_advice([], 2, 0) == "either"           # 0 == 0


def test_pass_advice_boundaries_around_pass_price():
    trips = [(False, False), (False, False)]  # 200
    assert pass_advice(trips, 2, 199) == "buy_pass"
    assert pass_advice(trips, 2, 200) == "either"
    assert pass_advice(trips, 2, 201) == "pay_per_trip"


def test_pass_advice_uses_peak_and_fastag_per_trip():
    trips = [(True, False), (False, True), (True, True)]  # 125 + 90 + 112.5
    assert pass_advice(trips, 2, 300) == "buy_pass"
    assert pass_advice(trips, 2, 400) == "pay_per_trip"


def test_pass_advice_invalid_axles_raises_when_there_are_trips():
    with pytest.raises(ValueError):
        pass_advice([(False, False)], 1, 100)

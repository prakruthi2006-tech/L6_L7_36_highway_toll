from hypothesis import given, strategies as st
from highway_toll import parse_plate, trip_cost, axle_class


# ---------------------------------------------------------------------------
# 1. "No crash" fuzz tests: any text (or None) must never raise an exception
# ---------------------------------------------------------------------------

@given(st.text() | st.none())
def test_parse_plate_no_crash(s):
    try:
        parse_plate(s)
    except Exception as e:
        assert False, f"parse_plate crashed with: {e!r}"


@given(st.text() | st.none())
def test_trip_cost_no_crash(s):
    try:
        trip_cost(s)
    except Exception as e:
        assert False, f"trip_cost crashed with: {e!r}"


@given(st.text() | st.none())
def test_axle_class_no_crash(s):
    try:
        axle_class(s)
    except Exception as e:
        assert False, f"axle_class crashed with: {e!r}"


# ---------------------------------------------------------------------------
# 2. More edge cases: other types (ints, floats, lists, bytes ...) must not crash
# ---------------------------------------------------------------------------

anything = st.one_of(
    st.none(), st.booleans(), st.integers(), st.floats(allow_nan=True),
    st.text(), st.binary(), st.lists(st.integers()),
)


@given(anything)
def test_parse_plate_any_type_no_crash(x):
    try:
        parse_plate(x)
    except Exception as e:
        assert False, f"parse_plate crashed with: {e!r}"


@given(anything)
def test_trip_cost_any_type_no_crash(x):
    try:
        trip_cost(x)
    except Exception as e:
        assert False, f"trip_cost crashed with: {e!r}"


@given(anything)
def test_axle_class_any_type_no_crash(x):
    try:
        axle_class(x)
    except Exception as e:
        assert False, f"axle_class crashed with: {e!r}"


# ---------------------------------------------------------------------------
# 3. Correctness properties: valid inputs must give the right answer,
#    invalid inputs must give None (never a wrong value)
# ---------------------------------------------------------------------------

letters = st.text(alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")


@given(
    state=st.text(alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz", min_size=2, max_size=2),
    district=st.integers(min_value=0, max_value=99),
    series=st.text(alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ", min_size=1, max_size=3),
    number=st.integers(min_value=0, max_value=9999),
)
def test_parse_plate_valid_plates(state, district, series, number):
    plate = f"{state}-{district:02d}-{series}-{number:04d}"
    assert parse_plate(plate) == (state.upper(), district, number)


@given(st.text(alphabet="abc-123 ", max_size=20))
def test_parse_plate_result_shape(s):
    result = parse_plate(s)
    assert result is None or (
        isinstance(result, tuple)
        and len(result) == 3
        and isinstance(result[0], str)
        and isinstance(result[1], int)
        and isinstance(result[2], int)
    )


@given(st.integers(min_value=0, max_value=10**6), st.integers(min_value=0, max_value=10**6))
def test_trip_cost_valid_values(count, rate):
    assert trip_cost(f"{count}x{rate}") == count * rate
    assert trip_cost(f"{count}X{rate}") == count * rate  # upper-case X also works


@given(st.text(alphabet="x0123456789- .", max_size=15))
def test_trip_cost_never_negative(s):
    result = trip_cost(s)
    assert result is None or result >= 0


@given(st.integers(min_value=2, max_value=10**6))
def test_axle_class_valid_counts(n):
    expected = "car" if n == 2 else "truck" if n <= 4 else "heavy"
    assert axle_class(n) == expected
    assert axle_class(str(n)) == expected


@given(st.integers(max_value=1))
def test_axle_class_rejects_fewer_than_two_axles(n):
    assert axle_class(n) is None
    assert axle_class(str(n)) is None


@given(st.text() | st.none())
def test_axle_class_only_known_classes(s):
    assert axle_class(s) in ("car", "truck", "heavy", None)

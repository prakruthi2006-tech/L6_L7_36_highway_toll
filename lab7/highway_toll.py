import re

# Plate format: STATE-DISTRICT-SERIES-NUMBER, e.g. KA-05-AB-1234
# (ASCII only; fullmatch so a trailing newline is not silently accepted)
PLATE_PATTERN = re.compile(r"([A-Za-z]{2})-([0-9]{1,2})-([A-Za-z]{1,3})-([0-9]{1,4})")
# Trips text: COUNTxRATE, e.g. 3x150 (x or X, digits only, so no negatives)
TRIP_PATTERN = re.compile(r"([0-9]{1,9})[xX]([0-9]{1,9})")


def parse_plate(plate):
    """Return (STATE, district, number) for a valid plate, otherwise None."""
    if not isinstance(plate, str):
        return None
    match = PLATE_PATTERN.fullmatch(plate.strip())
    if match is None:
        return None
    state, district, _series, number = match.groups()
    return state.upper(), int(district), int(number)


def trip_cost(text):
    """Return trips * rate for text like '3x150', otherwise None."""
    if not isinstance(text, str):
        return None
    match = TRIP_PATTERN.fullmatch(text.strip())
    if match is None:
        return None
    count, rate = match.groups()
    return int(count) * int(rate)


def axle_class(axles):
    """Return 'car', 'truck' or 'heavy' for a valid axle count, otherwise None."""
    # bool is a subclass of int, but True/False are not real axle counts
    if isinstance(axles, bool):
        return None
    if isinstance(axles, int):
        n = axles
    elif isinstance(axles, str):
        text = axles.strip()
        if not re.fullmatch(r"[0-9]{1,9}", text):
            return None
        n = int(text)
    else:
        return None

    if n < 2:
        return None
    if n == 2:
        return 'car'
    if n <= 4:
        return 'truck'
    return 'heavy'


def main():
    print("==== Running parse_plate ====")
    user_input = input("Enter a plate (e.g. KA-05-AB-1234): ")
    result = parse_plate(user_input)
    if result is None:
        print("Invalid plate. Expected format like KA-05-AB-1234")
    else:
        print("State, District and Number:", result)

    print("\n==== Running trip_cost ====")
    user_input = input("Enter trips x rate (e.g. 3x150): ")
    result = trip_cost(user_input)
    if result is None:
        print("Invalid input. Expected format like 3x150")
    else:
        print("Trip Cost:", result)

    print("\n==== Running axle_class ====")
    user_input = input("Enter an axle count (e.g. 3): ")
    result = axle_class(user_input)
    if result is None:
        print("Invalid axle count. Enter a whole number, 2 or more")
    else:
        print("Vehicle Class:", result)


if __name__ == "__main__":
    main()

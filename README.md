# L6_L7_36: Highway Toll Calculator

**Name:** <Prakruthi.NK>  **SRN:** <PES2UG24AM118>
**Course:** Software Engineering Lab

This repository contains my work for two labs on the same small Python module, a highway toll calculator.

| Lab | Topic | Folder |
|-----|-------|--------|
| Lab 6 | Code and branch coverage analysis | [`lab6/`](lab6) |
| Lab 7 | Fuzz testing with Hypothesis | [`lab7/`](lab7) |

## Setup

```
pip install pytest coverage hypothesis
```

---

## Lab 6: Code and Branch Coverage

The module `lab6/highway_toll.py` calculates tolls by axle count, peak hours and FASTag, and advises on monthly passes. The starter tests covered only **39%** of it.

| File | Purpose | Result |
|------|---------|--------|
| `CodeCoverageTest_highway_toll.py` | 11 tests for line coverage | **93%** line coverage |
| `BranchCoverageTest_highway_toll.py` | 35 tests covering both outcomes of every decision | **100%** line and branch coverage |
| `code_coverage_screenshot.png` | Terminal output for the code coverage run | |
| `branch_coverage_screenshot.png` | Terminal output for the branch coverage run | |

The two test files were committed separately: first the line coverage tests, then the branch coverage tests.

**How to run** (from the `lab6` folder):

```
python -m coverage run -m pytest CodeCoverageTest_highway_toll.py
python -m coverage report -m

python -m coverage run --branch -m pytest BranchCoverageTest_highway_toll.py
python -m coverage report -m
```

**What the branch tests added:**
- Invalid axle counts (0, 1, negative), including the boundary at 2 axles.
- Toll values inside and outside the base-toll table (2, 3, 4 axles, and 5 or more).
- Peak and off-peak, with and without FASTag, and both together for 2-axle and other vehicles.
- Exempt vehicles (ambulance, fire engine) skipping axle validation, and non-exempt vehicles that do not.
- `pass_advice` with no trips, and at, just below and just above the pass price.

---

## Lab 7: Fuzz Testing

The module `lab7/highway_toll.py` reads vehicle plates, prices trips and classifies vehicles by axle count. I used Hypothesis to find input-validation bugs, then fixed them.

| File | Purpose |
|------|---------|
| `highway_toll.py` | Fixed version of the program |
| `test_highway_toll.py` | 13 Hypothesis tests |
| `Lab7_Report.pdf` | Report with the 4 required screenshots |
| `screenshot1_buggy_app.png` … `screenshot4_tests_passing.png` | The same screenshots as separate files |

**Results:** on the original code, **10 of 13 tests failed**. On the fixed code, **all 13 pass**.

**Bugs found:**
- `parse_plate` crashed on text without exactly 4 parts, on non-numeric district or number, and on `None`.
- `trip_cost` crashed when there was no `x`, on non-numeric values, and on `None`.
- `axle_class` crashed on non-numeric text and `None`, and wrongly returned `truck` for 0, 1 or negative axles.

**Fix:** each function now checks its input (type and format) and returns `None` for invalid input instead of raising an exception. Plates and trip text are validated with strict patterns, and axle counts below 2 are rejected. The command-line program prints a clear message for invalid input.

**How to run** (from the `lab7` folder):

```
python highway_toll.py
python -m pytest test_highway_toll.py
```

**What the tests check:**
- No function crashes on any text, `None`, numbers, bytes or lists.
- Valid plates, trips and axle counts give the right answer.
- Invalid input gives `None`, and trip costs are never negative.

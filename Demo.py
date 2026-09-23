"""
INVESTMENT PLAN RETURN ANALYZER 
Muhammad Bilal Khan | Assignment No. 05 | Data Analysis
Educational project: descriptive comparison of two monthly return series.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import csv
import math

import numpy as np


PROJECT_TITLE = "INVESTMENT PLAN RETURN ANALYZER PRO"
STUDENT_NAME = "Muhammad Bilal Khan"
ASSIGNMENT_NO = "05"
SUBJECT = "Data Analysis"
ROLE = "Junior Data Analyst"

PLAN_A_NAME = "Plan A"
PLAN_B_NAME = "Plan B"
DEFAULT_STARTING_INVESTMENT = 100_000.00
REPORT_DIRECTORY = Path("investment_reports")

months = np.array([
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
])

short_months = np.array([
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
])

plan_a = np.array([
    4.20, 3.50, 5.10, 2.80, 4.70, 6.00,
    3.90, 5.40, 4.80, 6.20, 5.70, 7.10
], dtype=float)

plan_b = np.array([
    2.90, 4.60, 3.80, 5.20, 3.10, 4.90,
    5.70, 4.20, 6.10, 5.00, 6.50, 5.80
], dtype=float)


@dataclass(frozen=True)
class PlanStats:
    name: str
    average: float
    median: float
    minimum: float
    maximum: float
    std: float
    variance: float
    simple_total: float
    compounded: float
    range_value: float
    positive: int
    negative: int
    zero: int
    best_index: int
    worst_index: int


def line(char="=", width=88):
    print(char * width)


def title(text):
    print()
    line()
    print(text.center(88))
    line()


def subtitle(text):
    print()
    line("-")
    print(text.center(88))
    line("-")


def money(value):
    return f"Rs. {float(value):,.2f}"


def validate_data():
    if len(months) != 12:
        raise ValueError("Month data must contain exactly 12 months.")
    if plan_a.shape != plan_b.shape or len(plan_a) != len(months):
        raise ValueError("Both plans must contain 12 monthly values.")
    if not np.all(np.isfinite(plan_a)) or not np.all(np.isfinite(plan_b)):
        raise ValueError("Returns must contain only finite numeric values.")


def compounded_return(returns):
    factors = 1.0 + returns / 100.0
    if np.any(factors <= 0):
        raise ValueError("Returns of -100% or below cannot be compounded.")
    return float((np.prod(factors) - 1.0) * 100.0)


def cumulative_values(returns, starting_amount):
    if not math.isfinite(starting_amount) or starting_amount <= 0:
        raise ValueError("Starting investment must be greater than zero.")
    return starting_amount * np.cumprod(1.0 + returns / 100.0)


def drawdown(values):
    peak = np.maximum.accumulate(values)
    return (values / peak - 1.0) * 100.0


def calculate_stats(name, returns):
    return PlanStats(
        name=name,
        average=float(np.mean(returns)),
        median=float(np.median(returns)),
        minimum=float(np.min(returns)),
        maximum=float(np.max(returns)),
        std=float(np.std(returns)),
        variance=float(np.var(returns)),
        simple_total=float(np.sum(returns)),
        compounded=compounded_return(returns),
        range_value=float(np.ptp(returns)),
        positive=int(np.sum(returns > 0)),
        negative=int(np.sum(returns < 0)),
        zero=int(np.sum(returns == 0)),
        best_index=int(np.argmax(returns)),
        worst_index=int(np.argmin(returns)),
    )


def build_analysis(starting_amount=DEFAULT_STARTING_INVESTMENT):
    a = calculate_stats(PLAN_A_NAME, plan_a)
    b = calculate_stats(PLAN_B_NAME, plan_b)
    values_a = cumulative_values(plan_a, starting_amount)
    values_b = cumulative_values(plan_b, starting_amount)
    difference = plan_a - plan_b
    return {
        "a": a,
        "b": b,
        "values_a": values_a,
        "values_b": values_b,
        "difference": difference,
        "a_higher": int(np.sum(difference > 0)),
        "b_higher": int(np.sum(difference < 0)),
        "equal": int(np.sum(difference == 0)),
        "correlation": float(np.corrcoef(plan_a, plan_b)[0, 1]),
        "max_drawdown_a": float(np.min(drawdown(values_a))),
        "max_drawdown_b": float(np.min(drawdown(values_b))),
        "starting_amount": starting_amount,
    }


def welcome():
    title(PROJECT_TITLE)
    print(f"Student       : {STUDENT_NAME}")
    print(f"Assignment No.: {ASSIGNMENT_NO}")
    print(f"Subject       : {SUBJECT}")
    print(f"Role          : {ROLE}")
    print("Technology    : Python + NumPy")
    print()
    print("Educational analysis only. It does not provide financial advice.")


def show_dataset():
    title("MONTHLY DATA")
    print(f"{'Month':<15}{PLAN_A_NAME:>15}{PLAN_B_NAME:>15}{'Difference':>18}")
    line("-")
    for month, a, b in zip(months, plan_a, plan_b):
        print(f"{month:<15}{a:>12.2f}%{b:>15.2f}%{a-b:>15.2f}%")
    line("-")


def show_summary(data):
    subtitle("STATISTICAL SUMMARY")
    print(f"{'Metric':<28}{PLAN_A_NAME:>20}{PLAN_B_NAME:>20}")
    line("-")
    rows = [
        ("Average Return", data["a"].average, data["b"].average, "%"),
        ("Median Return", data["a"].median, data["b"].median, "%"),
        ("Minimum Return", data["a"].minimum, data["b"].minimum, "%"),
        ("Maximum Return", data["a"].maximum, data["b"].maximum, "%"),
        ("Standard Deviation", data["a"].std, data["b"].std, "%"),
        ("Variance", data["a"].variance, data["b"].variance, ""),
        ("Simple Total Return", data["a"].simple_total, data["b"].simple_total, "%"),
        ("Compounded Return", data["a"].compounded, data["b"].compounded, "%"),
        ("Return Range", data["a"].range_value, data["b"].range_value, "%"),
        ("Positive Months", data["a"].positive, data["b"].positive, ""),
        ("Negative Months", data["a"].negative, data["b"].negative, ""),
    ]
    for label, a, b, suffix in rows:
        if suffix == "%":
            print(f"{label:<28}{a:>18.2f}%{b:>18.2f}%")
        elif isinstance(a, float):
            print(f"{label:<28}{a:>20.4f}{b:>20.4f}")
        else:
            print(f"{label:<28}{a:>20}{b:>20}")


def show_best_worst(data):
    subtitle("BEST AND WORST MONTHS")
    for stats, values in ((data["a"], plan_a), (data["b"], plan_b)):
        print(f"{stats.name} best : {months[stats.best_index]} ({values[stats.best_index]:.2f}%)")
        print(f"{stats.name} worst: {months[stats.worst_index]} ({values[stats.worst_index]:.2f}%)")


def show_comparison(data):
    subtitle("MONTH-BY-MONTH COMPARISON")
    for month, a, b, d in zip(months, plan_a, plan_b, data["difference"]):
        status = "Plan A higher" if d > 0 else "Plan B higher" if d < 0 else "Equal"
        print(f"{month:<15} A={a:>7.2f}% | B={b:>7.2f}% | Difference={d:>+7.2f}% | {status}")
    print()
    print(f"Plan A higher months: {data['a_higher']}")
    print(f"Plan B higher months: {data['b_higher']}")
    print(f"Equal months        : {data['equal']}")


def show_cumulative(data):
    subtitle("CUMULATIVE INVESTMENT GROWTH")
    print(f"Starting investment: {money(data['starting_amount'])}")
    print(f"{'Month':<15}{'Plan A Value':>24}{'Plan B Value':>24}")
    line("-")
    for m, a, b in zip(months, data["values_a"], data["values_b"]):
        print(f"{m:<15}{money(a):>24}{money(b):>24}")
    line("-")
    print(f"Final Plan A value: {money(data['values_a'][-1])}")
    print(f"Final Plan B value: {money(data['values_b'][-1])}")


def show_advanced(data):
    subtitle("ADVANCED DESCRIPTIVE ANALYSIS")
    print(f"Correlation coefficient : {data['correlation']:.4f}")
    print(f"Plan A maximum drawdown : {data['max_drawdown_a']:.2f}%")
    print(f"Plan B maximum drawdown : {data['max_drawdown_b']:.2f}%")
    print()
    print("25th / 50th / 75th percentiles:")
    print(f"Plan A: {np.percentile(plan_a, [25, 50, 75])}")
    print(f"Plan B: {np.percentile(plan_b, [25, 50, 75])}")
    print()
    print("These are descriptive statistics for the supplied sample.")


def make_report(data):
    rows = [
        "=" * 88,
        PROJECT_TITLE.center(88),
        "=" * 88,
        f"Student       : {STUDENT_NAME}",
        f"Assignment No.: {ASSIGNMENT_NO}",
        f"Generated     : {datetime.now():%d-%m-%Y %I:%M:%S %p}",
        "",
        "MONTHLY DATA",
        "-" * 88,
        f"{'Month':<15}{PLAN_A_NAME:>15}{PLAN_B_NAME:>15}{'Difference':>18}",
    ]
    for m, a, b in zip(months, plan_a, plan_b):
        rows.append(f"{m:<15}{a:>12.2f}%{b:>15.2f}%{a-b:>15.2f}%")
    rows += [
        "",
        "SUMMARY",
        "-" * 88,
        f"Plan A average       : {data['a'].average:.2f}%",
        f"Plan B average       : {data['b'].average:.2f}%",
        f"Plan A compounded    : {data['a'].compounded:.2f}%",
        f"Plan B compounded    : {data['b'].compounded:.2f}%",
        f"Plan A volatility    : {data['a'].std:.2f}%",
        f"Plan B volatility    : {data['b'].std:.2f}%",
        f"Correlation          : {data['correlation']:.4f}",
        f"Plan A higher months : {data['a_higher']}",
        f"Plan B higher months : {data['b_higher']}",
        f"Equal months         : {data['equal']}",
        f"Final Plan A value   : {money(data['values_a'][-1])}",
        f"Final Plan B value   : {money(data['values_b'][-1])}",
        "",
        "DISCLAIMER",
        "-" * 88,
        "Educational data analysis only. No financial advice or future-return forecast.",
        "=" * 88,
    ]
    return "\n".join(rows)


def save_report(data):
    REPORT_DIRECTORY.mkdir(parents=True, exist_ok=True)
    path = REPORT_DIRECTORY / f"investment_report_{datetime.now():%Y%m%d_%H%M%S}.txt"
    path.write_text(make_report(data), encoding="utf-8")
    return path


def export_csv(data):
    REPORT_DIRECTORY.mkdir(parents=True, exist_ok=True)
    path = REPORT_DIRECTORY / "investment_monthly_analysis.csv"
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Month", "Plan A Return (%)", "Plan B Return (%)",
            "Difference (%)", "Plan A Value", "Plan B Value"
        ])
        for i, month in enumerate(months):
            writer.writerow([
                month, f"{plan_a[i]:.4f}", f"{plan_b[i]:.4f}",
                f"{data['difference'][i]:.4f}",
                f"{data['values_a'][i]:.2f}",
                f"{data['values_b'][i]:.2f}",
            ])
    return path


def complete_report(data):
    welcome()
    print("\nData validation completed successfully.")
    show_dataset()
    show_summary(data)
    show_best_worst(data)
    show_comparison(data)
    show_cumulative(data)
    show_advanced(data)


def get_starting_amount(default):
    while True:
        raw = input(f"Starting investment [{default:,.2f}]: ").strip()
        if not raw:
            return default
        try:
            value = float(raw)
            if math.isfinite(value) and value > 0:
                return value
        except ValueError:
            pass
        print("Enter a valid amount greater than zero.")


def menu():
    starting_amount = DEFAULT_STARTING_INVESTMENT
    data = build_analysis(starting_amount)

    while True:
        title("INVESTMENT ANALYTICS PRO MENU")
        print("1. Dataset Information")
        print("2. Monthly Data")
        print("3. Statistical Summary")
        print("4. Best / Worst Months")
        print("5. Month-by-Month Comparison")
        print("6. Cumulative Investment Analysis")
        print("7. Advanced Analysis")
        print("8. Change Starting Investment")
        print("9. Generate Text Report")
        print("10. Export CSV")
        print("11. Complete Professional Report")
        print("0. Exit")
        line()

        choice = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                title("DATASET INFORMATION")
                print(f"Months: {len(months)}")
                print(f"Plan A observations: {len(plan_a)}")
                print(f"Plan B observations: {len(plan_b)}")
                print(f"Plan A shape: {plan_a.shape}")
                print(f"Plan B shape: {plan_b.shape}")

            elif choice == "2":
                show_dataset()

            elif choice == "3":
                show_summary(data)

            elif choice == "4":
                show_best_worst(data)

            elif choice == "5":
                show_comparison(data)

            elif choice == "6":
                show_cumulative(data)

            elif choice == "7":
                show_advanced(data)

            elif choice == "8":
                starting_amount = get_starting_amount(starting_amount)
                data = build_analysis(starting_amount)
                print(f"Starting investment updated to {money(starting_amount)}.")

            elif choice == "9":
                path = save_report(data)
                print(f"Report saved: {path.resolve()}")

            elif choice == "10":
                path = export_csv(data)
                print(f"CSV saved: {path.resolve()}")

            elif choice == "11":
                complete_report(data)

            elif choice == "0":
                print("\nThank you for using Investment Plan Return Analyzer Pro!")
                break

            else:
                print("Invalid choice. Select 0 to 11.")

        except (ValueError, OSError, csv.Error) as error:
            print(f"Operation failed: {error}")

        if choice != "0":
            input("\nPress Enter to continue...")


def main():
    try:
        validate_data()
        menu()
    except KeyboardInterrupt:
        print("\nProgram interrupted safely.")
    except Exception as error:
        print(f"Program error: {error}")


if __name__ == "__main__":
    main()

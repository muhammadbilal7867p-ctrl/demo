# Name : Muhammmad Bilal Khan 
# Assignment No : 05
# =====================================================================
#              INVESTMENT PLAN RETURN ANALYZER
# =====================================================================
# Assignment Scenario:
#
# You are working as a Junior Data Analyst for an investment company.
# The company wants to compare the monthly returns of two investment
# plans.
#
# Technology Used:
#
# Main Objectives:
#   1. Store monthly investment returns using NumPy arrays
#   2. Calculate average returns
#   3. Calculate median returns
#   4. Calculate maximum and minimum returns
#   5. Calculate standard deviation
#   6. Calculate variance
#   7. Calculate total returns
#   8. Calculate compounded returns
#   9. Compare monthly performance
#  10. Calculate cumulative growth
#  11. Identify best and worst months
#  12. Count positive and negative months
#  13. Generate a detailed analytical report
#
# Note:
# This project is for educational data analysis.
# It does not provide financial advice.
# =====================================================================


import numpy as np


# =====================================================================
# 1. PROJECT INFORMATION
# =====================================================================

PROJECT_TITLE = "INVESTMENT PLAN RETURN ANALYZER"

STUDENT_NAME = "Muhammad Bilal"

ASSIGNMENT_TITLE = (
    "Comparison of Monthly Returns of Two Investment Plans"
)

SUBJECT = "Data Analysis"

ROLE = "Junior Data Analyst"


# =====================================================================
# 2. MONTH NAMES
# =====================================================================

months = np.array([
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
])


short_months = np.array([
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec"
])


# =====================================================================
# 3. INVESTMENT PLAN DATA
# =====================================================================
#
# All values represent monthly percentage returns.
#
# Example:
# 4.50 means 4.50% monthly return.
#
# Replace these values with the actual assignment data.
# =====================================================================

plan_a = np.array([
    4.20,
    3.50,
    5.10,
    2.80,
    4.70,
    6.00,
    3.90,
    5.40,
    4.80,
    6.20,
    5.70,
    7.10
], dtype=float)


plan_b = np.array([
    2.90,
    4.60,
    3.80,
    5.20,
    3.10,
    4.90,
    5.70,
    4.20,
    6.10,
    5.00,
    6.50,
    5.80
], dtype=float)


# =====================================================================
# 4. BASIC DISPLAY FUNCTIONS
# =====================================================================

def line(character="=", length=80):

    print(
        character * length
    )


def title(text):

    print()
    line()

    print(
        text.center(80)
    )

    line()


def subtitle(text):

    print()
    line("-")

    print(
        text.center(80)
    )

    line("-")


# =====================================================================
# 5. WELCOME SCREEN
# =====================================================================

def welcome():

    title(
        PROJECT_TITLE
    )

    print(
        f"Student Name : {STUDENT_NAME}"
    )

    print(
        f"Assignment   : {ASSIGNMENT_TITLE}"
    )

    print(
        f"Subject      : {SUBJECT}"
    )

    print(
        f"Role         : {ROLE}"
    )

    print()

    print(
        "Purpose:"
    )

    print(
        "This project uses NumPy to analyze and compare "
        "the monthly returns of two investment plans."
    )

    print()

    print(
        "Technology: NumPy"
    )


# =====================================================================
# 6. DATA VALIDATION
# =====================================================================

def validate_data():

    # Check number of months.

    if len(months) != 12:

        raise ValueError(
            "The month array must contain 12 months."
        )


    # Check Plan A.

    if len(plan_a) != 12:

        raise ValueError(
            "Plan A must contain exactly 12 monthly returns."
        )


    # Check Plan B.

    if len(plan_b) != 12:

        raise ValueError(
            "Plan B must contain exactly 12 monthly returns."
        )


    # Check for invalid numeric values.

    if not np.all(
        np.isfinite(plan_a)
    ):

        raise ValueError(
            "Plan A contains invalid numeric values."
        )


    if not np.all(
        np.isfinite(plan_b)
    ):

        raise ValueError(
            "Plan B contains invalid numeric values."
        )


    print(
        "\nData validation completed successfully."
    )


# =====================================================================
# 7. DATASET INFORMATION
# =====================================================================

def dataset_information():

    title(
        "DATASET INFORMATION"
    )

    print(
        f"Number of months       : {len(months)}"
    )

    print(
        f"Plan A observations    : {len(plan_a)}"
    )

    print(
        f"Plan B observations    : {len(plan_b)}"
    )

    print(
        f"Plan A data type       : {plan_a.dtype}"
    )

    print(
        f"Plan B data type       : {plan_b.dtype}"
    )

    print(
        f"Plan A shape           : {plan_a.shape}"
    )

    print(
        f"Plan B shape           : {plan_b.shape}"
    )


# =====================================================================
# 8. RAW DATA DISPLAY
# =====================================================================

def display_raw_data():

    title(
        "MONTHLY INVESTMENT DATA"
    )

    print(
        f"{'Month':<15}"
        f"{'Plan A':>15}"
        f"{'Plan B':>15}"
        f"{'Difference':>18}"
    )

    line("-")

    for i in range(
        len(months)
    ):

        difference = (
            plan_a[i]
            - plan_b[i]
        )

        print(
            f"{months[i]:<15}"
            f"{plan_a[i]:>12.2f}%"
            f"{plan_b[i]:>15.2f}%"
            f"{difference:>15.2f}%"
        )

    line("-")


# =====================================================================
# 9. AVERAGE ANALYSIS
# =====================================================================

def average_analysis():

    average_a = np.mean(
        plan_a
    )

    average_b = np.mean(
        plan_b
    )

    subtitle(
        "AVERAGE MONTHLY RETURN"
    )

    print(
        f"{'Plan A Average':<30}"
        f"{average_a:.2f}%"
    )

    print(
        f"{'Plan B Average':<30}"
        f"{average_b:.2f}%"
    )

    print()

    print(
        f"Average difference: "
        f"{average_a - average_b:+.2f}%"
    )


# =====================================================================
# 10. MEDIAN ANALYSIS
# =====================================================================

def median_analysis():

    median_a = np.median(
        plan_a
    )

    median_b = np.median(
        plan_b
    )

    subtitle(
        "MEDIAN MONTHLY RETURN"
    )

    print(
        f"Plan A Median: {median_a:.2f}%"
    )

    print(
        f"Plan B Median: {median_b:.2f}%"
    )


# =====================================================================
# 11. MINIMUM AND MAXIMUM
# =====================================================================

def extreme_analysis():

    maximum_a = np.max(
        plan_a
    )

    maximum_b = np.max(
        plan_b
    )

    minimum_a = np.min(
        plan_a
    )

    minimum_b = np.min(
        plan_b
    )

    subtitle(
        "MINIMUM AND MAXIMUM RETURN"
    )

    print(
        f"Plan A Maximum: {maximum_a:.2f}%"
    )

    print(
        f"Plan A Minimum: {minimum_a:.2f}%"
    )

    print()

    print(
        f"Plan B Maximum: {maximum_b:.2f}%"
    )

    print(
        f"Plan B Minimum: {minimum_b:.2f}%"
    )


# =====================================================================
# 12. STANDARD DEVIATION
# =====================================================================

def volatility_analysis():

    standard_a = np.std(
        plan_a
    )

    standard_b = np.std(
        plan_b
    )

    subtitle(
        "VOLATILITY ANALYSIS"
    )

    print(
        f"Plan A Standard Deviation: "
        f"{standard_a:.2f}%"
    )

    print(
        f"Plan B Standard Deviation: "
        f"{standard_b:.2f}%"
    )

    print()

    print(
        "Standard deviation describes how much the "
        "monthly returns vary around their average."
    )


# =====================================================================
# 13. VARIANCE
# =====================================================================

def variance_analysis():

    variance_a = np.var(
        plan_a
    )

    variance_b = np.var(
        plan_b
    )

    subtitle(
        "VARIANCE ANALYSIS"
    )

    print(
        f"Plan A Variance: "
        f"{variance_a:.4f}"
    )

    print(
        f"Plan B Variance: "
        f"{variance_b:.4f}"
    )


# =====================================================================
# 14. SIMPLE TOTAL RETURN
# =====================================================================

def total_return_analysis():

    total_a = np.sum(
        plan_a
    )

    total_b = np.sum(
        plan_b
    )

    subtitle(
        "TOTAL MONTHLY RETURN"
    )

    print(
        f"Plan A Total Return: "
        f"{total_a:.2f}%"
    )

    print(
        f"Plan B Total Return: "
        f"{total_b:.2f}%"
    )

    print()

    print(
        f"Difference: "
        f"{total_a - total_b:+.2f}%"
    )


# =====================================================================
# 15. COMPOUNDED RETURN
# =====================================================================

def compounded_return(returns):

    growth_factor = np.prod(
        1 + returns / 100
    )

    return (
        growth_factor - 1
    ) * 100


def compounded_analysis():

    compound_a = compounded_return(
        plan_a
    )

    compound_b = compounded_return(
        plan_b
    )

    subtitle(
        "COMPOUNDED RETURN"
    )

    print(
        f"Plan A Compounded Return: "
        f"{compound_a:.2f}%"
    )

    print(
        f"Plan B Compounded Return: "
        f"{compound_b:.2f}%"
    )


# =====================================================================
# 16. POSITIVE MONTH ANALYSIS
# =====================================================================

def positive_month_analysis():

    positive_a = np.sum(
        plan_a > 0
    )

    positive_b = np.sum(
        plan_b > 0
    )

    subtitle(
        "POSITIVE MONTH ANALYSIS"
    )

    print(
        f"Plan A Positive Months: "
        f"{positive_a}"
    )

    print(
        f"Plan B Positive Months: "
        f"{positive_b}"
    )


# =====================================================================
# 17. NEGATIVE MONTH ANALYSIS
# =====================================================================

def negative_month_analysis():

    negative_a = np.sum(
        plan_a < 0
    )

    negative_b = np.sum(
        plan_b < 0
    )

    subtitle(
        "NEGATIVE MONTH ANALYSIS"
    )

    print(
        f"Plan A Negative Months: "
        f"{negative_a}"
    )

    print(
        f"Plan B Negative Months: "
        f"{negative_b}"
    )


# =====================================================================
# 18. BEST MONTH
# =====================================================================

def best_month_analysis():

    best_a_index = np.argmax(
        plan_a
    )

    best_b_index = np.argmax(
        plan_b
    )

    subtitle(
        "BEST PERFORMING MONTH"
    )

    print(
        f"Plan A:"
    )

    print(
        f"Month  : {months[best_a_index]}"
    )

    print(
        f"Return : {plan_a[best_a_index]:.2f}%"
    )

    print()

    print(
        f"Plan B:"
    )

    print(
        f"Month  : {months[best_b_index]}"
    )

    print(
        f"Return : {plan_b[best_b_index]:.2f}%"
    )


# =====================================================================
# 19. WORST MONTH
# =====================================================================

def worst_month_analysis():

    worst_a_index = np.argmin(
        plan_a
    )

    worst_b_index = np.argmin(
        plan_b
    )

    subtitle(
        "LOWEST PERFORMING MONTH"
    )

    print(
        f"Plan A:"
    )

    print(
        f"Month  : {months[worst_a_index]}"
    )

    print(
        f"Return : {plan_a[worst_a_index]:.2f}%"
    )

    print()

    print(
        f"Plan B:"
    )

    print(
        f"Month  : {months[worst_b_index]}"
    )

    print(
        f"Return : {plan_b[worst_b_index]:.2f}%"
    )


# =====================================================================
# 20. MONTH-BY-MONTH COMPARISON
# =====================================================================

def monthly_comparison():

    subtitle(
        "MONTH-BY-MONTH COMPARISON"
    )

    differences = (
        plan_a - plan_b
    )

    for i in range(
        len(months)
    ):

        if differences[i] > 0:

            status = (
                "Plan A higher"
            )

        elif differences[i] < 0:

            status = (
                "Plan B higher"
            )

        else:

            status = "Equal"

        print(
            f"{months[i]:<15}"
            f"A = {plan_a[i]:>6.2f}% | "
            f"B = {plan_b[i]:>6.2f}% | "
            f"{status}"
        )


# =====================================================================
# 21. MONTHS WHERE PLAN A IS HIGHER
# =====================================================================

def plan_a_higher_months():

    condition = (
        plan_a > plan_b
    )

    count = np.sum(
        condition
    )

    subtitle(
        "PLAN A HIGHER-RETURN MONTHS"
    )

    print(
        f"Number of months: {count}"
    )

    if count > 0:

        selected_months = (
            months[condition]
        )

        print(
            "Months:"
        )

        print(
            ", ".join(
                selected_months
            )
        )


# =====================================================================
# 22. MONTHS WHERE PLAN B IS HIGHER
# =====================================================================

def plan_b_higher_months():

    condition = (
        plan_b > plan_a
    )

    count = np.sum(
        condition
    )

    subtitle(
        "PLAN B HIGHER-RETURN MONTHS"
    )

    print(
        f"Number of months: {count}"
    )

    if count > 0:

        selected_months = (
            months[condition]
        )

        print(
            "Months:"
        )

        print(
            ", ".join(
                selected_months
            )
        )


# =====================================================================
# 23. CUMULATIVE GROWTH
# =====================================================================

def cumulative_growth(
    returns,
    starting_amount
):

    monthly_growth = (
        1 + returns / 100
    )

    cumulative_factor = np.cumprod(
        monthly_growth
    )

    values = (
        starting_amount
        * cumulative_factor
    )

    return values


# =====================================================================
# 24. CUMULATIVE INVESTMENT ANALYSIS
# =====================================================================

def cumulative_analysis():

    starting_amount = 100000.0

    values_a = cumulative_growth(
        plan_a,
        starting_amount
    )

    values_b = cumulative_growth(
        plan_b,
        starting_amount
    )

    subtitle(
        "CUMULATIVE INVESTMENT ANALYSIS"
    )

    print(
        f"Starting Amount: "
        f"Rs. {starting_amount:,.2f}"
    )

    print()

    print(
        f"{'Month':<15}"
        f"{'Plan A Value':>22}"
        f"{'Plan B Value':>22}"
    )

    line("-")

    for i in range(
        len(months)
    ):

        print(
            f"{months[i]:<15}"
            f"Rs. {values_a[i]:>15,.2f}"
            f"Rs. {values_b[i]:>20,.2f}"
        )

    line("-")

    print(
        f"Final Plan A Value: "
        f"Rs. {values_a[-1]:,.2f}"
    )

    print(
        f"Final Plan B Value: "
        f"Rs. {values_b[-1]:,.2f}"
    )


# =====================================================================
# 25. RANGE ANALYSIS
# =====================================================================

def range_analysis():

    range_a = (
        np.ptp(plan_a)
    )

    range_b = (
        np.ptp(plan_b)
    )

    subtitle(
        "RETURN RANGE ANALYSIS"
    )

    print(
        f"Plan A Range: "
        f"{range_a:.2f}%"
    )

    print(
        f"Plan B Range: "
        f"{range_b:.2f}%"
    )


# =====================================================================
# 26. PERCENTILE ANALYSIS
# =====================================================================

def percentile_analysis():

    q25_a = np.percentile(
        plan_a,
        25
    )

    q50_a = np.percentile(
        plan_a,
        50
    )

    q75_a = np.percentile(
        plan_a,
        75
    )

    q25_b = np.percentile(
        plan_b,
        25
    )

    q50_b = np.percentile(
        plan_b,
        50
    )

    q75_b = np.percentile(
        plan_b,
        75
    )

    subtitle(
        "PERCENTILE ANALYSIS"
    )

    print(
        f"{'Percentile':<20}"
        f"{'Plan A':>15}"
        f"{'Plan B':>15}"
    )

    print("-" * 50)

    print(
        f"{'25th Percentile':<20}"
        f"{q25_a:>14.2f}%"
        f"{q25_b:>14.2f}%"
    )

    print(
        f"{'50th Percentile':<20}"
        f"{q50_a:>14.2f}%"
        f"{q50_b:>14.2f}%"
    )

    print(
        f"{'75th Percentile':<20}"
        f"{q75_a:>14.2f}%"
        f"{q75_b:>14.2f}%"
    )


# =====================================================================
# 27. CORRELATION ANALYSIS
# =====================================================================

def correlation_analysis():

    correlation_matrix = np.corrcoef(
        plan_a,
        plan_b
    )

    correlation = (
        correlation_matrix[0, 1]
    )

    subtitle(
        "CORRELATION ANALYSIS"
    )

    print(
        "Correlation coefficient:"
    )

    print(
        f"{correlation:.4f}"
    )

    print()

    print(
        "The correlation measures how the two sets of "
        "monthly returns move together in the supplied dataset."
    )


# =====================================================================
# 28. OVERALL SUMMARY
# =====================================================================

def overall_summary():

    average_a = np.mean(
        plan_a
    )

    average_b = np.mean(
        plan_b
    )

    compound_a = compounded_return(
        plan_a
    )

    compound_b = compounded_return(
        plan_b
    )

    volatility_a = np.std(
        plan_a
    )

    volatility_b = np.std(
        plan_b
    )

    subtitle(
        "OVERALL DATA ANALYSIS SUMMARY"
    )

    print(
        f"{'Metric':<35}"
        f"{'Plan A':>18}"
        f"{'Plan B':>18}"
    )

    line("-")

    print(
        f"{'Average Return':<35}"
        f"{average_a:>16.2f}%"
        f"{average_b:>16.2f}%"
    )

    print(
        f"{'Compounded Return':<35}"
        f"{compound_a:>16.2f}%"
        f"{compound_b:>16.2f}%"
    )

    print(
        f"{'Volatility':<35}"
        f"{volatility_a:>16.2f}%"
        f"{volatility_b:>16.2f}%"
    )

    line("-")

    print()

    print(
        "This summary describes the supplied monthly data."
    )

    print(
        "It should not be interpreted as a forecast "
        "of future investment performance."
    )


# =====================================================================
# 29. COMPLETE REPORT
# =====================================================================

def complete_report():

    welcome()

    validate_data()

    dataset_information()

    display_raw_data()

    average_analysis()

    median_analysis()

    extreme_analysis()

    total_return_analysis()

    compounded_analysis()

    volatility_analysis()

    variance_analysis()

    positive_month_analysis()

    negative_month_analysis()

    best_month_analysis()

    worst_month_analysis()

    monthly_comparison()

    plan_a_higher_months()

    plan_b_higher_months()

    cumulative_analysis()

    range_analysis()

    percentile_analysis()

    correlation_analysis()

    overall_summary()


# =====================================================================
# 30. INTERACTIVE MENU
# =====================================================================

def menu():

    while True:

        print()

        line()

        print(
            "INVESTMENT ANALYTICS MENU".center(80)
        )

        line()

        print(
            "1.  Dataset Information"
        )

        print(
            "2.  View Monthly Data"
        )

        print(
            "3.  Average Return"
        )

        print(
            "4.  Median Return"
        )

        print(
            "5.  Minimum / Maximum"
        )

        print(
            "6.  Volatility"
        )

        print(
            "7.  Variance"
        )

        print(
            "8.  Total Return"
        )

        print(
            "9.  Compounded Return"
        )

        print(
            "10. Positive Months"
        )

        print(
            "11. Negative Months"
        )

        print(
            "12. Best Month"
        )

        print(
            "13. Worst Month"
        )

        print(
            "14. Month-by-Month Comparison"
        )

        print(
            "15. Plan A Higher Months"
        )

        print(
            "16. Plan B Higher Months"
        )

        print(
            "17. Cumulative Investment"
        )

        print(
            "18. Range Analysis"
        )

        print(
            "19. Percentile Analysis"
        )

        print(
            "20. Correlation Analysis"
        )

        print(
            "21. Complete Report"
        )

        print(
            "0.  Exit"
        )

        line()

        choice = input(
            "Enter your choice: "
        ).strip()

        try:

            if choice == "1":

                dataset_information()

            elif choice == "2":

                display_raw_data()

            elif choice == "3":

                average_analysis()

            elif choice == "4":

                median_analysis()

            elif choice == "5":

                extreme_analysis()

            elif choice == "6":

                volatility_analysis()

            elif choice == "7":

                variance_analysis()

            elif choice == "8":

                total_return_analysis()

            elif choice == "9":

                compounded_analysis()

            elif choice == "10":

                positive_month_analysis()

            elif choice == "11":

                negative_month_analysis()

            elif choice == "12":

                best_month_analysis()

            elif choice == "13":

                worst_month_analysis()

            elif choice == "14":

                monthly_comparison()

            elif choice == "15":

                plan_a_higher_months()

            elif choice == "16":

                plan_b_higher_months()

            elif choice == "17":

                cumulative_analysis()

            elif choice == "18":

                range_analysis()

            elif choice == "19":

                percentile_analysis()

            elif choice == "20":

                correlation_analysis()

            elif choice == "21":

                complete_report()

            elif choice == "0":

                print()

                line()

                print(
                    "Thank you for using "
                    "Investment Plan Return Analyzer!"
                )

                line()

                break

            else:

                print(
                    "\nInvalid choice."
                )

                print(
                    "Please select a number from 0 to 21."
                )

        except Exception as error:

            print(
                f"\nAn error occurred: {error}"
            )

        if choice != "0":

            input(
                "\nPress Enter to continue..."
            )


# =====================================================================
# 31. MAIN PROGRAM
# =====================================================================

def main():

    try:

        validate_data()

        menu()

    except KeyboardInterrupt:

        print(
            "\n\nProgram interrupted by user."
        )

    except Exception as error:

        print(
            f"\nProgram error: {error}"
        )


# =====================================================================
# 32. PROGRAM START
# =====================================================================

if __name__ == "__main__":

    main()


# =====================================================================
#                         END OF PROGRAM
# =====================================================================
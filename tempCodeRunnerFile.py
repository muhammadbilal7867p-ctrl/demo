import math
import json
from datetime import datetime

import numpy as np
import streamlit as st


# ============================================================
# PROJECT INFORMATION
# ============================================================
APP_TITLE = "Residential Electricity Management System"
STUDENT_NAME = "Muhammad Bilal"
BATCH = "317"

# ============================================================
# ELECTRICITY TARIFF
# ============================================================
FIXED_SURCHARGE = 150.00

TIER_1_LIMIT = 1000.00
TIER_2_LIMIT = 2000.00

TIER_1_RATE = 100.00
TIER_2_RATE = 150.00
TIER_3_RATE = 200.00


# ============================================================
# STREAMLIT PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# SESSION STATE
# ============================================================
if "customers" not in st.session_state:
    st.session_state.customers = []

if "next_customer_id" not in st.session_state:
    st.session_state.next_customer_id = 1001


# ============================================================
# CUSTOM CSS
# ============================================================
st.markdown(
    """
    <style>
        .main-title {
            text-align: center;
            font-size: 42px;
            font-weight: 800;
            margin-bottom: 0;
        }

        .sub-title {
            text-align: center;
            font-size: 17px;
            opacity: 0.75;
            margin-bottom: 25px;
        }

        .bill-box {
            border: 2px solid rgba(128, 128, 128, 0.35);
            border-radius: 16px;
            padding: 25px;
            margin-top: 15px;
        }

        .bill-total {
            text-align: center;
            font-size: 34px;
            font-weight: 800;
            padding: 20px;
            border-radius: 15px;
            border: 2px solid rgba(128, 128, 128, 0.35);
        }

        .section-title {
            font-size: 25px;
            font-weight: 700;
            margin-top: 10px;
        }

        div[data-testid="stMetric"] {
            border: 1px solid rgba(128, 128, 128, 0.25);
            border-radius: 12px;
            padding: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# VALIDATION FUNCTIONS
# ============================================================
def valid_text(value):
    return bool(value and value.strip())


def valid_phone(phone):
    return phone.isdigit() and 10 <= len(phone) <= 15


def valid_meter(meter):
    return bool(meter and meter.strip())


def valid_reading(value):
    return math.isfinite(float(value)) and float(value) >= 0


# ============================================================
# NUMPY BILLING ENGINE
# ============================================================
def calculate_bill(units):
    """
    Calculate electricity charges using NumPy arrays.

    Slabs:
        First 100 units  -> Rs. 10/unit
        Next 200 units   -> Rs. 15/unit
        Above 300 units  -> Rs. 20/unit
    """

    units = max(float(units), 0.0)

    slab_units = np.array(
        [
            min(units, TIER_1_LIMIT),
            min(max(units - TIER_1_LIMIT, 0.0), TIER_2_LIMIT),
            max(units - (TIER_1_LIMIT + TIER_2_LIMIT), 0.0),
        ],
        dtype=float,
    )

    rates = np.array(
        [TIER_1_RATE, TIER_2_RATE, TIER_3_RATE],
        dtype=float,
    )

    slab_charges = slab_units * rates

    energy_charge = float(np.sum(slab_charges))
    total_bill = energy_charge + FIXED_SURCHARGE

    average_energy_cost = (
        energy_charge / units if units > 0 else 0.0
    )

    return {
        "slab_units": slab_units,
        "rates": rates,
        "slab_charges": slab_charges,
        "energy_charge": energy_charge,
        "surcharge": FIXED_SURCHARGE,
        "total_bill": total_bill,
        "average_energy_cost": average_energy_cost,
    }


# ============================================================
# ANALYTICS FUNCTIONS
# ============================================================
def get_arrays():
    """Convert stored customer records into NumPy arrays."""

    if not st.session_state.customers:
        return (
            np.array([], dtype=float),
            np.array([], dtype=float),
            np.array([], dtype=float),
        )

    units = np.array(
        [customer["units"] for customer in st.session_state.customers],
        dtype=float,
    )

    bills = np.array(
        [customer["total_bill"] for customer in st.session_state.customers],
        dtype=float,
    )

    energy = np.array(
        [customer["energy_charge"] for customer in st.session_state.customers],
        dtype=float,
    )

    return units, bills, energy


def get_statistics():
    units, bills, energy = get_arrays()

    if len(units) == 0:
        return None

    return {
        "customers": len(units),
        "total_units": float(np.sum(units)),
        "average_units": float(np.mean(units)),
        "median_units": float(np.median(units)),
        "std_units": float(np.std(units)),
        "minimum_units": float(np.min(units)),
        "maximum_units": float(np.max(units)),
        "total_energy": float(np.sum(energy)),
        "average_energy": float(np.mean(energy)),
        "total_revenue": float(np.sum(bills)),
        "average_bill": float(np.mean(bills)),
        "median_bill": float(np.median(bills)),
        "std_bill": float(np.std(bills)),
        "minimum_bill": float(np.min(bills)),
        "maximum_bill": float(np.max(bills)),
    }


def consumption_category(units):
    if units == 0:
        return "No Consumption"
    if units <= 100:
        return "Low"
    if units <= 300:
        return "Moderate"
    if units <= 500:
        return "High"
    return "Very High"


def bill_category(amount):
    if amount <= 1500:
        return "Low"
    if amount <= 4000:
        return "Moderate"
    if amount <= 8000:
        return "High"
    return "Very High"


def find_customer(customer_id):
    for customer in st.session_state.customers:
        if customer["id"] == customer_id:
            return customer
    return None


# ============================================================
# RECEIPT TEXT
# ============================================================
def create_receipt(customer):
    lines = [
        "=" * 58,
        "          RESIDENTIAL ELECTRICITY BILL",
        "=" * 58,
        f"Customer ID       : {customer['id']}",
        f"Customer Name     : {customer['customer_name']}",
        f"Meter Number      : {customer['meter']}",
        f"Phone Number      : {customer['phone']}",
        f"Address           : {customer['address']}",
        f"Bill Date         : {customer['date']}",
        "-" * 58,
        f"Previous Reading  : {customer['previous']:.2f}",
        f"Current Reading   : {customer['current']:.2f}",
        f"Units Consumed    : {customer['units']:.2f}",
        "-" * 58,
        f"First 100 Units   : Rs. {customer['slab_charges'][0]:,.2f}",
        f"Next 200 Units    : Rs. {customer['slab_charges'][1]:,.2f}",
        f"Above 300 Units   : Rs. {customer['slab_charges'][2]:,.2f}",
        "-" * 58,
        f"Energy Charge     : Rs. {customer['energy_charge']:,.2f}",
        f"Fixed Surcharge   : Rs. {customer['surcharge']:,.2f}",
        f"TOTAL BILL        : Rs. {customer['total_bill']:,.2f}",
        "-" * 58,
        f"Consumption Level : {customer['consumption_category']}",
        f"Bill Category     : {customer['bill_category']}",
        "=" * 58,
        "Thank you for using the electricity management system.",
        "=" * 58,
    ]

    return "\n".join(lines)


# ============================================================
# JSON EXPORT
# ============================================================
def create_json_export():
    return json.dumps(
        st.session_state.customers,
        indent=4,
        default=lambda value: (
            value.tolist()
            if isinstance(value, np.ndarray)
            else str(value)
        ),
    )


# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.title("⚡ Electricity System")
    st.caption("Python + NumPy + Streamlit")

    st.divider()

    st.subheader("📌 Navigation")

    page = st.radio(
        "Choose Module",
        [
            "🏠 Dashboard",
            "➕ Generate Bill",
            "👥 Customer Records",
            "🔎 Search Customer",
            "📊 Analytics",
            "💰 Tariff",
            "ℹ️ About Project",
        ],
    )

    st.divider()

    st.subheader("💰 Current Tariff")
    st.write(f"0–100 units: Rs. {TIER_1_RATE:.2f}/unit")
    st.write(f"101–300 units: Rs. {TIER_2_RATE:.2f}/unit")
    st.write(f"Above 300 units: Rs. {TIER_3_RATE:.2f}/unit")
    st.write(f"Surcharge: Rs. {FIXED_SURCHARGE:.2f}")

    st.divider()

    st.metric(
        "Registered Customers",
        len(st.session_state.customers),
    )


# ============================================================
# HEADER
# ============================================================
st.markdown(
    f'<div class="main-title">⚡ {APP_TITLE}</div>',
    unsafe_allow_html=True,
)

st.markdown(
    f'<div class="sub-title">'
    f'{STUDENT_NAME} • Data Analysis Batch {BATCH} • '
    f'NumPy Analytics Dashboard'
    f'</div>',
    unsafe_allow_html=True,
)


# ============================================================
# DASHBOARD
# ============================================================
if page == "🏠 Dashboard":

    st.markdown(
        '<div class="section-title">📊 Executive Dashboard</div>',
        unsafe_allow_html=True,
    )

    stats = get_statistics()

    if stats is None:
        st.info(
            "No customer records are available yet. "
            "Go to **Generate Bill** to create the first bill."
        )

        st.subheader("✨ System Features")

        feature_columns = st.columns(4)

        features = [
            ("⚡", "Smart Billing", "Automatic slab-based calculation"),
            ("🧮", "NumPy Engine", "Fast numerical calculations"),
            ("📊", "Analytics", "Mean, median and standard deviation"),
            ("🔎", "Search", "Find customers quickly"),
        ]

        for column, (icon, title, description) in zip(
            feature_columns,
            features,
        ):
            with column:
                st.markdown(f"### {icon} {title}")
                st.write(description)

    else:
        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "👥 Customers",
            f"{stats['customers']:,}",
        )

        c2.metric(
            "⚡ Total Units",
            f"{stats['total_units']:,.2f}",
        )

        c3.metric(
            "💰 Total Revenue",
            f"Rs. {stats['total_revenue']:,.2f}",
        )

        c4.metric(
            "🧾 Average Bill",
            f"Rs. {stats['average_bill']:,.2f}",
        )

        st.divider()

        left, right = st.columns(2)

        names = [
            customer["customer_name"][:20]
            for customer in st.session_state.customers
        ]

        units = [
            customer["units"]
            for customer in st.session_state.customers
        ]

        bills = [
            customer["total_bill"]
            for customer in st.session_state.customers
        ]

        with left:
            st.subheader("⚡ Consumption by Customer")
            st.bar_chart(
                dict(zip(names, units)),
                use_container_width=True,
            )

        with right:
            st.subheader("💰 Bill Amount by Customer")
            st.bar_chart(
                dict(zip(names, bills)),
                use_container_width=True,
            )

        st.divider()

        st.subheader("📋 Recent Customer Records")

        recent = st.session_state.customers[-10:][::-1]

        table = []

        for customer in recent:
            table.append(
                {
                    "ID": customer["id"],
                    "Customer": customer["customer_name"],
                    "Meter": customer["meter"],
                    "Units": round(customer["units"], 2),
                    "Energy": round(customer["energy_charge"], 2),
                    "Total": round(customer["total_bill"], 2),
                    "Level": customer["consumption_category"],
                }
            )

        st.dataframe(
            table,
            use_container_width=True,
            hide_index=True,
        )


# ============================================================
# GENERATE BILL
# ============================================================
elif page == "➕ Generate Bill":

    st.subheader("➕ Generate Residential Electricity Bill")

    with st.form("electricity_bill_form", clear_on_submit=False):

        left, right = st.columns(2)

        with left:
            customer_name = st.text_input(
                "Customer Name *",
                placeholder="Enter full name",
            )

            meter_number = st.text_input(
                "Meter Number *",
                placeholder="e.g. MTR-1001",
            )

            phone_number = st.text_input(
                "Phone Number *",
                placeholder="Digits only",
            )

            address = st.text_area(
                "Customer Address *",
                placeholder="Enter residential address",
            )

        with right:
            previous_reading = st.number_input(
                "Previous Meter Reading",
                min_value=0.0,
                value=0.0,
                step=1.0,
            )

            current_reading = st.number_input(
                "Current Meter Reading",
                min_value=0.0,
                value=0.0,
                step=1.0,
            )

            billing_days = st.number_input(
                "Billing Period (Days)",
                min_value=1,
                max_value=366,
                value=30,
            )

            st.info(
                "Current reading must be greater than or equal "
                "to the previous reading."
            )

        submitted = st.form_submit_button(
            "⚡ GENERATE ELECTRICITY BILL",
            use_container_width=True,
        )

    if submitted:

        errors = []

        if not valid_text(customer_name):
            errors.append("Customer name cannot be empty.")

        if not valid_meter(meter_number):
            errors.append("Meter number cannot be empty.")

        if not valid_phone(phone_number):
            errors.append(
                "Phone number must contain 10–15 digits only."
            )

        if not valid_text(address):
            errors.append("Address cannot be empty.")

        if not valid_reading(previous_reading):
            errors.append("Previous reading is invalid.")

        if not valid_reading(current_reading):
            errors.append("Current reading is invalid.")

        if current_reading < previous_reading:
            errors.append(
                "Current reading cannot be less than previous reading."
            )

        if errors:
            for error in errors:
                st.error(f"❌ {error}")

        else:
            units_consumed = (
                current_reading - previous_reading
            )

            calculation = calculate_bill(units_consumed)

            customer = {
                "id": st.session_state.next_customer_id,
                "customer_name": customer_name.strip(),
                "meter": meter_number.strip().upper(),
                "phone": phone_number.strip(),
                "address": address.strip(),
                "previous": float(previous_reading),
                "current": float(current_reading),
                "units": float(units_consumed),
                "billing_days": int(billing_days),
                "energy_charge": calculation["energy_charge"],
                "surcharge": calculation["surcharge"],
                "total_bill": calculation["total_bill"],
                "average_energy_cost": calculation[
                    "average_energy_cost"
                ],
                "slab_units": calculation["slab_units"],
                "rates": calculation["rates"],
                "slab_charges": calculation["slab_charges"],
                "consumption_category": consumption_category(
                    units_consumed
                ),
                "bill_category": bill_category(
                    calculation["total_bill"]
                ),
                "date": datetime.now().strftime(
                    "%d-%m-%Y %I:%M %p"
                ),
            }

            st.session_state.customers.append(customer)
            st.session_state.next_customer_id += 1

            st.success(
                f"✅ Bill generated successfully for "
                f"{customer['customer_name']}!"
            )

            st.markdown(
                f'<div class="bill-total">'
                f'TOTAL BILL<br>'
                f'Rs. {customer["total_bill"]:,.2f}'
                f'</div>',
                unsafe_allow_html=True,
            )

            st.write("")

            c1, c2, c3, c4 = st.columns(4)

            c1.metric(
                "⚡ Units",
                f"{customer['units']:,.2f}",
            )

            c2.metric(
                "💰 Energy Charge",
                f"Rs. {customer['energy_charge']:,.2f}",
            )

            c3.metric(
                "🏷️ Surcharge",
                f"Rs. {customer['surcharge']:,.2f}",
            )

            c4.metric(
                "📌 Cost / Unit",
                f"Rs. {customer['average_energy_cost']:.2f}",
            )

            st.subheader("📋 Tariff Slab Breakdown")

            slab_table = {
                "Slab": [
                    "First 100 Units",
                    "Next 200 Units",
                    "Above 300 Units",
                ],
                "Units Used": [
                    round(float(customer["slab_units"][0]), 2),
                    round(float(customer["slab_units"][1]), 2),
                    round(float(customer["slab_units"][2]), 2),
                ],
                "Rate": [
                    f"Rs. {TIER_1_RATE:.2f}",
                    f"Rs. {TIER_2_RATE:.2f}",
                    f"Rs. {TIER_3_RATE:.2f}",
                ],
                "Charge": [
                    f"Rs. {customer['slab_charges'][0]:,.2f}",
                    f"Rs. {customer['slab_charges'][1]:,.2f}",
                    f"Rs. {customer['slab_charges'][2]:,.2f}",
                ],
            }

            st.table(slab_table)

            st.info(
                f"Consumption Level: **"
                f"{customer['consumption_category']}**  |  "
                f"Bill Category: **"
                f"{customer['bill_category']}**"
            )

            st.download_button(
                "📥 Download This Bill as TXT",
                data=create_receipt(customer),
                file_name=f"electricity_bill_{customer['id']}.txt",
                mime="text/plain",
                use_container_width=True,
            )


# ============================================================
# CUSTOMER RECORDS
# ============================================================
elif page == "👥 Customer Records":

    st.subheader("👥 Customer Records")

    if not st.session_state.customers:

        st.info("No customer records available.")

    else:

        search_text = st.text_input(
            "🔎 Filter records by customer name or meter"
        ).strip().lower()

        records = st.session_state.customers

        if search_text:
            records = [
                customer
                for customer in records
                if search_text in customer["customer_name"].lower()
                or search_text in customer["meter"].lower()
            ]

        rows = []

        for customer in records:
            rows.append(
                {
                    "ID": customer["id"],
                    "Customer": customer["customer_name"],
                    "Meter": customer["meter"],
                    "Phone": customer["phone"],
                    "Units": round(customer["units"], 2),
                    "Energy": round(customer["energy_charge"], 2),
                    "Total Bill": round(customer["total_bill"], 2),
                    "Level": customer["consumption_category"],
                }
            )

        st.dataframe(
            rows,
            use_container_width=True,
            hide_index=True,
        )

        st.divider()

        st.subheader("🗑️ Record Management")

        customer_ids = [
            customer["id"]
            for customer in st.session_state.customers
        ]

        selected_id = st.selectbox(
            "Select Customer ID",
            customer_ids,
        )

        selected_customer = find_customer(selected_id)

        if selected_customer:
            st.write(
                f"Selected: **"
                f"{selected_customer['customer_name']}**"
            )

        confirm_delete = st.checkbox(
            "I confirm that I want to delete this record."
        )

        if st.button(
            "🗑️ Delete Selected Customer",
            disabled=not confirm_delete,
            use_container_width=True,
        ):
            st.session_state.customers = [
                customer
                for customer in st.session_state.customers
                if customer["id"] != selected_id
            ]

            st.success("Customer record deleted successfully.")
            st.rerun()

        st.divider()

        st.subheader("💾 Export All Records")

        st.download_button(
            "📥 Download Customer Data as JSON",
            data=create_json_export(),
            file_name="electricity_customer_records.json",
            mime="application/json",
            use_container_width=True,
        )


# ============================================================
# SEARCH CUSTOMER
# ============================================================
elif page == "🔎 Search Customer":

    st.subheader("🔎 Search Customer")

    query = st.text_input(
        "Enter Customer ID or Meter Number",
        placeholder="Example: 1001 or MTR-1001",
    ).strip().upper()

    if query:

        found = None

        for customer in st.session_state.customers:

            if (
                str(customer["id"]) == query
                or customer["meter"] == query
            ):
                found = customer
                break

        if found:

            st.success(
                f"✅ Customer Found: "
                f"{found['customer_name']}"
            )

            c1, c2, c3, c4 = st.columns(4)

            c1.metric(
                "Customer ID",
                found["id"],
            )

            c2.metric(
                "Units",
                f"{found['units']:,.2f}",
            )

            c3.metric(
                "Energy Charge",
                f"Rs. {found['energy_charge']:,.2f}",
            )

            c4.metric(
                "Total Bill",
                f"Rs. {found['total_bill']:,.2f}",
            )

            st.divider()

            left, right = st.columns(2)

            with left:
                st.write(f"**Customer:** {found['customer_name']}")
                st.write(f"**Meter:** {found['meter']}")
                st.write(f"**Phone:** {found['phone']}")
                st.write(f"**Address:** {found['address']}")
                st.write(f"**Bill Date:** {found['date']}")

            with right:
                st.write(
                    f"**Previous Reading:** "
                    f"{found['previous']:.2f}"
                )
                st.write(
                    f"**Current Reading:** "
                    f"{found['current']:.2f}"
                )
                st.write(
                    f"**Consumption Level:** "
                    f"{found['consumption_category']}"
                )
                st.write(
                    f"**Bill Category:** "
                    f"{found['bill_category']}"
                )

            st.download_button(
                "📥 Download Customer Bill",
                data=create_receipt(found),
                file_name=f"bill_{found['id']}.txt",
                mime="text/plain",
                use_container_width=True,
            )

        else:

            st.warning(
                "No customer found with that ID or meter number."
            )


# ============================================================
# ANALYTICS
# ============================================================
elif page == "📊 Analytics":

    st.subheader("📊 NumPy Data Analysis")

    stats = get_statistics()

    if stats is None:

        st.info(
            "Add customer records first to activate analytics."
        )

    else:

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Mean Units",
            f"{stats['average_units']:,.2f}",
        )

        c2.metric(
            "Median Units",
            f"{stats['median_units']:,.2f}",
        )

        c3.metric(
            "Mean Bill",
            f"Rs. {stats['average_bill']:,.2f}",
        )

        c4.metric(
            "Median Bill",
            f"Rs. {stats['median_bill']:,.2f}",
        )

        st.divider()

        st.subheader("📐 Statistical Summary")

        analysis_table = {
            "Metric": [
                "Total Customers",
                "Total Units",
                "Average Units",
                "Median Units",
                "Minimum Units",
                "Maximum Units",
                "Units Standard Deviation",
                "Total Energy Charges",
                "Average Energy Charge",
                "Total Revenue",
                "Average Bill",
                "Median Bill",
                "Minimum Bill",
                "Maximum Bill",
                "Bill Standard Deviation",
            ],
            "Result": [
                f"{stats['customers']:,}",
                f"{stats['total_units']:,.2f}",
                f"{stats['average_units']:,.2f}",
                f"{stats['median_units']:,.2f}",
                f"{stats['minimum_units']:,.2f}",
                f"{stats['maximum_units']:,.2f}",
                f"{stats['std_units']:,.2f}",
                f"Rs. {stats['total_energy']:,.2f}",
                f"Rs. {stats['average_energy']:,.2f}",
                f"Rs. {stats['total_revenue']:,.2f}",
                f"Rs. {stats['average_bill']:,.2f}",
                f"Rs. {stats['median_bill']:,.2f}",
                f"Rs. {stats['minimum_bill']:,.2f}",
                f"Rs. {stats['maximum_bill']:,.2f}",
                f"Rs. {stats['std_bill']:,.2f}",
            ],
        }

        st.table(analysis_table)

        units, bills, energy = get_arrays()

        st.divider()

        left, right = st.columns(2)

        names = [
            customer["customer_name"][:18]
            for customer in st.session_state.customers
        ]

        with left:

            st.subheader("⚡ Customer Consumption")

            st.bar_chart(
                dict(zip(names, units)),
                use_container_width=True,
            )

        with right:

            st.subheader("💰 Customer Bills")

            st.bar_chart(
                dict(zip(names, bills)),
                use_container_width=True,
            )

        st.divider()

        highest_bill_index = int(np.argmax(bills))
        lowest_bill_index = int(np.argmin(bills))
        highest_usage_index = int(np.argmax(units))

        high_customer = st.session_state.customers[
            highest_bill_index
        ]

        low_customer = st.session_state.customers[
            lowest_bill_index
        ]

        usage_customer = st.session_state.customers[
            highest_usage_index
        ]

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "🔝 Highest Bill",
            f"Rs. {bills[highest_bill_index]:,.2f}",
            high_customer["customer_name"],
        )

        c2.metric(
            "🔻 Lowest Bill",
            f"Rs. {bills[lowest_bill_index]:,.2f}",
            low_customer["customer_name"],
        )

        c3.metric(
            "⚡ Highest Consumption",
            f"{units[highest_usage_index]:,.2f} units",
            usage_customer["customer_name"],
        )

        st.divider()

        st.subheader("📊 Consumption Distribution")

        histogram, bin_edges = np.histogram(
            units,
            bins=min(10, max(1, len(units))),
        )

        distribution = []

        for index, count in enumerate(histogram):
            distribution.append(
                {
                    "Range": (
                        f"{bin_edges[index]:.0f} – "
                        f"{bin_edges[index + 1]:.0f}"
                    ),
                    "Customers": int(count),
                }
            )

        st.table(distribution)


# ============================================================
# TARIFF
# ============================================================
elif page == "💰 Tariff":

    st.subheader("💰 Electricity Tariff Structure")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "First 100 Units",
        f"Rs. {TIER_1_RATE:.2f}",
    )

    c2.metric(
        "Next 200 Units",
        f"Rs. {TIER_2_RATE:.2f}",
    )

    c3.metric(
        "Above 300 Units",
        f"Rs. {TIER_3_RATE:.2f}",
    )

    c4.metric(
        "Fixed Surcharge",
        f"Rs. {FIXED_SURCHARGE:.2f}",
    )

    st.divider()

    st.table(
        {
            "Tariff Slab": [
                "First 100 units",
                "101–300 units",
                "Above 300 units",
                "Fixed surcharge",
            ],
            "Rate": [
                f"Rs. {TIER_1_RATE:.2f}/unit",
                f"Rs. {TIER_2_RATE:.2f}/unit",
                f"Rs. {TIER_3_RATE:.2f}/unit",
                f"Rs. {FIXED_SURCHARGE:.2f}",
            ],
            "Calculation": [
                "Units × Rs. 10",
                "Units × Rs. 15",
                "Units × Rs. 20",
                "Fixed amount",
            ],
        }
    )

    st.info(
        "The bill is calculated progressively: "
        "each usage slab is charged at its own rate."
    )


# ============================================================
# ABOUT
# ============================================================
elif page == "ℹ️ About Project":

    st.subheader("ℹ️ About This Project")

    st.markdown(
        f"""
        ### ⚡ {APP_TITLE}

        **Student:** {STUDENT_NAME}

        **Data Analysis Batch:** {BATCH}

        **Programming Language:** Python

        **Libraries Used:**
        - NumPy
        - Streamlit

        ### 🎯 Project Objectives

        1. Collect residential customer information.
        2. Validate meter readings and customer data.
        3. Calculate electricity consumption.
        4. Apply progressive electricity tariff slabs.
        5. Calculate the final bill automatically.
        6. Store multiple customer records during the session.
        7. Analyze customer consumption using NumPy.
        8. Calculate statistical measures.
        9. Display an interactive Streamlit dashboard.
        10. Export individual bills and customer records.

        ### 🧮 NumPy Concepts Used

        - `np.array()`
        - `np.sum()`
        - `np.mean()`
        - `np.median()`
        - `np.std()`
        - `np.min()`
        - `np.max()`
        - `np.argmax()`
        - `np.argmin()`
        - `np.histogram()`

        ### 📚 Data Analysis Concepts

        The project demonstrates data collection, validation,
        numerical processing, descriptive statistics,
        visualization, and reporting.

        ### ⚠️ Important

        This application stores records in Streamlit session state.
        Restarting the Streamlit application clears the in-memory
        records unless they are exported.
        """
    )


# ============================================================
# FOOTER
# ============================================================
st.divider()

st.caption(
    f"⚡ {APP_TITLE} | "
    f"{STUDENT_NAME} | "
    f"Batch {BATCH} | "
    f"Python + NumPy + Streamlit"
)
"""
Employee Salary Prediction System
Student: Muhammad Bilal Khan
Problem: Regression
Algorithm: Linear Regression
Libraries: NumPy, Scikit-learn, Streamlit
"""

import io
from datetime import datetime
import numpy as np
import streamlit as st
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

st.set_page_config(
    page_title="Employee Salary Prediction",
    page_icon="💼",
    layout="wide",
)

# -------------------- DATA --------------------
EXPERIENCE = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype=float)
SALARY = np.array(
    [32000, 36000, 41000, 45000, 50000,
     55000, 61000, 67000, 73000, 80000],
    dtype=float,
)

# -------------------- MODEL --------------------
X = EXPERIENCE.reshape(-1, 1)
y = SALARY

model = LinearRegression()
model.fit(X, y)

slope = float(model.coef_[0])
intercept = float(model.intercept_)
fitted = model.predict(X)

mae_all = mean_absolute_error(y, fitted)
rmse_all = np.sqrt(mean_squared_error(y, fitted))
r2_all = r2_score(y, fitted)

# Reproducible evaluation split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.30, random_state=42
)
test_model = LinearRegression()
test_model.fit(X_train, y_train)
test_predictions = test_model.predict(X_test)

test_mae = mean_absolute_error(y_test, test_predictions)
test_rmse = np.sqrt(mean_squared_error(y_test, test_predictions))
test_r2 = r2_score(y_test, test_predictions)

# -------------------- SESSION STATE --------------------
if "history" not in st.session_state:
    st.session_state.history = []

# -------------------- HELPERS --------------------
def money(value):
    return f"Rs. {float(value):,.0f}"

def predict_salary(experience):
    prediction = model.predict(np.array([[float(experience)]]))[0]
    return max(float(prediction), 0.0)

def report(experience, prediction):
    return f"""EMPLOYEE SALARY PREDICTION REPORT
========================================
Student: Muhammad Bilal
Batch: 317
Generated: {datetime.now().strftime("%d-%m-%Y %I:%M %p")}

Experience: {experience:.1f} years
Estimated Salary: {money(prediction)}

Algorithm: Linear Regression
Training Records: {len(X)}

Slope: {slope:,.2f}
Intercept: {intercept:,.2f}
R²: {r2_all:.4f}
MAE: {money(mae_all)}
RMSE: {money(rmse_all)}

NOTE:
This is an estimated salary based only on historical
experience/salary data. It is not a guaranteed salary.
Real compensation can depend on role, skills, education,
location, performance, and company policy.
"""

# -------------------- STYLE --------------------
st.markdown("""
<style>
.main-title{text-align:center;font-size:42px;font-weight:800}
.subtitle{text-align:center;opacity:.7;font-size:17px;margin-bottom:25px}
.prediction{border:2px solid #8885;border-radius:18px;padding:25px;text-align:center}
.prediction-value{font-size:42px;font-weight:850}
</style>
""", unsafe_allow_html=True)

# -------------------- SIDEBAR --------------------
with st.sidebar:
    st.title("💼 Salary AI")
    st.caption("Linear Regression HR Analytics")
    page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "🔮 Salary Predictor",
            "📊 Dataset",
            "📈 Model Analysis",
            "🧮 Manual Calculation",
            "📝 Prediction History",
            "ℹ️ About",
        ],
    )
    st.divider()
    st.write("**Algorithm:** Linear Regression")
    st.write(f"**Training records:** {len(X)}")
    st.write(f"**Slope:** {money(slope)} / year")

# -------------------- HEADER --------------------
st.markdown(
    '<div class="main-title">💼 Employee Salary Prediction System</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="subtitle">Muhammad Bilal • Data Analysis Batch 317 • '
    'Regression using Linear Regression</div>',
    unsafe_allow_html=True,
)

# ==================== DASHBOARD ====================
if page == "🏠 Dashboard":
    st.subheader("📊 HR Analytics Dashboard")

    a, b, c, d = st.columns(4)
    a.metric("👥 Employees", len(X))
    b.metric("💰 Average Salary", money(np.mean(y)))
    c.metric("📈 R² Score", f"{r2_all:.4f}")
    d.metric("📐 Salary / Year", money(slope))

    st.divider()

    left, right = st.columns(2)
    with left:
        st.subheader("📈 Actual vs Model Salary")
        st.line_chart(
            {"Actual Salary": y, "Model Salary": fitted},
            use_container_width=True,
        )

    with right:
        st.subheader("📊 Salary by Experience")
        st.bar_chart(
            {f"{int(e)} Years": s for e, s in zip(EXPERIENCE, SALARY)},
            use_container_width=True,
        )

    st.divider()
    st.info(
        "The model estimates salary from years of experience. "
        "It does not guarantee an exact salary."
    )

# ==================== PREDICTOR ====================
elif page == "🔮 Salary Predictor":
    st.subheader("🔮 Predict Employee Salary")

    experience = st.number_input(
        "Years of Experience",
        min_value=0.0,
        max_value=50.0,
        value=3.0,
        step=0.5,
    )

    if st.button("🚀 PREDICT SALARY", use_container_width=True):
        prediction = predict_salary(experience)

        st.session_state.history.append({
            "Date & Time": datetime.now().strftime("%d-%m-%Y %I:%M %p"),
            "Experience": experience,
            "Estimated Salary": prediction,
        })

        st.markdown(
            f'<div class="prediction"><h3>💰 Estimated Salary</h3>'
            f'<div class="prediction-value">{money(prediction)}</div>'
            f'<p>For {experience:.1f} years of experience</p></div>',
            unsafe_allow_html=True,
        )

        c1, c2, c3 = st.columns(3)
        c1.metric("Experience", f"{experience:.1f} years")
        c2.metric("Estimated Salary", money(prediction))
        c3.metric("Increase / Year", money(slope))

        st.subheader("🧮 Model Explanation")
        st.latex(r"\hat{y} = b_0 + b_1x")
        st.write(
            f"The learned slope is {money(slope)} per additional "
            f"year of experience."
        )

        st.download_button(
            "📥 Download Prediction Report",
            report(experience, prediction),
            file_name="salary_prediction_report.txt",
            mime="text/plain",
            use_container_width=True,
        )

# ==================== DATASET ====================
elif page == "📊 Dataset":
    st.subheader("📊 Historical Employee Dataset")

    st.dataframe(
        {
            "Employee ID": [f"E{i:03d}" for i in range(1, 11)],
            "Experience": EXPERIENCE,
            "Actual Salary": SALARY,
            "Model Salary": np.round(fitted, 2),
            "Residual": np.round(y - fitted, 2),
        },
        use_container_width=True,
        hide_index=True,
    )

    st.divider()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Minimum Salary", money(np.min(y)))
    c2.metric("Maximum Salary", money(np.max(y)))
    c3.metric("Mean Salary", money(np.mean(y)))
    c4.metric("Median Salary", money(np.median(y)))

    st.subheader("🧮 NumPy Statistics")
    st.table({
        "Statistic": [
            "Mean Experience", "Median Experience",
            "Experience Std Dev", "Minimum Experience",
            "Maximum Experience", "Salary Std Dev",
        ],
        "Value": [
            f"{np.mean(EXPERIENCE):.2f} years",
            f"{np.median(EXPERIENCE):.2f} years",
            f"{np.std(EXPERIENCE):.2f} years",
            f"{np.min(EXPERIENCE):.2f} years",
            f"{np.max(EXPERIENCE):.2f} years",
            money(np.std(SALARY)),
        ],
    })

# ==================== MODEL ANALYSIS ====================
elif page == "📈 Model Analysis":
    st.subheader("📈 Linear Regression Model Analysis")

    st.latex(r"\hat{y} = b_0 + b_1x")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Slope", money(slope))
    c2.metric("Intercept", money(intercept))
    c3.metric("R²", f"{r2_all:.4f}")
    c4.metric("RMSE", money(rmse_all))

    st.write(
        f"Learned equation: **Salary = {intercept:,.2f} + "
        f"({slope:,.2f} × Experience)**"
    )

    st.divider()
    st.subheader("🎯 Train/Test Evaluation")

    st.table({
        "Metric": ["MAE", "MSE", "RMSE", "R²"],
        "Test Set": [
            money(test_mae),
            f"{mean_squared_error(y_test, test_predictions):,.2f}",
            money(test_rmse),
            f"{test_r2:.4f}",
        ],
    })

    st.subheader("🔬 Test Predictions")
    st.dataframe(
        {
            "Experience": X_test.flatten(),
            "Actual Salary": y_test,
            "Predicted Salary": np.round(test_predictions, 2),
            "Absolute Error": np.round(
                np.abs(y_test - test_predictions), 2
            ),
        },
        use_container_width=True,
        hide_index=True,
    )

    st.warning(
        "Only 10 sample employees are available, so evaluation "
        "metrics can vary considerably. A real HR system needs "
        "a much larger and more representative dataset."
    )

# ==================== MANUAL CALCULATION ====================
elif page == "🧮 Manual Calculation":
    st.subheader("🧮 Manual Linear Regression Calculation")

    experience = st.slider(
        "Years of Experience",
        0.0, 20.0, 5.0, 0.5
    )

    prediction = predict_salary(experience)

    st.metric("Estimated Salary", money(prediction))

    st.write(f"Intercept (b₀): **{intercept:,.2f}**")
    st.write(f"Slope (b₁): **{slope:,.2f}**")

    st.latex(
        rf"Salary = {intercept:,.2f} + "
        rf"({slope:,.2f} 	imes {experience:.1f})"
    )

    st.success(
        f"Estimated salary = {money(prediction)}"
    )

# ==================== HISTORY ====================
elif page == "📝 Prediction History":
    st.subheader("📝 Prediction History")

    if not st.session_state.history:
        st.info("No predictions have been generated yet.")
    else:
        st.dataframe(
            st.session_state.history,
            use_container_width=True,
            hide_index=True,
        )

        values = np.array(
            [r["Estimated Salary"] for r in st.session_state.history],
            dtype=float,
        )

        c1, c2, c3 = st.columns(3)
        c1.metric("Predictions", len(values))
        c2.metric("Average Prediction", money(np.mean(values)))
        c3.metric("Highest Prediction", money(np.max(values)))

        st.line_chart(
            {"Estimated Salary": values},
            use_container_width=True,
        )

        output = io.StringIO()
        output.write("Date & Time,Experience,Estimated Salary\n")
        for row in st.session_state.history:
            output.write(
                f"{row['Date & Time']},{row['Experience']},"
                f"{row['Estimated Salary']:.2f}\n"
            )

        st.download_button(
            "📥 Download History CSV",
            output.getvalue(),
            file_name="salary_prediction_history.csv",
            mime="text/csv",
            use_container_width=True,
        )

        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.history = []
            st.rerun()

# ==================== ABOUT ====================
elif page == "ℹ️ About":
    st.subheader("ℹ️ About This Project")

    st.markdown(
        """
        ### 🎯 Objective
        Build a salary estimation system for an HR department
        using historical experience and salary data.

        ### 🧠 Why Regression?
        Salary is a numerical target. Therefore, this is a
        **regression problem**, not a classification problem.

        ### 🤖 Algorithm
        **Linear Regression** learns a straight-line relationship
        between Years of Experience and Salary.

        ### 🧮 NumPy
        Used for arrays, statistics, numerical calculations,
        prediction preparation, errors, and RMSE.

        ### 🖥️ Streamlit
        Used for the interactive dashboard, input controls,
        charts, metrics, and downloadable reports.

        ### ⚠️ Limitation
        The assignment uses only 10 historical employees and one
        feature. A production HR model should consider role,
        skills, education, location, performance, seniority,
        department, and market salary information.
        """
    )

st.divider()
st.caption(
    "💼 Employee Salary Prediction System | Muhammad Bilal | "
    "Batch 317 | Python + NumPy + Scikit-learn + Streamlit"
)
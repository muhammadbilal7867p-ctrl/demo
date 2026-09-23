
# students according to their CGPA and Entrance Test Score.
#
# Classification Classes:
#
#       0 -> Not Eligible
#       1 -> Partial Scholarship (50%)
#       2 -> Full Scholarship (100%)
#
# Machine Learning Algorithm:
#       Logistic Regression
#
# Libraries:
#       NumPy
#       Pandas
#       Scikit-learn
#       Matplotlib
#       Streamlit
#
# =====================================================================


# =====================================================================
# 1. IMPORT LIBRARIES
# =====================================================================

import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)


# =====================================================================
# 2. STREAMLIT PAGE CONFIGURATION
# =====================================================================

st.set_page_config(
    page_title="Student Scholarship AI System",
    page_icon="🎓",
    layout="wide"
)


# =====================================================================
# 3. PROJECT TITLE
# =====================================================================

st.title("🎓 Student Scholarship Eligibility System")

st.subheader(
    "AI-Based Scholarship Classification using Logistic Regression"
)

st.markdown(
    """
    ### 📌 Assignment Scenario

    A university receives more than 1000 scholarship applications
    every year. Manually checking every student's CGPA and entrance
    test score takes significant time.

    This system uses **Machine Learning** to classify students into
    three scholarship categories:

    - ❌ **Not Eligible**
    - 🟡 **Partial Scholarship (50%)**
    - 🟢 **Full Scholarship (100%)**

    The classification model used in this project is
    **Logistic Regression**.
    """
)


# =====================================================================
# 4. CONSTANTS
# =====================================================================

RANDOM_STATE = 42

NUMBER_OF_STUDENTS = 1200

SCHOLARSHIP_LABELS = {
    0: "Not Eligible",
    1: "Partial Scholarship (50%)",
    2: "Full Scholarship (100%)"
}


# =====================================================================
# 5. GENERATE STUDENT DATA
# =====================================================================

@st.cache_data
def generate_student_data(
    number_of_students=1200
):
    """
    Generate a synthetic dataset containing:

        CGPA
        Entrance Test Score
        Scholarship Category

    The dataset is generated for educational purposes.
    """

    np.random.seed(
        RANDOM_STATE
    )

    # ---------------------------------------------------------------
    # Generate CGPA
    # Range approximately 2.00 - 4.00
    # ---------------------------------------------------------------

    cgpa = np.random.uniform(
        2.00,
        4.00,
        number_of_students
    )

    # ---------------------------------------------------------------
    # Generate entrance test scores
    # Range approximately 40 - 100
    # ---------------------------------------------------------------

    entrance_score = np.random.uniform(
        40,
        100,
        number_of_students
    )

    # ---------------------------------------------------------------
    # Calculate a combined academic score.
    #
    # CGPA is converted to a 0-100 scale.
    # ---------------------------------------------------------------

    cgpa_percentage = (
        (cgpa - 2.00)
        / 2.00
    ) * 100

    combined_score = (
        0.55 * cgpa_percentage
        +
        0.45 * entrance_score
    )

    # ---------------------------------------------------------------
    # Add small random variation so the dataset is not perfectly
    # separated.
    # ---------------------------------------------------------------

    noise = np.random.normal(
        0,
        4,
        number_of_students
    )

    final_score = (
        combined_score
        + noise
    )

    # ---------------------------------------------------------------
    # Create scholarship classes.
    #
    # These thresholds are sample educational rules.
    # ---------------------------------------------------------------

    scholarship = np.where(
        final_score >= 75,
        2,
        np.where(
            final_score >= 55,
            1,
            0
        )
    )

    # ---------------------------------------------------------------
    # Create DataFrame
    # ---------------------------------------------------------------

    data = pd.DataFrame({
        "CGPA": np.round(
            cgpa,
            2
        ),

        "Entrance Test Score": np.round(
            entrance_score,
            2
        ),

        "Scholarship Class": scholarship
    })

    # ---------------------------------------------------------------
    # Add readable scholarship labels
    # ---------------------------------------------------------------

    data["Scholarship"] = (
        data["Scholarship Class"]
        .map(SCHOLARSHIP_LABELS)
    )

    return data


# =====================================================================
# 6. LOAD DATA
# =====================================================================

data = generate_student_data(
    NUMBER_OF_STUDENTS
)


# =====================================================================
# 7. SIDEBAR
# =====================================================================

st.sidebar.title(
    "🎛️ Navigation"
)

page = st.sidebar.radio(
    "Select Section",
    [
        "🏠 Dashboard",
        "📊 Dataset",
        "📈 Data Analysis",
        "🤖 Train Model",
        "🎓 Scholarship Prediction",
        "📋 Model Evaluation"
    ]
)


# =====================================================================
# 8. DASHBOARD
# =====================================================================

if page == "🏠 Dashboard":

    st.header(
        "🏠 Scholarship Analytics Dashboard"
    )

    st.markdown(
        """
        This dashboard demonstrates how a university can use
        a machine-learning classification model to process
        scholarship applications.
        """
    )

    # ---------------------------------------------------------------
    # KPI CARDS
    # ---------------------------------------------------------------

    total_students = len(
        data
    )

    not_eligible = np.sum(
        data["Scholarship Class"] == 0
    )

    partial = np.sum(
        data["Scholarship Class"] == 1
    )

    full = np.sum(
        data["Scholarship Class"] == 2
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Total Applications",
            total_students
        )

    with col2:

        st.metric(
            "❌ Not Eligible",
            not_eligible
        )

    with col3:

        st.metric(
            "🟡 Partial Scholarship",
            partial
        )

    with col4:

        st.metric(
            "🟢 Full Scholarship",
            full
        )

    st.divider()

    # ---------------------------------------------------------------
    # SCHOLARSHIP DISTRIBUTION
    # ---------------------------------------------------------------

    st.subheader(
        "📊 Scholarship Distribution"
    )

    distribution = (
        data["Scholarship"]
        .value_counts()
    )

    st.bar_chart(
        distribution
    )

    # ---------------------------------------------------------------
    # PROJECT WORKFLOW
    # ---------------------------------------------------------------

    st.subheader(
        "🔄 Machine Learning Workflow"
    )

    workflow = [
        "1️⃣ Generate / collect student data",
        "2️⃣ Clean and validate the data",
        "3️⃣ Select CGPA and Entrance Test Score",
        "4️⃣ Split data into training and testing sets",
        "5️⃣ Standardize numerical features",
        "6️⃣ Train Logistic Regression",
        "7️⃣ Evaluate model performance",
        "8️⃣ Predict scholarship category"
    ]

    for step in workflow:

        st.write(
            step
        )


# =====================================================================
# 9. DATASET PAGE
# =====================================================================

elif page == "📊 Dataset":

    st.header(
        "📊 Student Dataset"
    )

    st.write(
        f"Dataset contains **{len(data)} student applications**."
    )

    # ---------------------------------------------------------------
    # Show data
    # ---------------------------------------------------------------

    st.dataframe(
        data,
        use_container_width=True,
        hide_index=True
    )

    # ---------------------------------------------------------------
    # Dataset statistics
    # ---------------------------------------------------------------

    st.subheader(
        "📐 Dataset Statistics"
    )

    statistics = data[
        [
            "CGPA",
            "Entrance Test Score"
        ]
    ].describe()

    st.dataframe(
        statistics,
        use_container_width=True
    )

    # ---------------------------------------------------------------
    # Download data
    # ---------------------------------------------------------------

    csv_data = data.to_csv(
        index=False
    )

    st.download_button(
        label="📥 Download Student Dataset",
        data=csv_data,
        file_name="student_scholarship_dataset.csv",
        mime="text/csv"
    )


# =====================================================================
# 10. DATA ANALYSIS PAGE
# =====================================================================

elif page == "📈 Data Analysis":

    st.header(
        "📈 Student Data Analysis"
    )

    # ---------------------------------------------------------------
    # Average values
    # ---------------------------------------------------------------

    average_cgpa = np.mean(
        data["CGPA"]
    )

    average_test_score = np.mean(
        data["Entrance Test Score"]
    )

    maximum_cgpa = np.max(
        data["CGPA"]
    )

    minimum_cgpa = np.min(
        data["CGPA"]
    )

    maximum_score = np.max(
        data["Entrance Test Score"]
    )

    minimum_score = np.min(
        data["Entrance Test Score"]
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Average CGPA",
            f"{average_cgpa:.2f}"
        )

    with col2:

        st.metric(
            "Average Entrance Score",
            f"{average_test_score:.2f}"
        )

    with col3:

        st.metric(
            "Maximum CGPA",
            f"{maximum_cgpa:.2f}"
        )

    # ---------------------------------------------------------------
    # CGPA distribution
    # ---------------------------------------------------------------

    st.subheader(
        "📚 CGPA Distribution"
    )

    st.bar_chart(
        data["CGPA"].round(1)
        .value_counts()
        .sort_index()
    )

    # ---------------------------------------------------------------
    # Entrance score distribution
    # ---------------------------------------------------------------

    st.subheader(
        "📝 Entrance Test Score Distribution"
    )

    st.bar_chart(
        data["Entrance Test Score"]
        .round(-1)
        .value_counts()
        .sort_index()
    )

    # ---------------------------------------------------------------
    # Scholarship class comparison
    # ---------------------------------------------------------------

    st.subheader(
        "🎓 Scholarship Categories"
    )

    category_summary = (
        data.groupby(
            "Scholarship"
        )[
            [
                "CGPA",
                "Entrance Test Score"
            ]
        ]
        .mean()
        .round(2)
    )

    st.dataframe(
        category_summary,
        use_container_width=True
    )


# =====================================================================
# 11. PREPARE MACHINE LEARNING DATA
# =====================================================================

X = data[
    [
        "CGPA",
        "Entrance Test Score"
    ]
]

y = data[
    "Scholarship Class"
]


# =====================================================================
# 12. TRAIN / TEST SPLIT
# =====================================================================

X_train, X_test, y_train, y_test = train_test_split(
           X,
    y,
    test_size=0.20,
    random_state=RANDOM_STATE,
    stratify=y
)


# =====================================================================
# 13. FEATURE SCALING
# =====================================================================

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(
    X_train
)

X_test_scaled = scaler.transform(
    X_test
)


# =====================================================================
# 14. LOGISTIC REGRESSION MODEL
# =====================================================================

model = LogisticRegression(
    max_iter=1000,
    random_state=RANDOM_STATE
)

model.fit(
    X_train_scaled,
    y_train
)


# =====================================================================
# 15. MODEL PREDICTIONS
# =====================================================================

y_pred = model.predict(
    X_test_scaled
)


# =====================================================================
# 16. MODEL ACCURACY
# =====================================================================

accuracy = accuracy_score(
    y_test,
    y_pred
)


# =====================================================================
# 17. TRAIN MODEL PAGE
# =====================================================================

if page == "🤖 Train Model":

    st.header(
        "🤖 Logistic Regression Model"
    )

    st.write(
        "The model uses two input features:"
    )

    st.code(
        """
Features:
    1. CGPA
    2. Entrance Test Score

Target:
    Scholarship Class
        0 = Not Eligible
        1 = Partial Scholarship
        2 = Full Scholarship
        """
    )

    # ---------------------------------------------------------------
    # Dataset split
    # ---------------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Training Applications",
            len(X_train)
        )

    with col2:

        st.metric(
            "Testing Applications",
            len(X_test)
        )

    # ---------------------------------------------------------------
    # Accuracy
    # ---------------------------------------------------------------

    st.subheader(
        "🎯 Model Accuracy"
    )

    st.metric(
        "Logistic Regression Accuracy",
        f"{accuracy * 100:.2f}%"
    )

    # ---------------------------------------------------------------
    # Model coefficients
    # ---------------------------------------------------------------

    st.subheader(
        "📐 Model Coefficients"
    )

    coefficients = pd.DataFrame(
        model.coef_,
        columns=[
            "CGPA",
            "Entrance Test Score"
        ],
        index=[
            "Not Eligible",
            "Partial Scholarship",
            "Full Scholarship"
        ]
    )

    st.dataframe(
        coefficients,
        use_container_width=True
    )

    st.info(
        """
        Logistic Regression calculates probabilities for the
        scholarship classes and assigns the class with the
        highest predicted probability.
        """
    )


# =====================================================================
# 18. SCHOLARSHIP PREDICTION PAGE
# =====================================================================

elif page == "🎓 Scholarship Prediction":

    st.header(
        "🎓 Student Scholarship Prediction"
    )

    st.write(
        """
        Enter a student's academic information below.
        The trained Logistic Regression model will classify
        the student into one of the three scholarship categories.
        """
    )

    # ---------------------------------------------------------------
    # User Inputs
    # ---------------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        student_cgpa = st.number_input(
            "📚 Student CGPA",
            min_value=0.0,
            max_value=4.0,
            value=3.00,
            step=0.01
        )

    with col2:

        entrance_score = st.number_input(
            "📝 Entrance Test Score",
            min_value=0.0,
            max_value=100.0,
            value=70.0,
            step=1.0
        )

    # ---------------------------------------------------------------
    # Prediction button
    # ---------------------------------------------------------------

    if st.button(
        "🔮 Predict Scholarship",
        use_container_width=True
    ):

        student_data = np.array([
            [
                student_cgpa,
                entrance_score
            ]
        ])

        student_scaled = scaler.transform(
            student_data
        )

        prediction = model.predict(
            student_scaled
        )

        probabilities = model.predict_proba(
            student_scaled
        )

        predicted_class = int(
            prediction[0]
        )

        scholarship_name = (
            SCHOLARSHIP_LABELS[
                predicted_class
            ]
        )

        confidence = (
            np.max(
                probabilities
            ) * 100
        )

        # -----------------------------------------------------------
        # Display prediction
        # -----------------------------------------------------------

        st.divider()

        if predicted_class == 0:

            st.error(
                f"❌ Prediction: {scholarship_name}"
            )

        elif predicted_class == 1:

            st.warning(
                f"🟡 Prediction: {scholarship_name}"
            )

        else:

            st.success(
                f"🟢 Prediction: {scholarship_name}"
            )

        st.metric(
            "Model Confidence",
            f"{confidence:.2f}%"
        )

        # -----------------------------------------------------------
        # Probability table
        # -----------------------------------------------------------

        st.subheader(
            "📊 Class Probabilities"
        )

        probability_data = pd.DataFrame({
            "Scholarship Category": [
                "Not Eligible",
                "Partial Scholarship (50%)",
                "Full Scholarship (100%)"
            ],

            "Probability": (
                probabilities[0] * 100
            )
        })

        probability_data[
            "Probability"
        ] = probability_data[
            "Probability"
        ].round(2)

        st.dataframe(
            probability_data,
            use_container_width=True,
            hide_index=True
        )


# =====================================================================
# 19. MODEL EVALUATION PAGE
# =====================================================================

elif page == "📋 Model Evaluation":

    st.header(
        "📋 Model Evaluation"
    )

    # ---------------------------------------------------------------
    # Accuracy
    # ---------------------------------------------------------------

    st.metric(
        "Accuracy",
        f"{accuracy * 100:.2f}%"
    )

    # ---------------------------------------------------------------
    # Classification Report
    # ---------------------------------------------------------------

    st.subheader(
        "📊 Classification Report"
    )

    report = classification_report(
        y_test,
        y_pred,
        target_names=[
            "Not Eligible",
            "Partial Scholarship",
            "Full Scholarship"
        ],
        output_dict=True
    )

    report_df = pd.DataFrame(
        report
    ).transpose()

    st.dataframe(
        report_df.round(3),
        use_container_width=True
    )

    # ---------------------------------------------------------------
    # Confusion Matrix
    # ---------------------------------------------------------------

    st.subheader(
        "🔲 Confusion Matrix"
    )

    matrix = confusion_matrix(
        y_test,
        y_pred
    )

    fig, ax = plt.subplots(
        figsize=(7, 5)
    )

    image = ax.imshow(
        matrix
    )

    ax.set_title(
        "Scholarship Classification Confusion Matrix"
    )

    ax.set_xlabel(
        "Predicted Class"
    )

    ax.set_ylabel(
        "Actual Class"
    )

    ax.set_xticks(
        [0, 1, 2]
    )

    ax.set_yticks(
        [0, 1, 2]
    )

    ax.set_xticklabels([
        "Not Eligible",
        "Partial",
        "Full"
    ])

    ax.set_yticklabels([
        "Not Eligible",
        "Partial",
        "Full"
    ])

    # Add values to cells

    for i in range(
        matrix.shape[0]
    ):

        for j in range(
            matrix.shape[1]
        ):

            ax.text(
                j,
                i,
                matrix[i, j],
                ha="center",
                va="center"
            )

    fig.colorbar(
        image,
        ax=ax
    )

    plt.tight_layout()

    st.pyplot(
        fig
    )


# =====================================================================
# 20. FOOTER
# =====================================================================

st.divider()

st.caption(
    """
    🎓 Student Scholarship Eligibility System |
    Machine Learning Assignment |
    Logistic Regression Classification
    """
)

st.caption(
    """
    ⚠️ Educational project: predictions are based on synthetic
    demonstration data and should not be used as real scholarship
    decisions without validated institutional criteria and review.
    """
)
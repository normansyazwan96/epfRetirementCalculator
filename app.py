import streamlit as st


# ==========================================
# EPF Calculation
# ==========================================

def calculate_epf_balance(
    epf_balance,
    avg_dividend,
    age,
    retirement_age,
    salary,
    bonus,
    increment,
    employee_contribution,
    employer_contribution,
    monthly_withdrawal,
    annual_withdrawal
):

    # Convert percentages to decimals
    dividend_rate = avg_dividend / 100
    increment_rate = increment / 100
    employee_rate = employee_contribution / 100
    employer_rate = employer_contribution / 100

    # Calculate year by year
    while age < retirement_age:

        # Annual employee contribution
        employee_amount = (
            salary * 12 * employee_rate
        )

        # Annual employer contribution
        employer_amount = (
            salary * 12 * employer_rate
        )

        # Total contribution
        total_contribution = (
            employee_amount + employer_amount
        )

        # EPF contribution from bonus
        bonus_contribution = (
            bonus * (employee_rate + employer_rate)
        )

        # Annual withdrawals
        total_withdrawal = (
            monthly_withdrawal * 12
            + annual_withdrawal
        )

        # Update EPF balance
        epf_balance += total_contribution
        epf_balance += bonus_contribution
        epf_balance -= total_withdrawal

        # Apply dividend
        dividend = epf_balance * dividend_rate
        epf_balance += dividend

        # Increase salary
        salary *= (1 + increment_rate)

        # Next year
        age += 1

    return epf_balance


# ==========================================
# Streamlit Webpage
# ==========================================

st.set_page_config(
    page_title="EPF Retirement Calculator",
    page_icon="💰",
    layout="centered"
)

st.title("💰 EPF Retirement Calculator")

st.write(
    "Estimate your EPF balance at retirement "
    "based on your salary, contributions, dividend "
    "and withdrawals."
)


# ==========================================
# User Inputs
# ==========================================

st.header("Your Information")

epf_balance = st.number_input(
    "Current EPF Balance (RM)",
    min_value=0.0,
    value=100000.0,
    step=1000.0
)

age = st.number_input(
    "Current Age",
    min_value=18,
    max_value=70,
    value=30
)

retirement_age = st.number_input(
    "Retirement Age",
    min_value=40,
    max_value=80,
    value=60
)

salary = st.number_input(
    "Monthly Salary (RM)",
    min_value=0.0,
    value=5000.0,
    step=500.0
)


# ==========================================
# EPF Assumptions
# ==========================================

st.header("EPF Assumptions")

avg_dividend = st.number_input(
    "Average Annual Dividend (%)",
    min_value=0.0,
    max_value=20.0,
    value=5.5,
    step=0.1
)

employee_contribution = st.number_input(
    "Employee Contribution (%)",
    min_value=0.0,
    max_value=30.0,
    value=11.0,
    step=0.1
)

employer_contribution = st.number_input(
    "Employer Contribution (%)",
    min_value=0.0,
    max_value=30.0,
    value=13.0,
    step=0.1
)

increment = st.number_input(
    "Annual Salary Increment (%)",
    min_value=0.0,
    max_value=20.0,
    value=3.0,
    step=0.1
)

bonus = st.number_input(
    "Annual Bonus (RM)",
    min_value=0.0,
    value=0.0,
    step=1000.0
)


# ==========================================
# Withdrawals
# ==========================================

st.header("Withdrawals")

monthly_withdrawal = st.number_input(
    "Monthly Withdrawal (RM)",
    min_value=0.0,
    value=0.0,
    step=100.0
)

annual_withdrawal = st.number_input(
    "Additional Annual Withdrawal (RM)",
    min_value=0.0,
    value=0.0,
    step=1000.0
)


# ==========================================
# Calculate
# ==========================================

if st.button(
    "Calculate Retirement Balance",
    type="primary"
):

    result = calculate_epf_balance(
        epf_balance,
        avg_dividend,
        age,
        retirement_age,
        salary,
        bonus,
        increment,
        employee_contribution,
        employer_contribution,
        monthly_withdrawal,
        annual_withdrawal
    )

    st.divider()

    st.subheader("Retirement Projection")

    st.metric(
        "Estimated EPF Balance",
        f"RM {result:,.2f}"
    )

    years = retirement_age - age

    st.write(
        f"Your estimated balance at age "
        f"**{retirement_age}** after **{years} years** "
        f"is **RM {result:,.2f}**."
    )

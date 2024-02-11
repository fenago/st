import streamlit as st

# Function to calculate savings
def calculate_savings(num_employees, hours_saved_per_employee, cost_per_hour):
    weekly_savings = num_employees * hours_saved_per_employee * cost_per_hour
    monthly_savings = weekly_savings * 4  # Assuming 4 weeks in a month
    annual_savings = weekly_savings * 52  # Assuming 52 weeks in a year
    return weekly_savings, monthly_savings, annual_savings

# Streamlit app
def main():
    st.header('RPA Cost Savings Calculator')
    st.write("Estimate the financial impact of automation on your workforce. Input the number of employees, hours saved per employee per week, and the average cost per hour to see your potential savings.")

    # Display RPA related images
    st.image('https://www.appstudio.ca/blog/wp-content/uploads/2020/09/What-is-RPA.jpg', caption='Robotic Process Automation', use_column_width=True)

    # Inputs for calculations
    num_employees = st.number_input('Number of Employees', min_value=1, value=1, step=1, help='Enter the number of employees whose tasks have been automated.')
    hours_saved_per_employee = st.number_input('Hours Saved per Employee per Week', min_value=1.0, value=1.0, step=1.0, format='%f', help='Enter the average number of hours saved per employee per week due to automation.')
    cost_per_hour = st.number_input('Average Cost per Hour', min_value=0.0, value=150.0, step=1.0, format='%f', help='Enter the average cost per hour for the automated task.')

    # Button to compute savings
    if st.button('Compute Savings'):
        weekly_savings, monthly_savings, annual_savings = calculate_savings(num_employees, hours_saved_per_employee, cost_per_hour)
        st.success(f"Savings per Week: ${weekly_savings:,.2f}")
        st.success(f"Savings per Month: ${monthly_savings:,.2f}")
        st.success(f"Annual Savings: ${annual_savings:,.2f}")

if __name__ == "__main__":
    main()

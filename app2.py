import streamlit as st

# Function to calculate total cost savings
def calculate_cost_savings(hours_saved, cost_per_hour):
    return hours_saved * cost_per_hour

# Streamlit app
def main():
    st.header('RPA Cost Savings Calculator')
    st.write("This calculator helps to estimate the cost savings realized through automation. By automating tasks, companies can save valuable hours that would otherwise be spent on manual processes. Simply input the total hours saved and the cost per hour to see your total cost savings.")

    # Display RPA related images
    st.image('https://www.appstudio.ca/blog/wp-content/uploads/2020/09/What-is-RPA.jpg', caption='Robotic Process Automation', use_column_width=True)

    # Input for hours saved
    hours_saved = st.number_input('Hours Saved', min_value=0.0, format='%f', help='Enter the total number of full-time employee hours saved due to automation.')

    # Input for cost per hour
    cost_per_hour = st.number_input('Cost Per Hour', min_value=0.0, format='%f', help='Enter the cost per hour for the automated task.')

    # Calculate cost savings button
    if st.button('Calculate Cost Savings'):
        total_savings = calculate_cost_savings(hours_saved, cost_per_hour)
        st.success(f"Total Cost Savings: ${total_savings:.2f}")

if __name__ == "__main__":
    main()

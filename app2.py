import streamlit as st

# Function to calculate ROI metrics
def calculate_roi(hours_saved, dollars_saved):
    # You can add more complex calculations here if needed
    return hours_saved, dollars_saved

# Streamlit app
def main():
    st.header('ROI Metrics Data')
    st.subheader('Store arbitrary key values pairs against your job to help understand your ROI (return on investment) per job execution.')

    # Input for hours saved
    hours_saved = st.number_input('Hours Saved', min_value=0.0, format='%f', help='FTE hours saved each time this job is run. (Field key: hours)')

    # Input for dollars saved
    dollars_saved = st.number_input('Dollars Saved', min_value=0, help='Field key dollars-saved')

    # Calculate ROI metrics button
    if st.button('Calculate ROI Metrics'):
        hours, dollars = calculate_roi(hours_saved, dollars_saved)
        st.success(f"Hours Saved: {hours} hours")
        st.success(f"Dollars Saved: ${dollars}")

if __name__ == "__main__":
    main()

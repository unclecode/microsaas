import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from EnhancedMarketingEstimator import EnhancedMarketingEstimator

def test():
    # Initialize the class
    estimator = EnhancedMarketingEstimator(1000, 10)

    # Calculate TAM
    tam_dicts = estimator.calculate_tam()
    for key, value in tam_dicts.items():
        print(f"{key}: {value:,.0f}")

    # Estimate marketing budgets
    budget_cpc = estimator.calculate_budget_cpc()
    budget_cpm = estimator.calculate_budget_cpm()
    print(f"Estimated Marketing Budget for CPC Campaign: ${budget_cpc}")
    print(f"Estimated Marketing Budget for CPM Campaign: ${budget_cpm}")

    # Calculate time to reach target
    months_to_reach_target = estimator.calculate_time_to_reach_target(5000, 'CPC')
    print(f"Months to Reach Target: {months_to_reach_target}")

    # Estimate monthly maintenance budget
    maintenance_budget = estimator.calculate_maintenance_budget()
    print(f"Monthly Maintenance Budget: ${maintenance_budget}")

    # Plot user acquisition and cumulative marketing spend over time
    estimator.calculate_growth_over_time(5000, 'CPC')  # Simulate growth over time
    estimator.plot_user_acquisition()

def main():
    # test()
    # Streamlit interface
    st.title("Marketing Estimator Web App")

    # User inputs for primary parameters
    target_users = st.number_input("Target Paid Users", min_value=1, value=1000)
    subscription_fee = st.number_input("Average Monthly Subscription Fee", min_value=0.1, value=10.0)
    monthly_budget = st.number_input("Monthly Marketing Budget", min_value=100.0, value=5000.0)

    # Optional advanced settings
    with st.expander("Advanced Settings"):
        global_internet_users = st.number_input("Global Internet Users", value=5e9)
        growth_rate = st.number_input("Growth Rate", value=0.02)
        smartphone_user_percentage = st.number_input("Smartphone User Percentage", value=0.80)
        target_audience_percentage = st.number_input("Target Audience Percentage", value=0.05)
        willingness_to_pay_percentage = st.number_input("Willingness to Pay Percentage", value=0.10)
        average_cpc = st.number_input("Average CPC", value=1.00)
        average_cpm = st.number_input("Average CPM", value=10.00)
        ctr = st.number_input("CTR", value=0.02)
        conversion_rate = st.number_input("Conversion Rate", value=0.02)
        churn_rate = st.number_input("Churn Rate", value=0.05)

    # Button to run calculation
    if st.button('Calculate'):
        # Initialize and calculate using the class
        estimator = EnhancedMarketingEstimator(target_users, subscription_fee,
                                            global_internet_users=global_internet_users,
                                            growth_rate=growth_rate,
                                            smartphone_user_percentage=smartphone_user_percentage,
                                            target_audience_percentage=target_audience_percentage,
                                            willingness_to_pay_percentage=willingness_to_pay_percentage,
                                            average_cpc=average_cpc,
                                            average_cpm=average_cpm,
                                            ctr=ctr,
                                            conversion_rate=conversion_rate,
                                            churn_rate=churn_rate)

        # Display results
        tam_dict = estimator.calculate_tam()
        # Use comma separator for thousands
        for key, value in tam_dict.items():
            st.write(f"{key.replace('_', ' ').title()}: {value:,.0f} users")

        budget_cpc = estimator.calculate_budget_cpc()
        budget_cpm = estimator.calculate_budget_cpm()
        # Use comma separator for thousands for fees
        st.write(f"Estimated Marketing Budget for CPC Campaign: ${budget_cpc:,.0f}")
        st.write(f"Estimated Marketing Budget for CPM Campaign: ${budget_cpm:,.0f}")

        months_to_reach_target = estimator.calculate_time_to_reach_target(monthly_budget, 'CPC')
        st.write(f"Months to Reach Target: {months_to_reach_target}")

        maintenance_budget = estimator.calculate_maintenance_budget()
        st.write(f"Monthly Maintenance Budget: ${maintenance_budget:,.0f}")

        # Plot
        estimator.calculate_growth_over_time(monthly_budget, 'CPC')  # Simulate growth over time
        estimator.plot_user_acquisition()
        st.pyplot(plt)    

if __name__ == '__main__':
    main()
import matplotlib.pyplot as plt
import numpy as np

class EnhancedMarketingEstimator:
    def __init__(self, target_paid_users, avg_monthly_subscription, **kwargs):
        self.target_paid_users = target_paid_users
        self.avg_monthly_subscription = avg_monthly_subscription

        # Default values
        default_params = {
            'global_internet_users': 5e9,
            'growth_rate': 0.02,
            'smartphone_user_percentage': 0.80,
            'target_audience_percentage': 0.05,
            'willingness_to_pay_percentage': 0.10,
            'average_cpc': 1.00,
            'average_cpm': 10.00,
            'ctr': 0.02,
            'conversion_rate': 0.02,
            'churn_rate': 0.05
        }

        # Update default values with any provided parameters
        default_params.update(kwargs)

        # Set attributes
        for key, value in default_params.items():
            setattr(self, key, value)

        # Storing monthly data for plotting
        self.monthly_subscribers = []
        self.monthly_marketing_spend = []
        self.cumulative_marketing_spend = []

    def calculate_tam(self):
        smartphone_users = self.global_internet_users * self.smartphone_user_percentage
        target_audience = smartphone_users * self.target_audience_percentage
        tam = target_audience * self.willingness_to_pay_percentage
        return {
            'smartphone_users': smartphone_users,
            'target_audience': target_audience,
            'total_addressable_market': tam
        }

    def calculate_required_reach(self):
        return self.target_paid_users / self.conversion_rate

    def calculate_budget_cpc(self):
        clicks_needed = self.calculate_required_reach()
        return clicks_needed * self.average_cpc

    def calculate_budget_cpm(self):
        clicks_needed = self.calculate_required_reach()
        impressions_needed = clicks_needed / self.ctr
        return (impressions_needed / 1000) * self.average_cpm

    def calculate_time_to_reach_target(self, monthly_budget, campaign_type='CPC'):
        subscribers = 0
        months = 0
        total_spend = 0  # Initialize total spend
        while subscribers < self.target_paid_users:
            if campaign_type == 'CPC':
                reach = monthly_budget / self.average_cpc
            else:  # CPM
                impressions = (monthly_budget / self.average_cpm) * 1000
                reach = impressions * self.ctr

            new_subscribers = reach * self.conversion_rate
            subscribers = subscribers * (1 - self.churn_rate) + new_subscribers

            # Store monthly data
            total_spend += monthly_budget
            self.monthly_subscribers.append(subscribers)  # Update monthly subscribers list
            self.cumulative_marketing_spend.append(total_spend)  # Update cumulative spend list

            months += 1
        return months

    def calculate_maintenance_budget(self):
        churned_subscribers = self.target_paid_users * self.churn_rate
        required_new_subscribers = churned_subscribers / self.conversion_rate
        maintenance_budget = required_new_subscribers * self.average_cpc
        return maintenance_budget

    def calculate_growth_over_time(self, monthly_budget, campaign_type='CPC'):
        subscribers = 0
        months = 0
        subscribers_over_time = []
        while subscribers < self.target_paid_users:
            if campaign_type == 'CPC':
                reach = monthly_budget / self.average_cpc
            else:  # CPM
                impressions = (monthly_budget / self.average_cpm) * 1000
                reach = impressions * self.ctr
            
            new_subscribers = reach * self.conversion_rate
            subscribers = subscribers * (1 - self.churn_rate) + new_subscribers
            subscribers_over_time.append(subscribers)
            months += 1

        for _ in range(12):  # Additional 12 months for maintenance phase
            subscribers = subscribers * (1 - self.churn_rate) + self.calculate_maintenance_budget() / self.average_cpc
            subscribers_over_time.append(subscribers)
        
        return subscribers_over_time

    def plot_user_acquisition(self):
        months = np.arange(len(self.monthly_subscribers))
        fig, ax1 = plt.subplots()

        color = 'tab:blue'
        ax1.set_xlabel('Months')
        ax1.set_ylabel('Subscribers', color=color)
        ax1.plot(months, self.monthly_subscribers, color=color, marker='o')  # Scatter-like plot with circles
        ax1.tick_params(axis='y', labelcolor=color)

        ax2 = ax1.twinx()  # Create another axis sharing the same x-axis
        color = 'tab:red'
        ax2.set_ylabel('Cumulative Marketing Spend ($)', color=color)
        ax2.plot(months, self.cumulative_marketing_spend, color=color, linestyle='--')  # Cumulative spend as dashed line
        ax2.tick_params(axis='y', labelcolor=color)

        fig.tight_layout()  # Adjust the layout
        plt.title('User Acquisition and Cumulative Marketing Spend Over Time')
        plt.show()



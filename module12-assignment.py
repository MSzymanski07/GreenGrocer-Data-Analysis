# Module 12 Assignment: Business Analytics Fundamentals and Applications
# GreenGrocer Data Analysis

# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Welcome message
print("=" * 60)
print("GREENGROCER BUSINESS ANALYTICS")
print("=" * 60)

# ----- USE THE FOLLOWING CODE TO CREATE SAMPLE DATA (DO NOT MODIFY) -----
# Set seed for reproducibility
np.random.seed(42)

# Store information
stores = ["Tampa", "Orlando", "Miami", "Jacksonville", "Gainesville"]
store_data = {
    "Store": stores,
    "SquareFootage": [15000, 12000, 18000, 10000, 8000],
    "StaffCount": [45, 35, 55, 30, 25],
    "YearsOpen": [5, 3, 7, 2, 1],
    "WeeklyMarketingSpend": [2500, 2000, 3000, 1800, 1500]
}

# Create store dataframe
store_df = pd.DataFrame(store_data)

# Product categories and departments
departments = ["Produce", "Dairy", "Bakery", "Grocery", "Prepared Foods"]
categories = {
    "Produce": ["Organic Vegetables", "Organic Fruits", "Fresh Herbs"],
    "Dairy": ["Milk & Cream", "Cheese", "Yogurt"],
    "Bakery": ["Bread", "Pastries", "Cakes"],
    "Grocery": ["Grains", "Canned Goods", "Snacks"],
    "Prepared Foods": ["Hot Bar", "Salad Bar", "Sandwiches"]
}

# Generate sales data for each store
sales_data = []
dates = pd.date_range(start="2023-01-01", end="2023-12-31", freq="D")

# Base performance factors for each store (relative scale)
store_performance = {
    "Tampa": 1.0, 
    "Orlando": 0.85, 
    "Miami": 1.2, 
    "Jacksonville": 0.75, 
    "Gainesville": 0.65
}

# Base performance factors for each department (relative scale)
dept_performance = {
    "Produce": 1.2,
    "Dairy": 1.0,
    "Bakery": 0.85,
    "Grocery": 0.95,
    "Prepared Foods": 1.1
}

# Generate daily sales data for each store, department, and category
for date in dates:
    # Seasonal factor (higher in summer and December)
    month = date.month
    seasonal_factor = 1.0
    if month in [6, 7, 8]:  # Summer
        seasonal_factor = 1.15
    elif month == 12:  # December
        seasonal_factor = 1.25
    elif month in [1, 2]:  # Winter
        seasonal_factor = 0.9
    
    # Day of week factor (weekends are busier)
    dow_factor = 1.3 if date.dayofweek >= 5 else 1.0  # Weekend vs weekday
    
    for store in stores:
        store_factor = store_performance[store]
        
        for dept in departments:
            dept_factor = dept_performance[dept]
            
            for category in categories[dept]:
                # Base sales amount
                base_sales = np.random.normal(loc=500, scale=100)
                
                # Calculate final sales with all factors and some randomness
                sales_amount = base_sales * store_factor * dept_factor * seasonal_factor * dow_factor
                sales_amount = sales_amount * np.random.normal(loc=1.0, scale=0.1)  # Add noise
                
                # Calculate profit margin (different base margins for departments)
                base_margin = {
                    "Produce": 0.25,
                    "Dairy": 0.22,
                    "Bakery": 0.35,
                    "Grocery": 0.20,
                    "Prepared Foods": 0.40
                }[dept]
                profit_margin = base_margin * np.random.normal(loc=1.0, scale=0.05)
                profit_margin = max(min(profit_margin, 0.5), 0.15)  # Keep within reasonable range
                
                # Calculate profit
                profit = sales_amount * profit_margin
                
                # Add record
                sales_data.append({
                    "Date": date,
                    "Store": store,
                    "Department": dept,
                    "Category": category,
                    "Sales": round(sales_amount, 2),
                    "ProfitMargin": round(profit_margin, 4),
                    "Profit": round(profit, 2)
                })

# Create sales dataframe
sales_df = pd.DataFrame(sales_data)

# Generate customer data
customer_data = []
total_customers = 5000

# Age distribution parameters
age_mean, age_std = 42, 15

# Income distribution parameters (in $1000s)
income_mean, income_std = 85, 30

# Create customer segments (will indirectly influence spending)
segments = ["Health Enthusiast", "Gourmet Cook", "Family Shopper", "Budget Organic", "Occasional Visitor"]
segment_probabilities = [0.25, 0.20, 0.30, 0.15, 0.10]

# Store preference probabilities (matches store performance somewhat)
store_probs = {
    "Tampa": 0.25,
    "Orlando": 0.20,
    "Miami": 0.30,
    "Jacksonville": 0.15,
    "Gainesville": 0.10
}

for i in range(total_customers):
    # Basic demographics
    age = int(np.random.normal(loc=age_mean, scale=age_std))
    age = max(min(age, 85), 18)  # Keep age in reasonable range
    
    gender = np.random.choice(["M", "F"], p=[0.48, 0.52])
    
    income = int(np.random.normal(loc=income_mean, scale=income_std))
    income = max(income, 20)  # Minimum income
    
    # Customer segment
    segment = np.random.choice(segments, p=segment_probabilities)
    
    # Preferred store
    preferred_store = np.random.choice(stores, p=list(store_probs.values()))
    
    # Shopping behavior - influenced by segment
    if segment == "Health Enthusiast":
        visit_frequency = np.random.randint(8, 15)  # Visits per month
        avg_basket = np.random.normal(loc=75, scale=15)
    elif segment == "Gourmet Cook":
        visit_frequency = np.random.randint(4, 10)
        avg_basket = np.random.normal(loc=120, scale=25)
    elif segment == "Family Shopper":
        visit_frequency = np.random.randint(5, 12)
        avg_basket = np.random.normal(loc=150, scale=30)
    elif segment == "Budget Organic":
        visit_frequency = np.random.randint(6, 10)
        avg_basket = np.random.normal(loc=60, scale=10)
    else:  # Occasional Visitor
        visit_frequency = np.random.randint(1, 5)
        avg_basket = np.random.normal(loc=45, scale=15)
    
    # Ensure values are reasonable
    visit_frequency = max(min(visit_frequency, 30), 1)
    avg_basket = max(avg_basket, 15)
    
    # Loyalty tier based on combination of frequency and spending
    monthly_spend = visit_frequency * avg_basket
    if monthly_spend > 1000:
        loyalty_tier = "Platinum"
    elif monthly_spend > 500:
        loyalty_tier = "Gold"
    elif monthly_spend > 200:
        loyalty_tier = "Silver"
    else:
        loyalty_tier = "Bronze"
    
    # Add to customer data
    customer_data.append({
        "CustomerID": f"C{i+1:04d}",
        "Age": age,
        "Gender": gender,
        "Income": income * 1000,  # Convert to actual income
        "Segment": segment,
        "PreferredStore": preferred_store,
        "VisitsPerMonth": visit_frequency,
        "AvgBasketSize": round(avg_basket, 2),
        "MonthlySpend": round(visit_frequency * avg_basket, 2),
        "LoyaltyTier": loyalty_tier
    })

# Create customer dataframe
customer_df = pd.DataFrame(customer_data)

# Create some calculated operational metrics for stores
operational_data = []

for store in stores:
    # Get store details
    store_row = store_df[store_df["Store"] == store].iloc[0]
    square_footage = store_row["SquareFootage"]
    staff_count = store_row["StaffCount"]
    
    # Calculate store metrics
    store_sales = sales_df[sales_df["Store"] == store]["Sales"].sum()
    store_profit = sales_df[sales_df["Store"] == store]["Profit"].sum()
    
    # Calculate derived metrics
    sales_per_sqft = store_sales / square_footage
    profit_per_sqft = store_profit / square_footage
    sales_per_staff = store_sales / staff_count
    inventory_turnover = np.random.uniform(12, 18) * store_performance[store]
    customer_satisfaction = min(5, np.random.normal(loc=4.0, scale=0.3) * 
                                (store_performance[store] ** 0.5))
    
    # Add to operational data
    operational_data.append({
        "Store": store,
        "AnnualSales": round(store_sales, 2),
        "AnnualProfit": round(store_profit, 2),
        "SalesPerSqFt": round(sales_per_sqft, 2),
        "ProfitPerSqFt": round(profit_per_sqft, 2),
        "SalesPerStaff": round(sales_per_staff, 2),
        "InventoryTurnover": round(inventory_turnover, 2),
        "CustomerSatisfaction": round(customer_satisfaction, 2)
    })

# Create operational dataframe
operational_df = pd.DataFrame(operational_data)

# Print data info
print("\nDataframes created successfully. Ready for analysis!")
print(f"Sales data shape: {sales_df.shape}")
print(f"Customer data shape: {customer_df.shape}")
print(f"Store data shape: {store_df.shape}")
print(f"Operational data shape: {operational_df.shape}")

# Print sample of each dataframe
print("\nSales Data Sample:")
print(sales_df.head(3))
print("\nCustomer Data Sample:")
print(customer_df.head(3))
print("\nStore Data Sample:")
print(store_df)
print("\nOperational Data Sample:")
print(operational_df)
# ----- END OF DATA CREATION -----


# TODO 1: Descriptive Analytics - Overview of Current Performance
# 1.1 Calculate and display basic descriptive statistics for sales and profit
def analyze_sales_performance():
    total_sales = sales_df["Sales"].sum()
    total_profit = sales_df["Profit"].sum()
    avg_profit_margin = sales_df["ProfitMargin"].mean()
    sales_by_store = sales_df.groupby("Store")["Sales"].sum()
    sales_by_dept = sales_df.groupby("Department")["Sales"].sum()
    
    sales_performance = {
        "total_sales": float(total_sales),
        "total_profit": float(total_profit),
        "avg_profit_margin": float(avg_profit_margin),
        "sales_by_store": sales_by_store,
        "sales_by_dept": sales_by_dept
        }
    return sales_performance

# 1.2 Create visualizations showing sales distribution by store, department, and time
def visualize_sales_distribution():
    # Store Fig
    store_sales = sales_df.groupby("Store")["Sales"].sum()
    
    store_fig, ax1 = plt.subplots()
    store_sales.plot(kind="bar", ax=ax1, color="blue")
    ax1.set_title("Total Sales by Store")
    ax1.set_xlabel("Store")
    ax1.set_ylabel("Sales")
    ax1.tick_params(axis='x', rotation=45)
    
    # Dept Fig
    dept_sales = sales_df.groupby("Department")["Sales"].sum()
    
    dept_fig, ax2 = plt.subplots()
    dept_sales.plot(kind="bar", ax=ax2, color="red")
    ax2.set_title("Total Sales by Department")
    ax2.set_xlabel("Department")
    ax2.set_ylabel("Sales")
    ax2.tick_params(axis='x', rotation=45)
    
    # Time Fig
    sales_over_time = sales_df.groupby("Date")["Sales"].sum()
    
    time_fig, ax3 = plt.subplots()
    sales_over_time.plot(ax=ax3)
    ax3.set_title("Sales Over Time")
    ax3.set_xlabel("Date")
    ax3.set_ylabel("Sales")
    return store_fig, dept_fig, time_fig

# 1.3 Analyze customer segments and their spending patterns
def analyze_customer_segments():
    segment_counts = customer_df["Segment"].value_counts()
    segment_avg_spend = customer_df.groupby("Segment")["MonthlySpend"].mean()
    segment_loyalty = pd.crosstab(customer_df["Segment"], customer_df["LoyaltyTier"])
    customer_segments_analysis = {
        "segment_counts": segment_counts,
        "segment_avg_spend": segment_avg_spend,
        "segment_loyalty": segment_loyalty
        }
    return customer_segments_analysis

# TODO 2: Diagnostic Analytics - Understanding Relationships
# 2.1 Identify factors correlated with sales performance
def analyze_sales_correlations():
    store_correlations = operational_df.corr(numeric_only=True)
    sales_corr = store_correlations["AnnualSales"].drop("AnnualSales")
    sorted_corr = sales_corr.sort_values(ascending=False).items()
    top_correlations = list(sorted_corr)
    
    correlation_fig, ax = plt.subplots(figsize=(8, 6))
    cax = ax.imshow(store_correlations, cmap="coolwarm", vmin=-1, vmax=1)
    ax.set_title("Sales Correlations Matrix")
    ax.set_xticks(range(len(store_correlations.columns)))
    ax.set_yticks(range(len(store_correlations.columns)))
    ax.set_xticklabels(store_correlations.columns, rotation=45, ha="right")
    ax.set_yticklabels(store_correlations.columns)
    plt.colorbar(cax, ax=ax)
    
    sales_correlations = {
        "store_correlations": store_correlations,
        "top_correlations": top_correlations,
        "correlation_fig": correlation_fig
        }
    return sales_correlations

# 2.2 Compare stores based on operational metrics
def compare_store_performance():
    efficiency_metrics = operational_df[["Store", "SalesPerSqFt", "SalesPerStaff"]].set_index("Store")
    performance_ranking = operational_df.set_index("Store")["AnnualProfit"].sort_values(ascending=False)
    
    comparison_fig, ax = plt.subplots()
    ax.bar(operational_df["Store"], operational_df["AnnualProfit"], color="green")
    ax.set_title("Annual Profit by Store")
    ax.set_xlabel("Store")
    ax.set_ylabel("Annual Profit")
    ax.tick_params(axis='x', rotation=45)
    
    store_perform_comparison = {
        "efficiency_metrics": efficiency_metrics,
        "performance_ranking": performance_ranking,
        "comparison_fig": comparison_fig
        }
    return store_perform_comparison

# 2.3 Analyze seasonal patterns and their impact
def analyze_seasonal_patterns():
    sales_df["Date"] = pd.to_datetime(sales_df["Date"])
    monthly_sales = sales_df.groupby(sales_df["Date"].dt.month)["Sales"].sum()
    monthly_sales.index = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][:len(monthly_sales)]
    dow_sales = sales_df.groupby(sales_df["Date"].dt.dayofweek)["Sales"].sum()
    dow_sales.index = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    
    seasonal_fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    # Monthly plot
    monthly_sales.plot(kind="line", ax=ax1)
    ax1.set_title("Monthly Sales Trend")
    ax1.set_xlabel("Month")
    ax1.set_ylabel("Sales")
    # Dow plot
    dow_sales.plot(kind="bar", ax=ax2, color="orange")
    ax2.set_title("Sales by Day of Week")
    ax2.set_xlabel("Day")
    ax2.set_ylabel("Sales")
    plt.tight_layout()
    
    seasonal_patterns = {
        "monthly_sales": monthly_sales,
        "dow_sales": dow_sales,
        "seasonal_fig": seasonal_fig
        }
    return seasonal_patterns

# TODO 3: Predictive Analytics - Basic Forecasting
# 3.1 Create a simple linear regression model to predict store sales
def predict_store_sales():
    characteristics = ["SalesPerSqFt", "SalesPerStaff", "InventoryTurnover", "CustomerSatisfaction"]
    
    X = operational_df[characteristics]
    y = operational_df["AnnualSales"]
    score = X.mean(axis=1)
    slope, intercept = np.polyfit(score, y, 1)
    predictions = slope * score + intercept
    predictions = pd.Series(predictions, index=operational_df["Store"])
    ss_res = ((y - predictions) ** 2).sum()
    ss_tot = ((y - y.mean()) ** 2).sum()
    r_squared = 1 - ss_res / ss_tot
    
    coefficients = {"operational_score": slope}
    
    model_fig, ax = plt.subplots()
    sorted_idx = np.argsort(score)
    ax.scatter(score, y)
    ax.plot(score.iloc[sorted_idx], predictions.iloc[sorted_idx])
    ax.set_title("Store Sales vs Operational Score")
    ax.set_xlabel("Operational Score")
    ax.set_ylabel("Annual Sales")
    
    store_sales_predictions = {
        "coefficients": coefficients,
        "r_squared": r_squared,
        "predictions": predictions,
        "model_fig": model_fig
        }
    return store_sales_predictions

# 3.2 Forecast departmental sales trends
def forecast_department_sales():
    sales_df["Date"] = pd.to_datetime(sales_df["Date"])
    dept_trends = sales_df.groupby([sales_df["Date"].dt.to_period("M"), "Department"])["Sales"].sum().unstack()
    growth_rates = dept_trends.pct_change().mean()
    
    forecast_fig, ax = plt.subplots(figsize=(10, 5))
    dept_trends.plot(ax=ax)
    ax.set_title("Department Sales Trends Over Time")
    ax.set_xlabel("Month")
    ax.set_ylabel("Sales")
    
    department_sales_forecast = {
        "dept_trends": dept_trends,
        "growth_rates": growth_rates,
        "forecast_fig": forecast_fig
        }
    return department_sales_forecast

# TODO 4: Integrated Analysis - Business Insights and Recommendations
# 4.1 Identify the most profitable combinations of store, department, and customer segments
def identify_profit_opportunities():
    """
    Identify the most profitable combinations and potential opportunities
    REQUIRED: Return dictionary with keys:
    - 'top_combinations': pandas DataFrame (top 10 store-dept combinations)
    - 'underperforming': pandas DataFrame (bottom 10)
    - 'opportunity_score': pandas Series (by store)
    """
    combination = sales_df.groupby(["Store", "Department"])[["Sales", "Profit"]].sum().reset_index()
    top_combinations = combination.sort_values("Profit", ascending=False).head(10)
    underperforming = combination.sort_values("Profit", ascending=True).head(10)
    opportunity_score = sales_df.groupby("Store")["Profit"].sum().sort_values(ascending=False)
    
    profit_opportunities = {
        "top_combinations": top_combinations,
        "underperforming": underperforming,
        "opportunity_score": opportunity_score
        }
    return profit_opportunities

# 4.2 Develop recommendations for improving performance
def develop_recommendations():
    recommendations = [
        "Invest in Miami Store Location",
        "Increase Profitability in Jacksonville and Gainesville",
        "Increase Customer Satisfaction to increase Sales and Profit",
        "Focus on Sales Towards the End of the Year",
        "Focus on Sales during Weekends"
        ]
    return recommendations

# TODO 5: Summary Report
def generate_executive_summary():
    """
    Generate an executive summary of key findings and recommendations
    REQUIRED: Print executive summary with sections:
    - Overview (1 paragraph)
    - Key Findings (3-5 bullet points)
    - Recommendations (3-5 bullet points)
    - Expected Impact (1 paragraph)
    """
    print("\nEXECUTIVE SUMMARY OF KEY FINDINGS AND RECOMMENDATIONS")
    print("""
    Overview:
    Our program has managed to successfully organize and visualize company, customer, and operational data.
    With our visualization efforts we have discovered a few key insights that could be useful to GreenGrocer.
    Along with these insights, we will put forward a few recomendations to GreenGrocer.
    """)
    print("""
    Key Findings:
    - Miami location has the highest sales and profitability
    - Produce department is the highest selling
    - Sales are highest on weekends and towards the end of the year
    """)
    print("""
    Recommendations:
    - Invest in Miami Store Location
    - Have discounts on produce to draw in customers and increase sales
    - Focus on sales towards the end of the year and on weekends
    """)
    print("""
    Expected Impact:
    We hope that the discoveries this program has made will impact GreenGrocer strategy in a positive way.
    Our insights and recommendations will likely be key in influencing future decisions by the business.
    """)
    
# Main function to execute all analyses
# REQUIRED: Do not modify function name
def main():
    print("\n" + "=" * 60)
    print("GREENGROCER BUSINESS ANALYTICS RESULTS")
    print("=" * 60)
    
    # Execute analyses in a logical order
    # REQUIRED: Store all results for potential testing
    
    print("\n--- DESCRIPTIVE ANALYTICS: CURRENT PERFORMANCE ---")
    sales_metrics = analyze_sales_performance()
    dist_figs = visualize_sales_distribution()
    customer_analysis = analyze_customer_segments()
    
    print("\n--- DIAGNOSTIC ANALYTICS: UNDERSTANDING RELATIONSHIPS ---")
    correlations = analyze_sales_correlations()
    store_comparison = compare_store_performance()
    seasonality = analyze_seasonal_patterns()
    
    print("\n--- PREDICTIVE ANALYTICS: FORECASTING ---")
    sales_model = predict_store_sales()
    dept_forecast = forecast_department_sales()
    
    print("\n--- BUSINESS INSIGHTS AND RECOMMENDATIONS ---")
    opportunities = identify_profit_opportunities()
    recommendations = develop_recommendations()
    
    print("\n--- EXECUTIVE SUMMARY ---")
    generate_executive_summary()
    
    # Show all figures
    plt.show()
    
    # Return results for testing purposes
    return {
        'sales_metrics': sales_metrics,
        'customer_analysis': customer_analysis,
        'correlations': correlations,
        'store_comparison': store_comparison,
        'seasonality': seasonality,
        'sales_model': sales_model,
        'dept_forecast': dept_forecast,
        'opportunities': opportunities,
        'recommendations': recommendations
    }

# Run the main function
if __name__ == "__main__":
    results = main()
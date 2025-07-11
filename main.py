import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import os

# Set page configuration
st.set_page_config(
    page_title="Telecom Customer Churn Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #0D47A1;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #E3F2FD;
        padding-bottom: 0.5rem;
    }
    .metric-card {
        background-color: #F5F5F5;
        border-radius: 5px;
        padding: 1rem;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }
    .insight-text {
        background-color: #E3F2FD;
        border-left: 5px solid #1E88E5;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .recommendation-card {
        background-color: #E8F5E9;
        border-left: 5px solid #43A047;
        padding: 1rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Function to load data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("C:/Users/asus//Downloads/churn_dataset.csv")
    except FileNotFoundError:
        st.warning("Data file not found. Using sample data for demonstration.")
        # Create sample data
        np.random.seed(42)
        n_samples = 7043
        
        # Generate sample data
        data = {
            'gender': np.random.choice(['Male', 'Female'], n_samples),
            'SeniorCitizen': np.random.choice([0, 1], n_samples, p=[0.8, 0.2]),
            'Partner': np.random.choice(['Yes', 'No'], n_samples, p=[0.5, 0.5]),
            'Dependents': np.random.choice(['Yes', 'No'], n_samples, p=[0.3, 0.7]),
            'tenure': np.random.randint(1, 73, n_samples),
            'PhoneService': np.random.choice(['Yes', 'No'], n_samples, p=[0.9, 0.1]),
            'MultipleLines': np.random.choice(['Yes', 'No', 'No phone service'], n_samples, p=[0.4, 0.4, 0.2]),
            'InternetService': np.random.choice(['DSL', 'Fiber optic', 'No'], n_samples, p=[0.4, 0.3, 0.3]),
            'OnlineSecurity': np.random.choice(['Yes', 'No', 'No internet service'], n_samples, p=[0.3, 0.4, 0.3]),
            'OnlineBackup': np.random.choice(['Yes', 'No', 'No internet service'], n_samples, p=[0.3, 0.4, 0.3]),
            'DeviceProtection': np.random.choice(['Yes', 'No', 'No internet service'], n_samples, p=[0.3, 0.4, 0.3]),
            'TechSupport': np.random.choice(['Yes', 'No', 'No internet service'], n_samples, p=[0.3, 0.4, 0.3]),
            'StreamingTV': np.random.choice(['Yes', 'No', 'No internet service'], n_samples, p=[0.3, 0.4, 0.3]),
            'StreamingMovies': np.random.choice(['Yes', 'No', 'No internet service'], n_samples, p=[0.3, 0.4, 0.3]),
            'Contract': np.random.choice(['Month-to-month', 'One year', 'Two year'], n_samples, p=[0.5, 0.3, 0.2]),
            'PaperlessBilling': np.random.choice(['Yes', 'No'], n_samples, p=[0.6, 0.4]),
            'PaymentMethod': np.random.choice(['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)'], n_samples, p=[0.3, 0.2, 0.25, 0.25]),
            'MonthlyCharges': np.random.uniform(18, 120, n_samples),
            'TotalCharges': np.random.uniform(18, 8000, n_samples),
            'Churn': np.random.choice(['Yes', 'No'], n_samples, p=[0.265, 0.735])
        }
        
        df = pd.DataFrame(data)
    
    # Convert TotalCharges to numeric
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    # Fill missing values
    df['TotalCharges'] = df['TotalCharges'].fillna(df['MonthlyCharges'])
    # Convert SeniorCitizen to categorical
    df['SeniorCitizen'] = df['SeniorCitizen'].map({0: 'No', 1: 'Yes'})
    return df

# Main function to run the app
def main():
    # Sidebar
    with st.sidebar:
        st.title("Navigation")
        page = st.radio(
            "Go to",
            ["Executive Summary", "Customer Demographics", "Service Analysis", 
             "Contract & Charges", "Churn Prediction", "Recommendations"]
        )
        
        st.markdown("---")
        st.subheader("About")
        st.info(
            """
            This dashboard provides interactive analysis of customer churn 
            for a telecommunications company. Explore different sections to 
            understand factors affecting customer retention.
            """
        )
        
        st.markdown("---")
        st.subheader("Filters")
        # These filters will be applied across all pages
        
    # Load data
    df = load_data()
    
    # Header
    st.markdown("<h1 class='main-header'>Telecom Customer Churn Analysis Dashboard</h1>", unsafe_allow_html=True)
    
    # Executive Summary Page
    if page == "Executive Summary":
        executive_summary(df)
    
    # Customer Demographics Page
    elif page == "Customer Demographics":
        customer_demographics(df)
    
    # Service Analysis Page
    elif page == "Service Analysis":
        service_analysis(df)
    
    # Contract & Charges Page
    elif page == "Contract & Charges":
        contract_charges_analysis(df)
    
    # Churn Prediction Page
    elif page == "Churn Prediction":
        churn_prediction(df)
    
    # Recommendations Page
    elif page == "Recommendations":
        recommendations()

# Executive Summary Page
def executive_summary(df):
    st.markdown("<h2 class='sub-header'>Executive Summary</h2>", unsafe_allow_html=True)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Customers", f"{len(df):,}")
    
    with col2:
        churn_rate = df['Churn'].value_counts(normalize=True).loc['Yes'] * 100
        st.metric("Churn Rate", f"{churn_rate:.2f}%")
    
    with col3:
        avg_tenure = df['tenure'].mean()
        st.metric("Avg. Tenure (months)", f"{avg_tenure:.1f}")
    
    with col4:
        avg_monthly = df['MonthlyCharges'].mean()
        st.metric("Avg. Monthly Charges", f"${avg_monthly:.2f}")
    
    st.markdown("---")
    
    # Overview text
    st.markdown("""
    <div class='insight-text'>
    <h3>Overview</h3>
    <p>This dashboard analyzes customer churn patterns for a telecommunications company. 
    The overall churn rate is 26.54%, with 1,869 customers having churned out of 7,043 total customers. 
    The analysis identifies key factors influencing customer decisions to leave the service.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Two column layout for key visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        # Churn distribution chart
        churn_counts = df['Churn'].value_counts()
        fig = px.pie(values=churn_counts.values, names=churn_counts.index, 
                    title="Overall Churn Distribution",
                    color_discrete_sequence=['#3498db', '#e74c3c'])
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        <div class='insight-text'>
        <p>The chart shows the distribution of customers who have churned versus those who have stayed. 
        26.54% of customers have left the service, representing a significant portion of the customer base.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Contract analysis chart
        contract_churn = df.groupby('Contract')['Churn'].apply(
            lambda x: (x == 'Yes').mean() * 100).reset_index()
        contract_churn.columns = ['Contract', 'Churn Rate (%)']
        
        fig = px.bar(contract_churn, x='Contract', y='Churn Rate (%)',
                    title="Churn by Contract Type",
                    color='Churn Rate (%)', color_continuous_scale='Reds')
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        <div class='insight-text'>
        <p>Contract type is the strongest predictor of churn. Month-to-month contracts show a 42.71% churn rate, 
        compared to just 11.27% for one-year contracts and only 2.83% for two-year contracts.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Key findings section
    st.markdown("<h3 class='sub-header'>Key Findings</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Tenure vs churn rate
        df['tenure_group'] = pd.cut(df['tenure'], bins=[0, 12, 24, 36, 48, 72], 
                                   labels=['0-12', '13-24', '25-36', '37-48', '49+'])
        tenure_churn = df.groupby('tenure_group')['Churn'].apply(
            lambda x: (x == 'Yes').mean() * 100).reset_index()
        tenure_churn.columns = ['Tenure Group', 'Churn Rate (%)']
        
        fig = px.line(tenure_churn, x='Tenure Group', y='Churn Rate (%)',
                     title="Churn Rate by Tenure",
                     markers=True)
        fig.update_layout(xaxis_title='Tenure (months)', yaxis_title='Churn Rate (%)')
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        <div class='insight-text'>
        <p>Customer tenure shows a strong negative correlation with churn. New customers with less than 12 months 
        of tenure have a 48.28% churn rate, while customers with more than 40 months show only a 10.99% churn rate.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Customer segment analysis
        df['segment'] = pd.cut(df['MonthlyCharges'], bins=[0, 40, 80, 120], 
                              labels=['Low', 'Medium', 'High'])
        segment_churn = df.groupby(['segment', 'Contract'])['Churn'].apply(
            lambda x: (x == 'Yes').mean() * 100).reset_index()
        segment_churn.columns = ['Monthly Charges', 'Contract', 'Churn Rate (%)']
        
        fig = px.scatter(segment_churn, x='Monthly Charges', y='Churn Rate (%)', 
                        color='Contract', size='Churn Rate (%)',
                        title="Churn Rate by Customer Segment")
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        <div class='insight-text'>
        <p>New customers with high monthly charges have the highest risk with a 73.76% churn rate, 
        while long-term customers with low charges show only a 2.79% churn rate.</p>
        </div>
        """, unsafe_allow_html=True)

# Customer Demographics Page
def customer_demographics(df):
    st.markdown("<h2 class='sub-header'>Customer Demographics Analysis</h2>", unsafe_allow_html=True)
    
    # Filters for this page
    col1, col2 = st.columns(2)
    with col1:
        gender_filter = st.multiselect("Filter by Gender", options=df['gender'].unique(), default=df['gender'].unique())
    with col2:
        senior_filter = st.multiselect("Filter by Senior Citizen", options=df['SeniorCitizen'].unique(), default=df['SeniorCitizen'].unique())
    
    # Apply filters
    filtered_df = df[(df['gender'].isin(gender_filter)) & (df['SeniorCitizen'].isin(senior_filter))]
    
    # Demographics overview
    st.markdown("<h3>Demographics Overview</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gender distribution
        fig = px.pie(filtered_df, names='gender', title='Gender Distribution',
                    color_discrete_sequence=px.colors.qualitative.Set2)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
        
        # Partner distribution
        fig = px.pie(filtered_df, names='Partner', title='Partner Status Distribution',
                    color_discrete_sequence=px.colors.qualitative.Pastel)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Senior Citizen distribution
        fig = px.pie(filtered_df, names='SeniorCitizen', title='Senior Citizen Distribution',
                    color_discrete_sequence=px.colors.qualitative.Bold)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
        
        # Dependents distribution
        fig = px.pie(filtered_df, names='Dependents', title='Dependents Status Distribution',
                    color_discrete_sequence=px.colors.qualitative.Pastel1)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    # Churn analysis by demographics
    st.markdown("<h3 class='sub-header'>Churn Analysis by Demographics</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gender vs Churn
        fig = px.histogram(filtered_df, x='gender', color='Churn', barmode='group',
                          title='Churn Distribution by Gender',
                          color_discrete_sequence=['#3498db', '#e74c3c'])
        fig.update_layout(xaxis_title='Gender', yaxis_title='Count')
        st.plotly_chart(fig, use_container_width=True)
        
        # Partner vs Churn
        fig = px.histogram(filtered_df, x='Partner', color='Churn', barmode='group',
                          title='Churn Distribution by Partner Status',
                          color_discrete_sequence=['#3498db', '#e74c3c'])
        fig.update_layout(xaxis_title='Partner Status', yaxis_title='Count')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Senior Citizen vs Churn
        fig = px.histogram(filtered_df, x='SeniorCitizen', color='Churn', barmode='group',
                          title='Churn Distribution by Senior Citizen Status',
                          color_discrete_sequence=['#3498db', '#e74c3c'])
        fig.update_layout(xaxis_title='Senior Citizen', yaxis_title='Count')
        st.plotly_chart(fig, use_container_width=True)
        
        # Dependents vs Churn
        fig = px.histogram(filtered_df, x='Dependents', color='Churn', barmode='group',
                          title='Churn Distribution by Dependents Status',
                          color_discrete_sequence=['#3498db', '#e74c3c'])
        fig.update_layout(xaxis_title='Dependents', yaxis_title='Count')
        st.plotly_chart(fig, use_container_width=True)
    
    # Churn rates by demographic combinations
    st.markdown("<h3 class='sub-header'>Churn Rates by Demographic Combinations</h3>", unsafe_allow_html=True)
    
    # Create demographic combinations
    filtered_df['demographic_group'] = filtered_df['gender'] + ', ' + filtered_df['SeniorCitizen'] + ' senior, ' + \
                                      filtered_df['Partner'] + ' partner, ' + filtered_df['Dependents'] + ' dependents'
    
    # Calculate churn rate by demographic group
    demo_churn = filtered_df.groupby('demographic_group')['Churn'].apply(
        lambda x: (x == 'Yes').mean() * 100).reset_index()
    demo_churn.columns = ['Demographic Group', 'Churn Rate (%)']
    demo_churn = demo_churn.sort_values('Churn Rate (%)', ascending=False)
    
    # Plot top 10 demographic groups by churn rate
    fig = px.bar(demo_churn.head(10), x='Churn Rate (%)', y='Demographic Group', 
                orientation='h', title='Top 10 Demographic Groups by Churn Rate',
                color='Churn Rate (%)', color_continuous_scale='Reds')
    fig.update_layout(yaxis_title='', xaxis_title='Churn Rate (%)')
    st.plotly_chart(fig, use_container_width=True)
    
    # Insights
    st.markdown("""
    <div class='insight-text'>
    <h3>Key Insights - Demographics</h3>
    <ul>
        <li>Senior citizens have a higher propensity to churn compared to non-seniors</li>
        <li>Customers without partners or dependents show higher churn rates</li>
        <li>Gender alone is not a strong predictor of churn</li>
        <li>The combination of being a senior citizen without dependents represents the highest risk demographic segment</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# Service Analysis Page
def service_analysis(df):
    st.markdown("<h2 class='sub-header'>Service Analysis</h2>", unsafe_allow_html=True)
    
    # Service selection filter
    service_options = ['PhoneService', 'MultipleLines', 'InternetService', 'OnlineSecurity', 
                      'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies']
    selected_services = st.multiselect("Select Services to Analyze", options=service_options, 
                                      default=['InternetService', 'OnlineSecurity', 'TechSupport'])
    
    # Service distribution
    st.markdown("<h3>Service Distribution</h3>", unsafe_allow_html=True)
    
    # Create columns based on number of selected services
    cols = st.columns(min(3, len(selected_services)))
    
    # Display distribution for each selected service
    for i, service in enumerate(selected_services):
        with cols[i % len(cols)]:
            fig = px.pie(df, names=service, title=f'{service} Distribution',
                        color_discrete_sequence=px.colors.qualitative.Bold)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
    
    # Service impact on churn
    st.markdown("<h3 class='sub-header'>Service Impact on Churn</h3>", unsafe_allow_html=True)
    
    # Create service impact chart
    service_impact_data = []
    for service in service_options:
        service_churn = df.groupby(service)['Churn'].apply(
            lambda x: (x == 'Yes').mean() * 100).reset_index()
        service_churn.columns = [service, 'Churn Rate (%)']
        service_impact_data.append(service_churn)
    
    # Combine all service data
    all_service_data = pd.concat(service_impact_data, ignore_index=True)
    
    # Create heatmap-style visualization
    fig = px.bar(all_service_data, x=all_service_data.columns[0], y='Churn Rate (%)',
                title="Impact of Services on Churn Rate",
                color='Churn Rate (%)', color_continuous_scale='Blues')
    st.plotly_chart(fig, use_container_width=True)
    
    # Interactive service churn analysis
    st.markdown("<h3>Interactive Service Churn Analysis</h3>", unsafe_allow_html=True)
    
    # Select service for detailed analysis
    selected_service = st.selectbox("Select a service for detailed analysis", options=service_options)
    
    # Calculate churn rate by selected service
    service_churn = df.groupby(selected_service)['Churn'].apply(
        lambda x: (x == 'Yes').mean() * 100).reset_index()
    service_churn.columns = [selected_service, 'Churn Rate (%)']
    
    # Plot
    fig = px.bar(service_churn, x=selected_service, y='Churn Rate (%)', 
                title=f'Churn Rate by {selected_service}',
                color='Churn Rate (%)', color_continuous_scale='Blues')
    st.plotly_chart(fig, use_container_width=True)
    
    # Service combinations analysis
    st.markdown("<h3 class='sub-header'>Service Combinations Analysis</h3>", unsafe_allow_html=True)
    
    # Select two services to analyze together
    col1, col2 = st.columns(2)
    with col1:
        service1 = st.selectbox("Select first service", options=service_options, index=2)  # InternetService
    with col2:
        remaining_options = [s for s in service_options if s != service1]
        service2 = st.selectbox("Select second service", options=remaining_options, index=2)  # TechSupport
    
    # Calculate churn rate by service combination
    combo_churn = df.groupby([service1, service2])['Churn'].apply(
        lambda x: (x == 'Yes').mean() * 100).reset_index()
    combo_churn.columns = [service1, service2, 'Churn Rate (%)']
    
    # Create pivot table for heatmap
    pivot_combo = combo_churn.pivot(index=service1, columns=service2, values='Churn Rate (%)')
    
    # Plot heatmap
    fig = px.imshow(pivot_combo, text_auto=True, aspect="auto",
                   title=f'Churn Rate (%) by {service1} and {service2} Combination',
                   color_continuous_scale='YlOrRd')
    fig.update_layout(xaxis_title=service2, yaxis_title=service1)
    st.plotly_chart(fig, use_container_width=True)
    
    # Insights
    st.markdown("""
    <div class='insight-text'>
    <h3>Key Insights - Services</h3>
    <ul>
        <li>Online Security and Tech Support services show the strongest protective effect against churn</li>
        <li>Fiber optic internet customers have higher churn rates despite the premium service</li>
        <li>Customers with multiple services (bundling) tend to have lower churn rates</li>
        <li>The combination of no online security and fiber optic internet represents a particularly high-risk segment</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# Contract & Charges Analysis Page
def contract_charges_analysis(df):
    st.markdown("<h2 class='sub-header'>Contract & Charges Analysis</h2>", unsafe_allow_html=True)
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        contract_filter = st.multiselect("Filter by Contract Type", options=df['Contract'].unique(), 
                                        default=df['Contract'].unique())
    with col2:
        payment_filter = st.multiselect("Filter by Payment Method", options=df['PaymentMethod'].unique(), 
                                       default=df['PaymentMethod'].unique())
    
    # Apply filters
    filtered_df = df[(df['Contract'].isin(contract_filter)) & (df['PaymentMethod'].isin(payment_filter))]
    
    # Contract and payment distribution
    st.markdown("<h3>Contract and Payment Distribution</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Contract distribution
        fig = px.pie(filtered_df, names='Contract', title='Contract Type Distribution',
                    color_discrete_sequence=px.colors.qualitative.Set1)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Payment method distribution
        fig = px.pie(filtered_df, names='PaymentMethod', title='Payment Method Distribution',
                    color_discrete_sequence=px.colors.qualitative.Pastel)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    # Contract impact on churn
    st.markdown("<h3 class='sub-header'>Contract Impact on Churn</h3>", unsafe_allow_html=True)
    
    # Create contract impact chart
    contract_churn = df.groupby('Contract')['Churn'].apply(
        lambda x: (x == 'Yes').mean() * 100).reset_index()
    contract_churn.columns = ['Contract', 'Churn Rate (%)']
    
    fig = px.bar(contract_churn, x='Contract', y='Churn Rate (%)',
                title="Contract Type Impact on Churn",
                color='Churn Rate (%)', color_continuous_scale='Reds')
    st.plotly_chart(fig, use_container_width=True)
    
    # Payment method impact on churn
    st.markdown("<h3 class='sub-header'>Payment Method Impact on Churn</h3>", unsafe_allow_html=True)
    
    # Create payment method impact chart
    payment_churn = df.groupby('PaymentMethod')['Churn'].apply(
        lambda x: (x == 'Yes').mean() * 100).reset_index()
    payment_churn.columns = ['Payment Method', 'Churn Rate (%)']
    
    fig = px.bar(payment_churn, x='Payment Method', y='Churn Rate (%)',
                title="Payment Method Impact on Churn",
                color='Churn Rate (%)', color_continuous_scale='Blues')
    st.plotly_chart(fig, use_container_width=True)
    
    # Charges analysis
    st.markdown("<h3 class='sub-header'>Charges Analysis</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Monthly charges distribution
        fig = px.histogram(filtered_df, x='MonthlyCharges', color='Churn',
                          title='Monthly Charges Distribution by Churn Status',
                          color_discrete_sequence=['#3498db', '#e74c3c'],
                          marginal='box')
        fig.update_layout(xaxis_title='Monthly Charges ($)', yaxis_title='Count')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Total charges distribution
        fig = px.histogram(filtered_df, x='TotalCharges', color='Churn',
                          title='Total Charges Distribution by Churn Status',
                          color_discrete_sequence=['#3498db', '#e74c3c'],
                          marginal='box')
        fig.update_layout(xaxis_title='Total Charges ($)', yaxis_title='Count')
        st.plotly_chart(fig, use_container_width=True)
    
    # Contract and charges combined analysis
    st.markdown("<h3 class='sub-header'>Contract and Charges Combined Analysis</h3>", unsafe_allow_html=True)
    
    # Create contract and charges combined chart
    df['charges_group'] = pd.cut(df['MonthlyCharges'], bins=[0, 40, 80, 120], 
                                labels=['Low', 'Medium', 'High'])
    contract_charges_churn = df.groupby(['Contract', 'charges_group'])['Churn'].apply(
        lambda x: (x == 'Yes').mean() * 100).reset_index()
    contract_charges_churn.columns = ['Contract', 'Monthly Charges', 'Churn Rate (%)']
    
    fig = px.scatter(contract_charges_churn, x='Contract', y='Churn Rate (%)',
                    color='Monthly Charges', size='Churn Rate (%)',
                    title="Churn Rate by Contract Type and Monthly Charges")
    st.plotly_chart(fig, use_container_width=True)
    
    # Interactive scatter plot
    st.markdown("<h3>Interactive Charges vs. Tenure Analysis</h3>", unsafe_allow_html=True)
    
    fig = px.scatter(filtered_df, x='tenure', y='MonthlyCharges', color='Churn', 
                    size='TotalCharges', hover_name='Contract',
                    hover_data=['PaymentMethod', 'InternetService'],
                    title='Monthly Charges vs. Tenure by Churn Status',
                    color_discrete_sequence=['#3498db', '#e74c3c'])
    fig.update_layout(xaxis_title='Tenure (months)', yaxis_title='Monthly Charges ($)')
    st.plotly_chart(fig, use_container_width=True)
    
    # Insights
    st.markdown("""
    <div class='insight-text'>
    <h3>Key Insights - Contract & Charges</h3>
    <ul>
        <li>Contract type is the strongest predictor of churn, with month-to-month contracts showing a 42.71% churn rate compared to just 2.83% for two-year contracts</li>
        <li>Electronic check payment method is associated with significantly higher churn rates (45.29%) compared to automatic payment methods (15-17%)</li>
        <li>Higher monthly charges correlate with increased churn risk, especially for customers with shorter tenure</li>
        <li>The combination of month-to-month contracts and high monthly charges represents the highest risk segment</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# Churn Prediction Page
def churn_prediction(df):
    st.markdown("<h2 class='sub-header'>Churn Prediction Factors</h2>", unsafe_allow_html=True)
    
    # Feature importance visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        # Create categorical feature importance chart
        categorical_features = ['Contract', 'PaymentMethod', 'InternetService', 'OnlineSecurity', 'TechSupport']
        cat_importance = []
        for feature in categorical_features:
            importance = df.groupby(feature)['Churn'].apply(
                lambda x: (x == 'Yes').mean() * 100).max()
            cat_importance.append({'Feature': feature, 'Importance': importance})
        
        cat_importance_df = pd.DataFrame(cat_importance)
        fig = px.bar(cat_importance_df, x='Feature', y='Importance',
                    title="Categorical Features Importance",
                    color='Importance', color_continuous_scale='Reds')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Create numerical feature importance chart
        numerical_features = ['tenure', 'MonthlyCharges', 'TotalCharges']
        num_importance = []
        for feature in numerical_features:
            # Calculate correlation with churn
            correlation = df[feature].corr(df['Churn'].map({'Yes': 1, 'No': 0}))
            num_importance.append({'Feature': feature, 'Correlation': abs(correlation)})
        
        num_importance_df = pd.DataFrame(num_importance)
        fig = px.bar(num_importance_df, x='Feature', y='Correlation',
                    title="Numerical Features Importance",
                    color='Correlation', color_continuous_scale='Blues')
        st.plotly_chart(fig, use_container_width=True)
    
    # Interactive churn probability calculator
    st.markdown("<h3 class='sub-header'>Interactive Churn Risk Calculator</h3>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='insight-text'>
    <p>This interactive tool estimates churn risk based on key customer attributes. 
    Adjust the parameters below to see how different factors affect churn probability.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create columns for input parameters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        contract = st.selectbox("Contract Type", options=['Month-to-month', 'One year', 'Two year'])
        internet = st.selectbox("Internet Service", options=['DSL', 'Fiber optic', 'No'])
        security = st.selectbox("Online Security", options=['Yes', 'No', 'No internet service'])
    
    with col2:
        tech_support = st.selectbox("Tech Support", options=['Yes', 'No', 'No internet service'])
        payment = st.selectbox("Payment Method", options=['Electronic check', 'Mailed check', 
                                                        'Bank transfer (automatic)', 'Credit card (automatic)'])
        paperless = st.selectbox("Paperless Billing", options=['Yes', 'No'])
    
    with col3:
        tenure = st.slider("Tenure (months)", min_value=0, max_value=72, value=12)
        monthly_charges = st.slider("Monthly Charges ($)", min_value=18, max_value=120, value=70)
        senior = st.selectbox("Senior Citizen", options=['No', 'Yes'])
    
    # Calculate estimated churn probability based on selected parameters
    # This is a simplified model based on the analysis findings
    
    # Base probability
    churn_prob = 26.54  # Overall churn rate
    
    # Contract adjustment (strongest factor)
    if contract == 'Month-to-month':
        churn_prob *= 1.6  # Increase probability
    elif contract == 'One year':
        churn_prob *= 0.42  # Decrease probability
    elif contract == 'Two year':
        churn_prob *= 0.11  # Decrease probability significantly
    
    # Tenure adjustment
    if tenure < 12:
        churn_prob *= 1.8  # Increase probability for new customers
    elif tenure > 40:
        churn_prob *= 0.4  # Decrease probability for long-term customers
    
    # Internet service adjustment
    if internet == 'Fiber optic':
        churn_prob *= 1.5  # Increase probability
    elif internet == 'No':
        churn_prob *= 0.3  # Decrease probability significantly
    
    # Security and support adjustment
    if security == 'No' and internet != 'No internet service':
        churn_prob *= 1.3  # Increase probability
    if tech_support == 'No' and internet != 'No internet service':
        churn_prob *= 1.3  # Increase probability
    
    # Payment method adjustment
    if payment == 'Electronic check':
        churn_prob *= 1.4  # Increase probability
    elif payment in ['Bank transfer (automatic)', 'Credit card (automatic)']:
        churn_prob *= 0.7  # Decrease probability
    
    # Monthly charges adjustment
    if monthly_charges > 80:
        churn_prob *= 1.3  # Increase probability for high charges
    elif monthly_charges < 40:
        churn_prob *= 0.7  # Decrease probability for low charges
    
    # Senior citizen adjustment
    if senior == 'Yes':
        churn_prob *= 1.2  # Slight increase in probability
    
    # Paperless billing adjustment
    if paperless == 'Yes':
        churn_prob *= 1.1  # Slight increase in probability
    
    # Cap probability between 1% and 99%
    churn_prob = max(1, min(99, churn_prob))
    
    # Display the estimated churn probability
    st.markdown("<h3>Estimated Churn Probability</h3>", unsafe_allow_html=True)
    
    # Create a gauge chart for churn probability
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = churn_prob,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Churn Probability (%)"},
        gauge = {
            'axis': {'range': [0, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 20], 'color': "green"},
                {'range': [20, 40], 'color': "yellow"},
                {'range': [40, 60], 'color': "orange"},
                {'range': [60, 100], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': churn_prob
            }
        }
    ))
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Risk category
    risk_category = ""
    if churn_prob < 20:
        risk_category = "Low Risk"
    elif churn_prob < 40:
        risk_category = "Moderate Risk"
    elif churn_prob < 60:
        risk_category = "High Risk"
    else:
        risk_category = "Very High Risk"
    
    st.markdown(f"""
    <div class='insight-text'>
    <h3>Risk Assessment: {risk_category}</h3>
    <p>Based on the selected parameters, this customer profile has a {churn_prob:.1f}% probability of churning, 
    which is categorized as {risk_category}.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Recommendations based on risk level
    st.markdown("<h3 class='sub-header'>Recommended Retention Strategies</h3>", unsafe_allow_html=True)
    
    if risk_category == "Low Risk":
        st.markdown("""
        <div class='recommendation-card'>
        <h4>Recommended Approach for Low Risk Customers:</h4>
        <ul>
            <li>Maintain current service quality and relationship</li>
            <li>Consider upselling additional services</li>
            <li>Implement loyalty rewards program</li>
            <li>Gather feedback to understand what's working well</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    elif risk_category == "Moderate Risk":
        st.markdown("""
        <div class='recommendation-card'>
        <h4>Recommended Approach for Moderate Risk Customers:</h4>
        <ul>
            <li>Proactive check-ins to address any emerging issues</li>
            <li>Offer service upgrades or bundle discounts</li>
            <li>Provide educational resources about service benefits</li>
            <li>Consider contract extension incentives</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    elif risk_category == "High Risk":
        st.markdown("""
        <div class='recommendation-card'>
        <h4>Recommended Approach for High Risk Customers:</h4>
        <ul>
            <li>Immediate outreach to address potential issues</li>
            <li>Offer significant discounts for contract extensions</li>
            <li>Provide free trials of security and support services</li>
            <li>Consider personalized retention offers</li>
            <li>Implement regular satisfaction check-ins</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    else:  # Very High Risk
        st.markdown("""
        <div class='recommendation-card'>
        <h4>Recommended Approach for Very High Risk Customers:</h4>
        <ul>
            <li>Urgent intervention with dedicated retention specialist</li>
            <li>Offer substantial discounts or contract restructuring</li>
            <li>Provide complimentary service upgrades</li>
            <li>Address specific pain points with customized solutions</li>
            <li>Consider win-back strategies if preventive measures fail</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

# Recommendations Page
def recommendations():
    st.markdown("<h2 class='sub-header'>Recommendations</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='insight-text'>
    <p>Based on the comprehensive analysis of customer churn patterns, the following recommendations 
    are provided to reduce customer attrition and increase retention.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Recommendation 1
    st.markdown("""
    <div class='recommendation-card'>
    <h3>1. Target High-Risk Segments</h3>
    <p>Focus retention efforts on the segments with the highest churn probability.</p>
    <h4>Action Items:</h4>
    <ul>
        <li>Develop special offers for new customers with high monthly charges</li>
        <li>Create targeted retention campaigns for month-to-month customers</li>
        <li>Implement early intervention for customers showing signs of dissatisfaction</li>
    </ul>
    <h4>Expected Impact:</h4>
    <p>Targeting the highest-risk segments could potentially reduce overall churn by 15-20% 
    by addressing the most vulnerable customer groups.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Recommendation 2
    st.markdown("""
    <div class='recommendation-card'>
    <h3>2. Promote Longer-Term Contracts</h3>
    <p>Encourage customers to switch from month-to-month to longer-term contracts.</p>
    <h4>Action Items:</h4>
    <ul>
        <li>Offer incentives for contract upgrades (discounted rates, free premium services)</li>
        <li>Implement graduated discounts that increase with contract length</li>
        <li>Create compelling bundle offers exclusive to long-term contracts</li>
    </ul>
    <h4>Expected Impact:</h4>
    <p>Converting just 20% of month-to-month customers to annual contracts could reduce 
    overall churn by approximately 7-10%.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Recommendation 3
    st.markdown("""
    <div class='recommendation-card'>
    <h3>3. Enhance Value of Security & Support Services</h3>
    <p>Increase adoption of services that correlate with lower churn rates.</p>
    <h4>Action Items:</h4>
    <ul>
        <li>Offer free trial periods for online security and technical support</li>
        <li>Bundle these services into popular packages</li>
        <li>Educate customers about the benefits through targeted communications</li>
    </ul>
    <h4>Expected Impact:</h4>
    <p>Increasing security and support service adoption by 25% could reduce churn by 
    approximately 5-8% among internet service customers.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Recommendation 4
    st.markdown("""
    <div class='recommendation-card'>
    <h3>4. Optimize Payment Methods</h3>
    <p>Encourage adoption of automatic payment methods which show lower churn rates.</p>
    <h4>Action Items:</h4>
    <ul>
        <li>Offer small discounts for switching to automatic payments</li>
        <li>Simplify the setup process for automatic payments</li>
        <li>Highlight the convenience benefits in customer communications</li>
    </ul>
    <h4>Expected Impact:</h4>
    <p>Converting 30% of electronic check customers to automatic payment methods could 
    reduce overall churn by approximately 3-5%.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Recommendation 5
    st.markdown("""
    <div class='recommendation-card'>
    <h3>5. Enhance First-Year Customer Experience</h3>
    <p>Create a specialized onboarding and first-year experience program.</p>
    <h4>Action Items:</h4>
    <ul>
        <li>Personalized welcome and setup assistance</li>
        <li>Regular check-ins during the first 3-6 months</li>
        <li>Educational resources to maximize service value</li>
        <li>Early renewal incentives before the end of promotional periods</li>
    </ul>
    <h4>Expected Impact:</h4>
    <p>Improving the first-year experience could reduce churn among new customers by 
    20-25%, significantly impacting overall retention rates.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Implementation roadmap
    st.markdown("<h3 class='sub-header'>Implementation Roadmap</h3>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='insight-text'>
    <h4>Phase 1: Immediate Actions (1-3 months)</h4>
    <ul>
        <li>Implement targeted retention campaigns for highest-risk segments</li>
        <li>Launch automatic payment incentive program</li>
        <li>Begin first-year experience program development</li>
    </ul>
    
    <h4>Phase 2: Medium-Term Initiatives (3-6 months)</h4>
    <ul>
        <li>Roll out contract upgrade incentives</li>
        <li>Launch security and support services promotion</li>
        <li>Implement first-year experience program</li>
    </ul>
    
    <h4>Phase 3: Long-Term Strategies (6-12 months)</h4>
    <ul>
        <li>Develop predictive churn models for proactive intervention</li>
        <li>Implement comprehensive loyalty program</li>
        <li>Review and optimize pricing structures</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Expected outcomes
    st.markdown("<h3 class='sub-header'>Expected Outcomes</h3>", unsafe_allow_html=True)
    
    # Create metrics for expected outcomes
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Potential Churn Reduction", "30-40%", "↓")
    
    with col2:
        st.metric("Customer Lifetime Value Increase", "15-25%", "↑")
    
    with col3:
        st.metric("ROI on Retention Initiatives", "300-400%", "↑")

# Run the app
if __name__ == "__main__":
    main()

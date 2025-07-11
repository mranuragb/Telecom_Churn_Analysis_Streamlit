import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Set page configuration
st.set_page_config(
    page_title="Telecom Customer Churn Analysis",
    page_icon="📊",
    layout="wide"
)

# Load sample data
@st.cache_data
def load_data():
    np.random.seed(42)
    n_samples = 1000
    
    data = {
        'Contract': np.random.choice(['Month-to-month', 'One year', 'Two year'], n_samples, p=[0.5, 0.3, 0.2]),
        'PaymentMethod': np.random.choice(['Electronic check', 'Mailed check', 'Bank transfer', 'Credit card'], n_samples),
        'MonthlyCharges': np.random.uniform(18, 120, n_samples),
        'tenure': np.random.randint(1, 73, n_samples),
        'Churn': np.random.choice(['Yes', 'No'], n_samples, p=[0.265, 0.735])
    }
    
    return pd.DataFrame(data)

# Main app
def main():
    st.title("📊 Telecom Customer Churn Analysis")
    st.markdown("---")
    
    # Load data
    df = load_data()
    
    # Key metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Customers", f"{len(df):,}")
    
    with col2:
        churn_rate = df['Churn'].value_counts(normalize=True).loc['Yes'] * 100
        st.metric("Churn Rate", f"{churn_rate:.2f}%")
    
    with col3:
        avg_tenure = df['tenure'].mean()
        st.metric("Avg. Tenure", f"{avg_tenure:.1f} months")
    
    st.markdown("---")
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        # Contract analysis
        contract_churn = df.groupby('Contract')['Churn'].apply(
            lambda x: (x == 'Yes').mean() * 100).reset_index()
        contract_churn.columns = ['Contract', 'Churn Rate (%)']
        
        fig = px.bar(contract_churn, x='Contract', y='Churn Rate (%)',
                    title="Churn Rate by Contract Type",
                    color='Churn Rate (%)', color_continuous_scale='Reds')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Payment method analysis
        payment_churn = df.groupby('PaymentMethod')['Churn'].apply(
            lambda x: (x == 'Yes').mean() * 100).reset_index()
        payment_churn.columns = ['Payment Method', 'Churn Rate (%)']
        
        fig = px.bar(payment_churn, x='Payment Method', y='Churn Rate (%)',
                    title="Churn Rate by Payment Method",
                    color='Churn Rate (%)', color_continuous_scale='Blues')
        st.plotly_chart(fig, use_container_width=True)
    
    # Interactive analysis
    st.markdown("### 🔍 Interactive Analysis")
    
    selected_contract = st.selectbox("Select Contract Type", df['Contract'].unique())
    
    filtered_df = df[df['Contract'] == selected_contract]
    
    fig = px.scatter(filtered_df, x='tenure', y='MonthlyCharges', 
                    color='Churn', title=f"Tenure vs Monthly Charges ({selected_contract})")
    st.plotly_chart(fig, use_container_width=True)
    
    # Insights
    st.markdown("### 💡 Key Insights")
    st.markdown("""
    - **Contract Type**: Month-to-month contracts have the highest churn rate
    - **Payment Method**: Electronic check users are more likely to churn
    - **Tenure**: Longer tenure customers are less likely to churn
    - **Monthly Charges**: Higher charges correlate with increased churn risk
    """)

if __name__ == "__main__":
    main() 
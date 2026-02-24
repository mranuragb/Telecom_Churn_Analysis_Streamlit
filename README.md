# Telecom Customer Churn Analysis Dashboard

This is an interactive Streamlit dashboard that analyzes telecom customer churn patterns and provides insights for retention strategies.

## Features

- **Executive Summary**: Overall churn metrics and key insights
- **Customer Demographics**: Analysis of demographic factors' impact on churn
- **Service Analysis**: Effect of different services on customer retention
- **Contract & Charges**: Analysis of contract types and payment methods
- **Churn Prediction**: Interactive churn risk calculator
- **Recommendations**: Data-driven retention strategies

## Installation

1. **Install Dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the App:**
```bash
streamlit run main.py
cd E:\Streamlit\teleco
streamlit run main.py
```

## Data

The app automatically generates sample data if the original dataset is not found. For real data analysis, place the `churn_dataset.csv` file in the project directory.

## Usage

1. Navigate to `http://localhost:8501` in your browser
2. Select different sections from the sidebar
3. Use interactive filters to explore the data
4. Adjust parameters in the churn prediction calculator

## Key Insights

- Contract type is the strongest predictor of churn
- Month-to-month contracts have the highest churn rate (42.71%)
- Long-term contracts have the lowest churn rate (2.83%)
- Online security and tech support services reduce churn
- Electronic check payment method has the highest churn rate

## Technical Details

- **Framework**: Streamlit
- **Visualization**: Plotly
- **Data Processing**: Pandas, NumPy
- **Styling**: Custom CSS

## Troubleshooting

If you encounter any errors:
1. Check if all dependencies are installed
2. Use Python version 3.8+
3. Use a virtual environment
4. Make sure you're in the correct directory when running the app

## Project Structure

```
teleco/
├── main.py              # Main Streamlit application
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── churn_dataset.csv   # Data file (optional)
```

## Contributing

Feel free to contribute to this project by:
- Adding new visualizations
- Improving the prediction model
- Enhancing the UI/UX
- Adding new analysis features

```bash
git remote add origin https://github.com/mranuragb/telecom-churn-analysis.git
git push -u origin main
```
### IMAGES

<img width="1825" height="840" alt="image" src="https://github.com/user-attachments/assets/da75b3fc-6967-4550-b9be-907f73cf52ed" />
<img width="1835" height="895" alt="image" src="https://github.com/user-attachments/assets/3417703c-2482-4ef9-9045-5cd90a3af9b8" />
<img width="1852" height="898" alt="image" src="https://github.com/user-attachments/assets/c10a2f1e-8ce4-40e4-b8e8-2d7ee86db09b" />



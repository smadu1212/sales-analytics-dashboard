# 📊 Sales Analytics Dashboard

A beginner-friendly, interactive sales dashboard built with **Python**, **Streamlit**, **Pandas**, and **Plotly**. Includes fictional sample sales data for demonstration.

## Features
- Revenue, profit, order count and units sold KPIs
- Monthly sales trend, category comparison and top products charts
- Date and category filters
- Upload your own CSV and download filtered results
- Currency label customization (default: Rs.)

## Quick start (Windows)
Install Python 3.10+ and open a terminal in this folder.

```powershell
py -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m streamlit run app.py
```

Open the local URL displayed in the terminal (usually http://localhost:8501).

## CSV format
Your CSV must include these columns:

`Date,Order_ID,Product,Category,Quantity,Unit_Price,Unit_Cost`

Example:

```csv
Date,Order_ID,Product,Category,Quantity,Unit_Price,Unit_Cost
2026-01-05,ORD001,Rice,Groceries,2,350,270
```

- `Date`: a parseable date, preferably YYYY-MM-DD.
- `Quantity`: positive number.
- `Unit_Price` and `Unit_Cost`: non-negative values in the same currency.
- `Order_ID`: may appear on multiple rows for an order containing multiple products.
- `Sales = Quantity × Unit_Price`; `Profit = Quantity × (Unit_Price − Unit_Cost)` (gross profit before overheads/taxes).

## Repository structure
```text
sales-analytics-dashboard/
├── app.py
├── data/
│   └── sample_sales.csv
├── requirements.txt
├── .gitignore
└── README.md
```

## Publish on GitHub
1. Create a new public repository named `sales-analytics-dashboard` (do not initialize it with a README).
2. In the project folder, run:

```powershell
git init
git add .
git commit -m "Initial commit: sales analytics dashboard"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/sales-analytics-dashboard.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username. Authenticate when prompted. Never commit passwords, tokens, customer information or private sales data.

## Notes
- Data is fictional and is for learning/demo purposes.
- Dashboard is a local app and does not store uploaded data in a database.
- Changing the currency symbol only changes the label, not exchange rates.

## License
MIT — see LICENSE.

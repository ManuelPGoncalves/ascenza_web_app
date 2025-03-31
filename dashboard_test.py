import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

# Load dataset
df = pd.read_excel('CasoPrático_RecrutamentoFev2025.xlsx',sheet_name='DB')

# Ensure "Period/Year" is a string
df["Period/Year"] = df["Period/Year"].astype(str)

# Extract month and year, pad months if needed
df["Month"] = df["Period/Year"].str.split('.').str[0].str.zfill(2).astype(int)  # First part before the dot, padded to 2 digits
df["Year"] = df["Period/Year"].str.split('.').str[1].astype(int)  # Second part after the dot (the year)

# Create a proper Date column (assuming the first day of each month)
df["Date"] = pd.to_datetime(df["Year"].astype(str) + "-" + df["Month"].astype(str) + "-01")

# Initialize Dash app
app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("Sales Dashboard", style={"textAlign": "center"}),
    
    html.H2("General Sales Analysis", style={"textAlign": "center"}),
    
    html.Div([
        html.Div([
            html.H4("Top 10 Products"),
            dcc.Graph(id="top_10_products")
        ], className="six columns"),
        html.Div([
            html.H4("Bottom 10 Products"),
            dcc.Graph(id="bottom_10_products")
        ], className="six columns"),
    ], className="row"),
    
    html.Div([
        html.Div([
            html.H4("Top 10 Clients"),
            dcc.Graph(id="top_10_clients")
        ], className="six columns"),
        html.Div([
            html.H4("Bottom 10 Clients"),
            dcc.Graph(id="bottom_10_clients")
        ], className="six columns"),
    ], className="row"),
    
    html.H2("Sales Evolution by Region", style={"textAlign": "center"}),
    dcc.Graph(id="sales_evolution_region"),
    
    html.H2("Company-Specific Analysis", style={"textAlign": "center"}),
    
    html.Div([
        html.Label("Select Company:"),
        dcc.Dropdown(
            id="company_dropdown",
            options=[{"label": company, "value": company} for company in df["Company"].unique()],
            multi=False,
            placeholder="Select a company",
        ),
    ], style={"width": "50%", "margin": "auto"}),
    
    html.Div([
        html.Div([
            html.H4("Top 10 Products (Company-Specific)"),
            dcc.Graph(id="top_10_products_company")
        ], className="six columns"),
        html.Div([
            html.H4("Bottom 10 Products (Company-Specific)"),
            dcc.Graph(id="bottom_10_products_company")
        ], className="six columns"),
    ], className="row"),
    
    html.Div([
        html.Div([
            html.H4("Top 10 Clients (Company-Specific)"),
            dcc.Graph(id="top_10_clients_company")
        ], className="six columns"),
        html.Div([
            html.H4("Bottom 10 Clients (Company-Specific)"),
            dcc.Graph(id="bottom_10_clients_company")
        ], className="six columns"),
    ], className="row"),
])

# Callbacks for updating graphs
@app.callback(
    [Output("top_10_products", "figure"),
     Output("bottom_10_products", "figure"),
     Output("top_10_clients", "figure"),
     Output("bottom_10_clients", "figure"),
     Output("sales_evolution_region", "figure"),
     Output("top_10_products_company", "figure"),
     Output("bottom_10_products_company", "figure"),
     Output("top_10_clients_company", "figure"),
     Output("bottom_10_clients_company", "figure")],
    [Input("company_dropdown", "value")]
)
def update_graphs(selected_company):
    # General analysis (entire dataset)
    top_10_products = df.groupby("Product")["Net Sales"].sum().nlargest(10)
    bottom_10_products = df.groupby("Product")["Net Sales"].sum().nsmallest(10)
    top_10_clients = df.groupby("Customer")["Net Sales"].sum().nlargest(10)
    bottom_10_clients = df.groupby("Customer")["Net Sales"].sum().nsmallest(10)
    
    top_10_products_fig = px.bar(top_10_products, x=top_10_products.index, y=top_10_products.values, title="Top 10 Products")
    bottom_10_products_fig = px.bar(bottom_10_products, x=bottom_10_products.index, y=bottom_10_products.values, title="Bottom 10 Products")
    top_10_clients_fig = px.bar(top_10_clients, x=top_10_clients.index, y=top_10_clients.values, title="Top 10 Clients")
    bottom_10_clients_fig = px.bar(bottom_10_clients, x=bottom_10_clients.index, y=bottom_10_clients.values, title="Bottom 10 Clients")
    
    sales_evolution_fig = px.line(df.groupby(["Year", "Region"])["Net Sales"].sum().reset_index(), 
                                  x="Year", y="Net Sales", color="Region", title="Sales Evolution by Region")
    
    # Company-specific analysis
    if selected_company:
        df_company = df[df["Company"] == selected_company]
        top_10_products_company = df_company.groupby("Product")["Net Sales"].sum().nlargest(10)
        bottom_10_products_company = df_company.groupby("Product")["Net Sales"].sum().nsmallest(10)
        top_10_clients_company = df_company.groupby("Customer")["Net Sales"].sum().nlargest(10)
        bottom_10_clients_company = df_company.groupby("Customer")["Net Sales"].sum().nsmallest(10)
        
        top_10_products_company_fig = px.bar(top_10_products_company, x=top_10_products_company.index, y=top_10_products_company.values, title="Top 10 Products (Company)")
        bottom_10_products_company_fig = px.bar(bottom_10_products_company, x=bottom_10_products_company.index, y=bottom_10_products_company.values, title="Bottom 10 Products (Company)")
        top_10_clients_company_fig = px.bar(top_10_clients_company, x=top_10_clients_company.index, y=top_10_clients_company.values, title="Top 10 Clients (Company)")
        bottom_10_clients_company_fig = px.bar(bottom_10_clients_company, x=bottom_10_clients_company.index, y=bottom_10_clients_company.values, title="Bottom 10 Clients (Company)")
    else:
        top_10_products_company_fig = bottom_10_products_company_fig = top_10_clients_company_fig = bottom_10_clients_company_fig = px.bar(title="Select a Company")
    
    return (top_10_products_fig, bottom_10_products_fig, top_10_clients_fig, bottom_10_clients_fig,
            sales_evolution_fig, top_10_products_company_fig, bottom_10_products_company_fig, 
            top_10_clients_company_fig, bottom_10_clients_company_fig)

# if __name__ == "__main__":
#     app.run(debug=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))  # Get port from environment variable
    app.run(host="0.0.0.0", port=port, debug=False)

import dash
from dash import html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import requests

# Token y URL de la API
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUxMzI5OTA2LCJpYXQiOjE3NTEzMjYzMDYsImp0aSI6ImY1NTk5ODM4OTQ1NDQ2NTBhODZkMWI0OGYyZjE4NWY1IiwidXNlcl9pZCI6MX0.jzVsxYLEImFod5b8vFt3hywo3vZ4yfKk6KzBwj3FilY"
url = "http://127.0.0.1:8000/api/orders/all/"
headers = {"Authorization": f"Bearer {TOKEN}"}

# Obtener datos de la API
response = requests.get(url, headers=headers)
orders = response.json()

# Validar y filtrar órdenes válidas
valid_orders = [
    o for o in orders if "ordered_at" in o and "total" in o and isinstance(o.get("user"), dict)
]
if not valid_orders:
    raise ValueError("No hay órdenes válidas con 'ordered_at', 'total' o 'user'")

# Crear DataFrame base
df = pd.DataFrame(valid_orders)
df["ordered_at"] = pd.to_datetime(df["ordered_at"])
df["date"] = df["ordered_at"].dt.date
df["total"] = df["total"].astype(float)
df["username"] = df["user"].apply(lambda u: u.get("username", "Desconocido"))

# Rango de fechas inicial
min_date = df["date"].min()
max_date = df["date"].max()

# Crear la app
app = dash.Dash(__name__)
app.title = "Dashboard de Órdenes"

app.layout = html.Div([
    html.H1("Análisis de Órdenes", style={"textAlign": "center"}),

    html.Div([
        html.Label("Selecciona un rango de fechas:"),
        dcc.DatePickerRange(
            id="date-range",
            min_date_allowed=min_date,
            max_date_allowed=max_date,
            start_date=min_date,
            end_date=max_date,
            display_format="YYYY-MM-DD"
        )
    ], style={"margin": "20px"}),

    dcc.Graph(id="ventas-dia"),
    dcc.Graph(id="ventas-usuario")
])


@app.callback(
    Output("ventas-dia", "figure"),
    Output("ventas-usuario", "figure"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date"),
)
def update_graphs(start_date, end_date):
    # Filtrar el DataFrame según el rango seleccionado
    mask = (df["date"] >= pd.to_datetime(start_date).date()) & (df["date"] <= pd.to_datetime(end_date).date())
    df_filtrado = df[mask]

    # Agrupar por fecha
    ventas_por_dia = df_filtrado.groupby("date")["total"].sum().reset_index()
    fig_dia = px.line(
        ventas_por_dia,
        x="date",
        y="total",
        title="Total de Ventas por Día",
        markers=True
    )

    # Agrupar por usuario
    ventas_por_usuario = df_filtrado.groupby("username")["total"].sum().reset_index()
    fig_usuario = px.bar(
        ventas_por_usuario,
        x="username",
        y="total",
        title="Total Gastado por Usuario",
        text_auto=True
    )

    return fig_dia, fig_usuario


if __name__ == "__main__":
    app.run(debug=True)

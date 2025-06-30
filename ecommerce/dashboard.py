import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd
import requests

# 🚨 Reemplaza esto con tu token JWT real
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUxMTY0ODIzLCJpYXQiOjE3NTExNjEyMjMsImp0aSI6IjNiZWQxODExNjU1MDQxODM4OTY2ZDI4MGFiNWE5MTdkIiwidXNlcl9pZCI6MX0.97vSw0PEHddSTDsCTQqlxny0ExVn1Q-C3mOzJgpigd0"

# URL del endpoint que devuelve todas las órdenes
url = "http://127.0.0.1:8000/api/orders/all/"
headers = {"Authorization": f"Bearer {TOKEN}"}

response = requests.get(url, headers=headers)
orders = response.json()

# Crear DataFrame y preparar datos
df = pd.DataFrame(orders)
df["ordered_at"] = pd.to_datetime(df["ordered_at"])
df["date"] = df["ordered_at"].dt.date
df["total"] = df["total"].astype(float)

# Ventas totales por día
ventas_por_dia = df.groupby("date")["total"].sum().reset_index()

# Ventas totales por usuario
ventas_por_usuario = df.groupby(df["user"].apply(lambda u: u["username"]))["total"].sum().reset_index()
ventas_por_usuario.columns = ["username", "total"]

# Crear app Dash
app = dash.Dash(__name__)
app.title = "Dashboard de Órdenes"

app.layout = html.Div([
    html.H1("Análisis de Órdenes", style={"textAlign": "center"}),

    dcc.Graph(
        id="ventas-dia",
        figure=px.line(
            ventas_por_dia,
            x="date",
            y="total",
            title="Total de Ventas por Día",
            markers=True
        )
    ),

    dcc.Graph(
        id="ventas-usuario",
        figure=px.bar(
            ventas_por_usuario,
            x="username",
            y="total",
            title="Total Gastado por Usuario",
            text="total"
        )
    )
])

if __name__ == "__main__":
    app.run(debug=True)

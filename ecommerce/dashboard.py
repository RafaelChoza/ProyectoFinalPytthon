import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import requests

# Token de autenticación (reemplázalo con uno válido en producción)
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUxMzc4NzM3LCJpYXQiOjE3NTEyOTIzMzcsImp0aSI6IjIwNTBhMmQyZTc5YTQ0ZWY4NjY5MzAwM2QxNzFlOGY5IiwidXNlcl9pZCI6MX0.QCtb5nOitLpGRwvzJHucE2oy1MVu8QD5pGhVeMM5ZDU"
url = "http://127.0.0.1:8000/api/orders/all/"
headers = {"Authorization": f"Bearer {TOKEN}"}

# Obtener los datos desde la API
response = requests.get(url, headers=headers)
orders = response.json()

# Procesamiento inicial del DataFrame
df = pd.DataFrame(orders)
df["ordered_at"] = pd.to_datetime(df["ordered_at"])
df["date"] = df["ordered_at"].dt.date
df["total"] = df["total"].astype(float)

# Inicializar la app
app = dash.Dash(__name__)
app.title = "Dashboard de Órdenes"

# Layout con selector de fecha
app.layout = html.Div([
    html.H1("Análisis de Órdenes", style={"textAlign": "center"}),

    dcc.DatePickerRange(
        id="rango-fechas",
        start_date=df["date"].min(),
        end_date=df["date"].max(),
        display_format="YYYY-MM-DD",
        style={"margin": "20px auto", "textAlign": "center"}
    ),

    dcc.Graph(id="ventas-dia"),
    dcc.Graph(id="ventas-usuario")
])

# Callback para actualizar gráficos según el rango de fechas
@app.callback(
    [Output("ventas-dia", "figure"), Output("ventas-usuario", "figure")],
    [Input("rango-fechas", "start_date"), Input("rango-fechas", "end_date")]
)
def actualizar_graficas(start_date, end_date):
    if start_date and end_date:
        rango = (pd.to_datetime(df["date"]) >= pd.to_datetime(start_date)) & (pd.to_datetime(df["date"]) <= pd.to_datetime(end_date))
        df_filtrado = df.loc[rango]
    else:
        df_filtrado = df.copy()

    # Total por día
    ventas_por_dia = df_filtrado.groupby("date")["total"].sum().reset_index()

    # Total por usuario
    ventas_por_usuario = df_filtrado.groupby(df_filtrado["user"].apply(lambda u: u["username"]))["total"].sum().reset_index()
    ventas_por_usuario.columns = ["username", "total"]

    fig_dia = px.line(
        ventas_por_dia,
        x="date",
        y="total",
        title="Total de Ventas por Día",
        markers=True
    )

    fig_usuario = px.bar(
        ventas_por_usuario,
        x="username",
        y="total",
        title="Total Gastado por Usuario",
        text="total"
    )

    return fig_dia, fig_usuario

if __name__ == "__main__":
    app.run(debug=True)

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objs as go

texts = {
    "ru": {
        "title": "Модель хищник–жертва",
        "alpha": "α (рост жертв)",
        "beta": "β (поедание)",
        "gamma": "γ (смертность хищников)",
        "delta": "δ (превращение жертв в хищников)",
        "x0": "Начальное число жертв",
        "y0": "Начальное число хищников",
        "T": "Время моделирования",
        "dt": "Шаг времени",
        "prey": "Жертвы",
        "predator": "Хищники",
        "time": "Время",
        "populations_over_time": "Популяции во времени",
        "phase_portrait": "Фазовый портрет",
        "download_csv": "Скачать результаты в CSV",
        "language": "Язык",
        "theme": "Тема",
        "light": "Светлая",
        "dark": "Тёмная",
        "model": "Модель",
        "lotka_volterra": "Классическая Лотка–Вольтерра",
        "logistic_lv": "Логистическая модель с ограничением ресурсов",
    },
    "en": {
        "title": "Predator-Prey Model",
        "alpha": "α (prey growth rate)",
        "beta": "β (predation rate)",
        "gamma": "γ (predator death rate)",
        "delta": "δ (predator reproduction rate)",
        "x0": "Initial prey population",
        "y0": "Initial predator population",
        "T": "Simulation time",
        "dt": "Time step",
        "prey": "Prey",
        "predator": "Predators",
        "time": "Time",
        "populations_over_time": "Populations over time",
        "phase_portrait": "Phase portrait",
        "download_csv": "Download results as CSV",
        "language": "Language",
        "theme": "Theme",
        "light": "Light",
        "dark": "Dark",
        "model": "Model",
        "lotka_volterra": "Classic Lotka–Volterra",
        "logistic_lv": "Logistic model with resource limit",
    },
    "kk": {
        "title": "Jirtqish-jalıwshi modeli",
        "alpha": "α (óljeniń ósiw tezligi)",
        "beta": "β (jirtqishliq tezligi)",
        "gamma": "γ (jirtqish ólim koefficienti)",
        "delta": "δ (jirtqish kóbeyiw tezligi)",
        "x0": "Dáslepki jemtik populyaciyası",
        "y0": "Jirtqishlardın dáslepki sanı",
        "T": "Simulyaciya waqtı",
        "dt": "Waqıt qádemi",
        "prey": "ólje",
        "predator": "Jirtqishlar",
        "time": "Waqit",
        "populations_over_time": "Zamana boyinsha populyaciyalar",
        "phase_portrait": "Faza portreti",
        "download_csv": "CSV túrinde nátiyjelerdi júklep alıw",
        "language": "Til",
        "theme": "Tema",
        "light": "jaqtılıq",
        "dark": "Qarańǵı",
        "model": "Model",
        "lotka_volterra": "Classic Lotka-Volterra",
        "logistic_lv": "Resource limitli logistika modeli",
    }
}

# Выбор языка
lang = st.sidebar.selectbox("🌐 Язык / Language / Til", ["Русский", "English", "Қарақалпақша"])
lang_code = "ru" if lang == "Русский" else ("kk" if lang == "Қарақалпақша" else "en")
t = texts[lang_code]

st.title(t["title"])

# Тема (светлая/тёмная)
theme = st.sidebar.radio(t["theme"], [t["light"], t["dark"]])
is_dark = (theme == t["dark"])

bg_color = "#222222" if is_dark else "white"
fg_color = "white" if is_dark else "black"
prey_color = "cyan" if is_dark else "blue"
predator_color = "orange" if is_dark else "red"

# Выбор модели
model_choice = st.sidebar.selectbox(t["model"], [t["lotka_volterra"], t["logistic_lv"]])

# Параметры
alpha = st.sidebar.number_input(t["alpha"], min_value=0.01, max_value=1.0, value=0.1, step=0.01, format="%.2f")
beta = st.sidebar.number_input(t["beta"], min_value=0.001, max_value=0.1, value=0.02, step=0.001, format="%.3f")
gamma = st.sidebar.number_input(t["gamma"], min_value=0.01, max_value=1.0, value=0.1, step=0.01, format="%.2f")
delta = st.sidebar.number_input(t["delta"], min_value=0.001, max_value=0.1, value=0.01, step=0.001, format="%.3f")
x0 = st.sidebar.number_input(t["x0"], min_value=1.0, max_value=100.0, value=40.0, step=1.0, format="%.0f")
y0 = st.sidebar.number_input(t["y0"], min_value=1.0, max_value=100.0, value=9.0, step=1.0, format="%.0f")
T = st.sidebar.number_input(t["T"], min_value=10.0, max_value=500.0, value=200.0, step=10.0, format="%.0f")
dt = st.sidebar.number_input(t["dt"], min_value=0.01, max_value=1.0, value=0.1, step=0.01, format="%.2f")

time = np.arange(0, T + dt, dt)
x = [x0]
y = [y0]

def lotka_volterra(x, y, a, b, g, d):
    dx = a * x - b * x * y
    dy = d * x * y - g * y
    return dx, dy

def logistic_lv(x, y, a, b, g, d, K=100):
    dx = a * x * (1 - x / K) - b * x * y
    dy = d * x * y - g * y
    return dx, dy

for _ in time[1:]:
    if model_choice == t["lotka_volterra"]:
        dx, dy = lotka_volterra(x[-1], y[-1], alpha, beta, gamma, delta)
    else:
        dx, dy = logistic_lv(x[-1], y[-1], alpha, beta, gamma, delta)
    x.append(x[-1] + dx * dt)
    y.append(y[-1] + dy * dt)

df = pd.DataFrame({
    t["time"]: time,
    t["prey"]: x,
    t["predator"]: y
})

# График популяций во времени
fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=time, y=x, mode='lines', name=t["prey"], line=dict(color=prey_color)))
fig1.add_trace(go.Scatter(x=time, y=y, mode='lines', name=t["predator"], line=dict(color=predator_color)))
fig1.update_layout(
    title=t["populations_over_time"],
    xaxis_title=t["time"],
    yaxis_title="Популяция",
    plot_bgcolor=bg_color,
    paper_bgcolor=bg_color,
    font_color=fg_color
)
st.plotly_chart(fig1, use_container_width=True)

# Фазовый портрет
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=x, y=y, mode='lines', line=dict(color=prey_color)))
fig2.update_layout(
    title=t["phase_portrait"],
    xaxis_title=t["prey"],
    yaxis_title=t["predator"],
    plot_bgcolor=bg_color,
    paper_bgcolor=bg_color,
    font_color=fg_color
)
st.plotly_chart(fig2, use_container_width=True)

# Скачать CSV
csv = df.to_csv(index=False)
st.download_button(
    label=t["download_csv"],
    data=csv,
    file_name='predator_prey_simulation.csv',
    mime='text/csv'
)
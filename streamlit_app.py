import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import os

# ─────────────────────────────────────────────────────────────
# CONFIGURACIÓN GENERAL
# ─────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Entreno",
    page_icon="💪",
    layout="centered",
    initial_sidebar_state="collapsed",
)

DATA_FILE = "data_lagartijas.csv"
OLD_DATA_FILE = "data_entreno.csv"

COLUMNAS = ["Fecha", "Tipo_Ejercicio", "Cantidad", "Peso", "RPE_Esfuerzo"]

TIPO_FLEXIONES = "Flexiones"
TIPO_PLANCHA = "Plancha"
TIPO_PESO = "Peso"
TIPO_DESCANSO = "Día Libre / Sick Day"

TIPOS_RACHA = [TIPO_FLEXIONES, TIPO_PLANCHA, TIPO_DESCANSO]


# ─────────────────────────────────────────────────────────────
# CSS — APPLE FITNESS STYLE
# ─────────────────────────────────────────────────────────────

st.markdown("""
<style>
  :root {
    --bg: #000000;
    --card: #1C1C1E;
    --card-soft: #2C2C2E;
    --text: #FFFFFF;
    --muted: #8E8E93;
    --muted-2: #636366;
    --border: rgba(255, 255, 255, 0.10);

    --pink: #FF2D55;
    --green: #A1FF00;
    --orange: #FF9500;
    --blue: #0A84FF;
    --gray: #3A3A3C;

    --shadow: 0 18px 42px rgba(0, 0, 0, 0.45);
  }

  html, body, [class*="css"] {
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display",
                 "SF Pro Text", Inter, "Helvetica Neue", Arial, sans-serif;
    background: var(--bg) !important;
    color: var(--text) !important;
    -webkit-font-smoothing: antialiased;
  }

  #MainMenu, footer {
    visibility: hidden;
  }

  header {
    visibility: visible !important;
    background: transparent !important;
    height: 3rem !important;
  }

  .stDeployButton {
    display: none;
  }

  [data-testid="stAppViewContainer"] {
    background:
      radial-gradient(circle at 15% 0%, rgba(255, 45, 85, 0.20), transparent 30%),
      radial-gradient(circle at 95% 12%, rgba(161, 255, 0, 0.14), transparent 30%),
      radial-gradient(circle at 50% 100%, rgba(10, 132, 255, 0.10), transparent 34%),
      #000000 !important;
  }

  [data-testid="stHeader"] {
    background: transparent !important;
  }

  [data-testid="collapsedControl"] {
    visibility: visible !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    position: fixed !important;
    top: 14px !important;
    left: 14px !important;
    z-index: 999999 !important;
    width: 46px !important;
    height: 46px !important;
    border-radius: 16px !important;
    background: rgba(28, 28, 30, 0.78) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border: 1px solid var(--border) !important;
    box-shadow: 0 10px 30px rgba(0,0,0,.45) !important;
  }

  [data-testid="collapsedControl"] svg {
    color: #FFFFFF !important;
  }

  [data-testid="stSidebar"] {
    background: rgba(28, 28, 30, 0.96) !important;
    border-right: 1px solid var(--border);
  }

  [data-testid="stSidebar"] * {
    color: var(--text);
  }

  .block-container {
    max-width: 820px;
    padding: 1.2rem 1rem 4rem;
    margin: 0 auto;
  }

  .app-header {
    padding: 24px 4px 18px;
  }

  .eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 0.2px;
    color: var(--green);
    background: rgba(161, 255, 0, 0.12);
    border: 1px solid rgba(161, 255, 0, 0.18);
    border-radius: 999px;
    padding: 7px 11px;
    margin-bottom: 12px;
  }

  .app-header h1 {
    font-size: 44px;
    line-height: 0.95;
    margin: 0;
    letter-spacing: -1.8px;
    color: var(--text);
    font-weight: 900;
  }

  .app-header p {
    margin: 10px 0 0;
    color: var(--muted);
    font-size: 15px;
    line-height: 1.42;
    max-width: 560px;
  }

  .fitness-card {
    background: rgba(28, 28, 30, 0.88);
    backdrop-filter: blur(22px);
    -webkit-backdrop-filter: blur(22px);
    border: 1px solid var(--border);
    border-radius: 24px;
    padding: 22px;
    margin-bottom: 16px;
    box-shadow: var(--shadow);
  }

  .fitness-card-soft {
    background: rgba(44, 44, 46, 0.82);
    border: 1px solid var(--border);
    border-radius: 22px;
    padding: 18px;
    margin-bottom: 14px;
  }

  .card-title {
    font-size: 21px;
    font-weight: 900;
    letter-spacing: -0.5px;
    color: var(--text);
    margin: 0 0 8px;
  }

  .card-subtitle {
    color: var(--muted);
    font-size: 14px;
    line-height: 1.42;
    margin: 0 0 16px;
  }

  .hero-grid {
    display: grid;
    grid-template-columns: 1.1fr 0.9fr;
    gap: 14px;
    margin-bottom: 16px;
  }

  @media (max-width: 760px) {
    .hero-grid {
      grid-template-columns: 1fr;
    }
  }

  .today-panel {
    background:
      linear-gradient(145deg, rgba(255, 45, 85, 0.17), rgba(28, 28, 30, 0.92) 46%),
      rgba(28, 28, 30, 0.92);
    border: 1px solid rgba(255, 45, 85, 0.20);
    border-radius: 28px;
    padding: 22px;
    box-shadow: var(--shadow);
  }

  .rings-panel {
    background:
      linear-gradient(145deg, rgba(161, 255, 0, 0.13), rgba(28, 28, 30, 0.92) 50%),
      rgba(28, 28, 30, 0.92);
    border: 1px solid rgba(161, 255, 0, 0.18);
    border-radius: 28px;
    padding: 22px;
    box-shadow: var(--shadow);
  }

  .panel-label {
    color: var(--muted);
    font-size: 12px;
    font-weight: 850;
    text-transform: uppercase;
    letter-spacing: 0.7px;
    margin-bottom: 8px;
  }

  .today-main {
    font-size: 70px;
    line-height: 0.9;
    font-weight: 950;
    color: var(--text);
    letter-spacing: -4px;
    margin-bottom: 10px;
  }

  .today-sub {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    color: var(--muted);
    font-size: 14px;
    font-weight: 700;
  }

  .pill {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 8px 10px;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid var(--border);
  }

  .pill-pink {
    color: var(--pink);
  }

  .pill-green {
    color: var(--green);
  }

  .pill-orange {
    color: var(--orange);
  }

  .ring-row {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-top: 8px;
  }

  .ring {
    width: 110px;
    height: 110px;
    border-radius: 999px;
    display: grid;
    place-items: center;
    background:
      conic-gradient(var(--ring-color) var(--ring-deg), rgba(255,255,255,0.10) 0deg);
    box-shadow: 0 0 34px rgba(161,255,0,0.10);
  }

  .ring-inner {
    width: 78px;
    height: 78px;
    border-radius: 999px;
    background: #000000;
    display: grid;
    place-items: center;
    border: 1px solid rgba(255,255,255,0.08);
  }

  .ring-value {
    color: var(--text);
    font-weight: 950;
    font-size: 19px;
    letter-spacing: -0.4px;
  }

  .ring-meta {
    flex: 1;
  }

  .ring-title {
    color: var(--text);
    font-size: 18px;
    font-weight: 900;
    letter-spacing: -0.3px;
  }

  .ring-detail {
    color: var(--muted);
    font-size: 13px;
    margin-top: 4px;
    line-height: 1.35;
  }

  .impact-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 16px;
  }

  @media (max-width: 760px) {
    .impact-grid {
      grid-template-columns: repeat(2, 1fr);
    }
  }

  .impact-card {
    background: rgba(28, 28, 30, 0.88);
    border: 1px solid var(--border);
    border-radius: 22px;
    padding: 16px;
    min-height: 112px;
    box-shadow: 0 12px 28px rgba(0,0,0,.35);
  }

  .impact-label {
    color: var(--muted);
    font-size: 12px;
    font-weight: 850;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    margin-bottom: 10px;
  }

  .impact-value {
    color: var(--text);
    font-size: 29px;
    line-height: 1;
    font-weight: 950;
    letter-spacing: -1.1px;
  }

  .impact-detail {
    color: var(--muted);
    font-size: 12px;
    margin-top: 8px;
    font-weight: 700;
    line-height: 1.35;
  }

  .pink-text { color: var(--pink); }
  .green-text { color: var(--green); }
  .orange-text { color: var(--orange); }
  .blue-text { color: var(--blue); }

  .express-card {
    background:
      linear-gradient(135deg, rgba(255, 45, 85, 0.24), rgba(161, 255, 0, 0.10)),
      rgba(28, 28, 30, 0.82);
    border: 1px solid rgba(255, 255, 255, 0.14);
    border-radius: 30px;
    padding: 22px;
    margin-bottom: 16px;
    box-shadow:
      0 18px 42px rgba(0,0,0,.50),
      0 0 42px rgba(255,45,85,.11);
  }

  .express-title {
    font-size: 24px;
    font-weight: 950;
    color: var(--text);
    letter-spacing: -0.8px;
    margin-bottom: 4px;
  }

  .express-sub {
    color: var(--muted);
    font-size: 14px;
    font-weight: 650;
    margin-bottom: 16px;
  }

  .express-button div[data-testid="stButton"] > button {
    width: 100% !important;
    min-height: 76px !important;
    border-radius: 24px !important;
    background:
      linear-gradient(135deg, rgba(255, 45, 85, 0.92), rgba(161, 255, 0, 0.80)) !important;
    color: #FFFFFF !important;
    font-size: 19px !important;
    font-weight: 950 !important;
    letter-spacing: -0.4px !important;
    border: 1px solid rgba(255,255,255,0.22) !important;
    box-shadow:
      0 16px 34px rgba(255,45,85,.24),
      0 0 32px rgba(161,255,0,.12) !important;
  }

  div[data-testid="stButton"] > button {
    border-radius: 18px !important;
    min-height: 54px !important;
    font-size: 16px !important;
    font-weight: 850 !important;
    letter-spacing: -0.25px !important;
    border: 1px solid var(--border) !important;
    background: rgba(58, 58, 60, 0.88) !important;
    color: var(--text) !important;
    transition: transform .08s ease, opacity .12s ease, filter .12s ease !important;
  }

  div[data-testid="stButton"] > button:hover {
    transform: scale(0.985);
    opacity: .94;
    filter: brightness(1.08);
  }

  div[data-testid="stButton"] > button:active {
    transform: scale(0.96);
    opacity: .80;
  }

  .pink-button div[data-testid="stButton"] > button {
    background: var(--pink) !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(255,45,85,0.42) !important;
    box-shadow: 0 14px 28px rgba(255,45,85,.22) !important;
  }

  .green-button div[data-testid="stButton"] > button {
    background: var(--green) !important;
    color: #000000 !important;
    border: 1px solid rgba(161,255,0,0.42) !important;
    box-shadow: 0 14px 28px rgba(161,255,0,.16) !important;
  }

  .orange-button div[data-testid="stButton"] > button {
    background: var(--orange) !important;
    color: #000000 !important;
    border: 1px solid rgba(255,149,0,0.42) !important;
    box-shadow: 0 14px 28px rgba(255,149,0,.18) !important;
  }

  .subtle-button div[data-testid="stButton"] > button {
    background: rgba(58, 58, 60, 0.60) !important;
    color: var(--muted) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    box-shadow: none !important;
  }

  div[data-testid="stNumberInput"] label,
  div[data-testid="stSlider"] label,
  div[data-testid="stSelectbox"] label {
    color: var(--muted) !important;
    font-size: 13px !important;
    font-weight: 800 !important;
  }

  div[data-testid="stNumberInput"] input {
    border-radius: 16px !important;
    border: 1px solid var(--border) !important;
    background: rgba(44, 44, 46, 0.90) !important;
    min-height: 48px !important;
    font-size: 16px !important;
    color: var(--text) !important;
  }

  [data-testid="stTabs"] button {
    border-radius: 999px !important;
    font-weight: 850 !important;
    color: var(--muted) !important;
  }

  [data-testid="stTabs"] [aria-selected="true"] {
    color: var(--green) !important;
  }

  .stSuccess, .stWarning, .stInfo {
    border-radius: 18px !important;
    border: none !important;
  }

  .debt-display {
    background: rgba(255, 149, 0, 0.12);
    border: 1px solid rgba(255, 149, 0, 0.22);
    border-radius: 24px;
    padding: 18px;
    margin-bottom: 16px;
  }

  .debt-main {
    color: var(--orange);
    font-size: 38px;
    font-weight: 950;
    letter-spacing: -1.2px;
    line-height: 1;
  }

  .debt-sub {
    color: var(--muted);
    font-size: 13px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.55px;
    margin-top: 8px;
  }

  .calendar-wrap {
    margin-top: 14px;
  }

  .calendar-grid {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 9px;
  }

  .activity-cell {
    aspect-ratio: 1 / 1;
    border-radius: 14px;
    background: rgba(58, 58, 60, 0.52);
    border: 1px solid rgba(255,255,255,0.06);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    box-shadow: inset 0 0 0 1px rgba(255,255,255,0.02);
  }

  .activity-done {
    background: rgba(161, 255, 0, 0.92);
    border-color: rgba(161, 255, 0, 0.95);
    box-shadow:
      0 0 18px rgba(161, 255, 0, 0.45),
      0 0 34px rgba(161, 255, 0, 0.20);
  }

  .activity-rest {
    background: rgba(255, 149, 0, 0.56);
    border-color: rgba(255, 149, 0, 0.70);
    box-shadow:
      0 0 16px rgba(255, 149, 0, 0.28);
  }

  .activity-today {
    outline: 2px solid var(--pink);
    outline-offset: 2px;
  }

  .activity-day {
    font-size: 15px;
    font-weight: 950;
    color: #FFFFFF;
    line-height: 1;
  }

  .activity-done .activity-day {
    color: #000000;
  }

  .activity-rest .activity-day {
    color: #000000;
  }

  .activity-weekday {
    color: rgba(255,255,255,0.54);
    font-size: 10px;
    font-weight: 850;
    margin-top: 4px;
  }

  .activity-done .activity-weekday,
  .activity-rest .activity-weekday {
    color: rgba(0,0,0,0.62);
  }

  .legend {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    margin-top: 14px;
    color: var(--muted);
    font-size: 13px;
    font-weight: 750;
  }

  .dot {
    display: inline-block;
    width: 10px;
    height: 10px;
    border-radius: 999px;
    margin-right: 6px;
  }

  .dot-green { background: var(--green); box-shadow: 0 0 10px rgba(161,255,0,.65); }
  .dot-orange { background: var(--orange); }
  .dot-gray { background: var(--gray); }

  .dataframe {
    color: white !important;
  }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# FUNCIONES DE DATOS
# ─────────────────────────────────────────────────────────────

def crear_df_vacio() -> pd.DataFrame:
    return pd.DataFrame(columns=COLUMNAS)


def normalizar_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Mantiene integridad del CSV.
    Convierte formatos antiguos al formato actual sin borrar registros.
    """

    if df.empty:
        return crear_df_vacio()

    # Formato actual
    if all(col in df.columns for col in COLUMNAS):
        out = df[COLUMNAS].copy()

    # Formato antiguo: fecha, cantidad
    elif "fecha" in df.columns and "cantidad" in df.columns:
        out = pd.DataFrame({
            "Fecha": df["fecha"],
            "Tipo_Ejercicio": TIPO_FLEXIONES,
            "Cantidad": df["cantidad"],
            "Peso": None,
            "RPE_Esfuerzo": None,
        })

    # Formato antiguo: fecha, lagartijas, plancha_segundos
    elif "fecha" in df.columns and ("lagartijas" in df.columns or "plancha_segundos" in df.columns):
        registros = []

        for _, row in df.iterrows():
            fecha = row.get("fecha", datetime.now().strftime("%Y-%m-%d %H:%M"))

            lagartijas = int(row.get("lagartijas", 0) or 0)
            plancha = int(row.get("plancha_segundos", 0) or 0)

            if lagartijas > 0:
                registros.append({
                    "Fecha": fecha,
                    "Tipo_Ejercicio": TIPO_FLEXIONES,
                    "Cantidad": lagartijas,
                    "Peso": None,
                    "RPE_Esfuerzo": None,
                })

            if plancha > 0:
                registros.append({
                    "Fecha": fecha,
                    "Tipo_Ejercicio": TIPO_PLANCHA,
                    "Cantidad": plancha,
                    "Peso": None,
                    "RPE_Esfuerzo": None,
                })

        out = pd.DataFrame(registros, columns=COLUMNAS)

    else:
        out = crear_df_vacio()

    for col in COLUMNAS:
        if col not in out.columns:
            out[col] = None

    out["Fecha"] = pd.to_datetime(out["Fecha"], errors="coerce")
    out = out.dropna(subset=["Fecha"])

    out["Tipo_Ejercicio"] = out["Tipo_Ejercicio"].astype(str)
    out["Cantidad"] = pd.to_numeric(out["Cantidad"], errors="coerce").fillna(0).astype(int)
    out["Peso"] = pd.to_numeric(out["Peso"], errors="coerce")
    out["RPE_Esfuerzo"] = pd.to_numeric(out["RPE_Esfuerzo"], errors="coerce")

    return out[COLUMNAS]


def guardar_df(df: pd.DataFrame) -> None:
    df = normalizar_df(df)
    df.to_csv(DATA_FILE, index=False)


def cargar_datos() -> pd.DataFrame:
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        return normalizar_df(df)

    if os.path.exists(OLD_DATA_FILE):
        df = pd.read_csv(OLD_DATA_FILE)
        df = normalizar_df(df)
        guardar_df(df)
        return df

    return crear_df_vacio()


def agregar_registro(tipo: str, cantidad: int, peso=None, rpe=None) -> None:
    df = cargar_datos()

    nuevo = pd.DataFrame([{
        "Fecha": datetime.now(),
        "Tipo_Ejercicio": tipo,
        "Cantidad": int(cantidad),
        "Peso": peso,
        "RPE_Esfuerzo": rpe,
    }])

    df = pd.concat([df, nuevo], ignore_index=True)
    guardar_df(df)


def obtener_datos_hoy(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return crear_df_vacio()

    return df[df["Fecha"].dt.date == date.today()].copy()


def total_hoy(df: pd.DataFrame, tipo: str) -> int:
    hoy_df = obtener_datos_hoy(df)

    if hoy_df.empty:
        return 0

    return int(hoy_df.loc[hoy_df["Tipo_Ejercicio"] == tipo, "Cantidad"].sum())


def peso_actual(df: pd.DataFrame):
    if df.empty:
        return None

    pesos = df.dropna(subset=["Peso"]).copy()
    pesos = pesos[pesos["Peso"] > 0]

    if pesos.empty:
        return None

    pesos = pesos.sort_values("Fecha")
    return float(pesos.iloc[-1]["Peso"])


def format_seconds(seconds: int) -> str:
    seconds = int(seconds)

    if seconds < 60:
        return f"{seconds}s"

    minutes, sec = divmod(seconds, 60)

    if minutes < 60:
        return f"{minutes}:{sec:02d}"

    hours, minutes = divmod(minutes, 60)
    return f"{hours}h {minutes}m {sec}s"


def max_historico_diario(df: pd.DataFrame, tipo: str, excluir_hoy: bool = True) -> int:
    if df.empty:
        return 0

    temp = df[df["Tipo_Ejercicio"] == tipo].copy()

    if temp.empty:
        return 0

    if excluir_hoy:
        temp = temp[temp["Fecha"].dt.date != date.today()]

    if temp.empty:
        return 0

    daily = temp.groupby(temp["Fecha"].dt.date)["Cantidad"].sum()

    if daily.empty:
        return 0

    return int(daily.max())


def registrar_ejercicio_con_pr(tipo: str, cantidad: int, peso=None, rpe=None) -> None:
    """
    Guarda el ejercicio y revisa récord personal diario.
    """

    if cantidad <= 0:
        return

    df_antes = cargar_datos()
    record_anterior = max_historico_diario(df_antes, tipo, excluir_hoy=True)
    total_antes_hoy = total_hoy(df_antes, tipo)

    agregar_registro(
        tipo=tipo,
        cantidad=int(cantidad),
        peso=peso,
        rpe=rpe
    )

    total_despues_hoy = total_antes_hoy + int(cantidad)

    if total_despues_hoy > record_anterior:
        if tipo == TIPO_PLANCHA:
            valor = format_seconds(total_despues_hoy)
        else:
            valor = f"{total_despues_hoy} reps"

        st.session_state.pr_messages.append(
            f"¡NUEVO RÉCORD PERSONAL! 🔥 {tipo}: {valor}"
        )
        st.session_state.show_balloons = True


def fechas_activas(df: pd.DataFrame) -> set:
    if df.empty:
        return set()

    temp = df[df["Tipo_Ejercicio"].isin(TIPOS_RACHA)].copy()

    if temp.empty:
        return set()

    temp = temp[
        ((temp["Tipo_Ejercicio"].isin([TIPO_FLEXIONES, TIPO_PLANCHA])) & (temp["Cantidad"] > 0)) |
        (temp["Tipo_Ejercicio"] == TIPO_DESCANSO)
    ]

    return set(temp["Fecha"].dt.date)


def fechas_descanso(df: pd.DataFrame) -> set:
    if df.empty:
        return set()

    temp = df[df["Tipo_Ejercicio"] == TIPO_DESCANSO].copy()

    if temp.empty:
        return set()

    return set(temp["Fecha"].dt.date)


def calcular_racha(df: pd.DataFrame) -> int:
    activas = fechas_activas(df)

    if not activas:
        return 0

    racha = 0
    cursor = date.today()

    while cursor in activas:
        racha += 1
        cursor -= timedelta(days=1)

    return racha


def preparar_progreso_diario(df: pd.DataFrame, tipo: str, dias: int = 14) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()

    desde = date.today() - timedelta(days=dias - 1)

    temp = df[
        (df["Tipo_Ejercicio"] == tipo) &
        (df["Fecha"].dt.date >= desde)
    ].copy()

    if temp.empty:
        return pd.DataFrame()

    temp["Día"] = temp["Fecha"].dt.strftime("%d/%m")

    resumen = temp.groupby("Día", as_index=False)["Cantidad"].sum()
    return resumen.set_index("Día")


def preparar_peso_semanal(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()

    desde = date.today() - timedelta(days=6)

    temp = df[
        (df["Fecha"].dt.date >= desde) &
        (df["Peso"].notna()) &
        (df["Peso"] > 0)
    ].copy()

    if temp.empty:
        return pd.DataFrame()

    temp["Día"] = temp["Fecha"].dt.strftime("%d/%m")
    temp = temp.sort_values("Fecha")

    resumen = temp.groupby("Día", as_index=False)["Peso"].last()
    return resumen.set_index("Día")


def generar_calendario_html(df: pd.DataFrame, dias: int = 35) -> str:
    """
    Calendario visual tipo actividad.
    Se debe renderizar con:
    st.markdown(html_calendario, unsafe_allow_html=True)
    """

    activas = fechas_activas(df)
    descansos = fechas_descanso(df)

    inicio = date.today() - timedelta(days=dias - 1)
    hoy = date.today()

    dias_semana = ["L", "M", "M", "J", "V", "S", "D"]

    html = """
    <div class="calendar-wrap">
      <div class="calendar-grid">
    """

    for i in range(dias):
        d = inicio + timedelta(days=i)

        clases = ["activity-cell"]

        if d in descansos:
            clases.append("activity-rest")
        elif d in activas:
            clases.append("activity-done")

        if d == hoy:
            clases.append("activity-today")

        clase_final = " ".join(clases)

        html += f"""
        <div class="{clase_final}">
          <div class="activity-day">{d.day}</div>
          <div class="activity-weekday">{dias_semana[d.weekday()]}</div>
        </div>
        """

    html += """
      </div>
      <div class="legend">
        <span><span class="dot dot-green"></span>Actividad</span>
        <span><span class="dot dot-orange"></span>Sick Day</span>
        <span><span class="dot dot-gray"></span>Sin registro</span>
      </div>
    </div>
    """

    return html


def descargar_csv(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8-sig")


def porcentaje_ring(valor: int, record: int) -> int:
    if record <= 0:
        return 0

    pct = min(valor / record, 1)
    return int(round(pct * 360))


def ring_html(titulo: str, valor: str, detalle: str, grados: int, color: str) -> str:
    return f"""
    <div class="ring-row">
      <div class="ring" style="--ring-deg:{grados}deg; --ring-color:{color};">
        <div class="ring-inner">
          <div class="ring-value">{valor}</div>
        </div>
      </div>
      <div class="ring-meta">
        <div class="ring-title">{titulo}</div>
        <div class="ring-detail">{detalle}</div>
      </div>
    </div>
    """


# ─────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────

if "show_balloons" not in st.session_state:
    st.session_state.show_balloons = False

if "pr_messages" not in st.session_state:
    st.session_state.pr_messages = []

if "deuda_pendiente_flexiones" not in st.session_state:
    st.session_state.deuda_pendiente_flexiones = 0

if "deuda_pendiente_plancha" not in st.session_state:
    st.session_state.deuda_pendiente_plancha = 0

if "manual_input_version" not in st.session_state:
    st.session_state.manual_input_version = 0

if "express_ok" not in st.session_state:
    st.session_state.express_ok = False

if "deuda_ok" not in st.session_state:
    st.session_state.deuda_ok = False

if "guardado_ok" not in st.session_state:
    st.session_state.guardado_ok = False

if "sick_ok" not in st.session_state:
    st.session_state.sick_ok = False


# ─────────────────────────────────────────────────────────────
# SIDEBAR — PESO Y RPE
# ─────────────────────────────────────────────────────────────

df = cargar_datos()

st.sidebar.markdown("## Peso diario")

peso_input = st.sidebar.number_input(
    "Peso actual (kg)",
    min_value=0.0,
    max_value=300.0,
    value=0.0,
    step=0.1,
    format="%.1f"
)

if st.sidebar.button("Guardar peso", use_container_width=True):
    if peso_input > 0:
        agregar_registro(
            tipo=TIPO_PESO,
            cantidad=0,
            peso=float(peso_input),
            rpe=None
        )

        st.session_state.guardado_ok = True
        st.rerun()
    else:
        st.sidebar.warning("Ingresa un peso válido.")

st.sidebar.markdown("---")
st.sidebar.markdown("## Esfuerzo")

rpe_actual = st.sidebar.slider(
    "RPE esfuerzo",
    min_value=1,
    max_value=10,
    value=7,
    help="1 = muy fácil, 10 = máximo esfuerzo."
)


# ─────────────────────────────────────────────────────────────
# RECÁLCULO DE DATOS
# ─────────────────────────────────────────────────────────────

df = cargar_datos()

flexiones_hoy = total_hoy(df, TIPO_FLEXIONES)
plancha_hoy = total_hoy(df, TIPO_PLANCHA)

record_flexiones = max_historico_diario(df, TIPO_FLEXIONES, excluir_hoy=False)
record_plancha = max_historico_diario(df, TIPO_PLANCHA, excluir_hoy=False)

record_flexiones_prev = max_historico_diario(df, TIPO_FLEXIONES, excluir_hoy=True)
record_plancha_prev = max_historico_diario(df, TIPO_PLANCHA, excluir_hoy=True)

peso_ultimo = peso_actual(df)
racha_actual = calcular_racha(df)

ring_flex_deg = porcentaje_ring(flexiones_hoy, max(record_flexiones, 1))
ring_plancha_deg = porcentaje_ring(plancha_hoy, max(record_plancha, 1))


# ─────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────

st.markdown("""
<div class="app-header">
  <div class="eyebrow">Apple Fitness style</div>
  <h1>Entreno diario</h1>
  <p>Control oscuro, rápido y acumulado de flexiones, plancha, deuda, racha, peso y récords.</p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# MENSAJES Y CONFETI
# ─────────────────────────────────────────────────────────────

if st.session_state.show_balloons:
    st.balloons()
    st.session_state.show_balloons = False

if st.session_state.pr_messages:
    for msg in st.session_state.pr_messages:
        st.success(msg)
    st.session_state.pr_messages = []

if st.session_state.express_ok:
    st.success("¡+5 y +20 registrados!")
    st.session_state.express_ok = False

if st.session_state.deuda_ok:
    st.success("Deuda saldada y registrada.")
    st.session_state.deuda_ok = False

if st.session_state.guardado_ok:
    st.success("Registro guardado correctamente.")
    st.session_state.guardado_ok = False

if st.session_state.sick_ok:
    st.success("Sick Day registrado. La racha sigue viva.")
    st.session_state.sick_ok = False


# ─────────────────────────────────────────────────────────────
# HERO FITNESS
# ─────────────────────────────────────────────────────────────

st.markdown(f"""
<div class="hero-grid">
  <div class="today-panel">
    <div class="panel-label">Total de hoy</div>
    <div class="today-main">{flexiones_hoy}</div>
    <div class="today-sub">
      <span class="pill pill-pink">Flexiones</span>
      <span class="pill pill-green">{format_seconds(plancha_hoy)} plancha</span>
    </div>
  </div>

  <div class="rings-panel">
    <div class="panel-label">Actividad</div>
    {ring_html(
        titulo="Flexiones",
        valor=str(flexiones_hoy),
        detalle=f"PR histórico: {record_flexiones} reps",
        grados=ring_flex_deg,
        color="#FF2D55"
    )}
    {ring_html(
        titulo="Plancha",
        valor=format_seconds(plancha_hoy),
        detalle=f"PR histórico: {format_seconds(record_plancha)}",
        grados=ring_plancha_deg,
        color="#A1FF00"
    )}
  </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# BLOQUES DE IMPACTO
# ─────────────────────────────────────────────────────────────

peso_texto = "Sin dato" if peso_ultimo is None else f"{peso_ultimo:.1f} kg"

st.markdown(f"""
<div class="impact-grid">
  <div class="impact-card">
    <div class="impact-label">Flexiones hoy</div>
    <div class="impact-value pink-text">{flexiones_hoy}</div>
    <div class="impact-detail">Récord previo: {record_flexiones_prev}</div>
  </div>

  <div class="impact-card">
    <div class="impact-label">Plancha hoy</div>
    <div class="impact-value green-text">{format_seconds(plancha_hoy)}</div>
    <div class="impact-detail">Récord previo: {format_seconds(record_plancha_prev)}</div>
  </div>

  <div class="impact-card">
    <div class="impact-label">Racha</div>
    <div class="impact-value orange-text">🔥 {racha_actual}</div>
    <div class="impact-detail">días activos</div>
  </div>

  <div class="impact-card">
    <div class="impact-label">Peso actual</div>
    <div class="impact-value blue-text">{peso_texto}</div>
    <div class="impact-detail">último registro</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────

tab_entreno, tab_deuda, tab_peso, tab_analisis = st.tabs(
    ["Entreno", "Modo Oficina/Calle", "Peso", "Análisis"]
)


# ─────────────────────────────────────────────────────────────
# TAB ENTRENAMIENTO
# ─────────────────────────────────────────────────────────────

with tab_entreno:
    st.markdown("""
    <div class="express-card">
      <div class="express-title">Botón Express</div>
      <div class="express-sub">Para registrar rápido un bloque mínimo sin pensar.</div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="express-button">', unsafe_allow_html=True)

    if st.button("Fui al baño 🚽  +5 flexiones / +20s plancha", use_container_width=True):
        registrar_ejercicio_con_pr(
            tipo=TIPO_FLEXIONES,
            cantidad=5,
            peso=peso_ultimo,
            rpe=rpe_actual
        )

        registrar_ejercicio_con_pr(
            tipo=TIPO_PLANCHA,
            cantidad=20,
            peso=peso_ultimo,
            rpe=rpe_actual
        )

        st.session_state.express_ok = True
        st.rerun()

    st.markdown("</div></div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="fitness-card">
      <div class="card-title">Flexiones</div>
      <div class="card-subtitle">Registro acumulado directo al CSV.</div>
    </div>
    """, unsafe_allow_html=True)

    col_f1, col_f2 = st.columns([1.2, 1])

    with col_f1:
        st.markdown('<div class="pink-button">', unsafe_allow_html=True)

        if st.button("＋ Sumar 5 flexiones", use_container_width=True, key="btn_flex_5"):
            registrar_ejercicio_con_pr(
                tipo=TIPO_FLEXIONES,
                cantidad=5,
                peso=peso_ultimo,
                rpe=rpe_actual
            )

            st.session_state.guardado_ok = True
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    manual_flex_key = f"manual_flex_{st.session_state.manual_input_version}"

    with col_f2:
        manual_flexiones = st.number_input(
            "Flexiones manuales",
            min_value=0,
            max_value=3000,
            value=0,
            step=5,
            key=manual_flex_key
        )

    st.markdown('<div class="pink-button">', unsafe_allow_html=True)

    if st.button("Guardar flexiones escritas", use_container_width=True, key="btn_flex_manual"):
        if manual_flexiones > 0:
            registrar_ejercicio_con_pr(
                tipo=TIPO_FLEXIONES,
                cantidad=int(manual_flexiones),
                peso=peso_ultimo,
                rpe=rpe_actual
            )

            st.session_state.manual_input_version += 1
            st.session_state.guardado_ok = True
            st.rerun()
        else:
            st.warning("Ingresa una cantidad mayor que 0.")

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="fitness-card">
      <div class="card-title">Plancha</div>
      <div class="card-subtitle">Registra segundos acumulados de plancha.</div>
    </div>
    """, unsafe_allow_html=True)

    col_p1, col_p2 = st.columns([1.2, 1])

    with col_p1:
        st.markdown('<div class="green-button">', unsafe_allow_html=True)

        if st.button("＋ Sumar 10 segundos", use_container_width=True, key="btn_plancha_10"):
            registrar_ejercicio_con_pr(
                tipo=TIPO_PLANCHA,
                cantidad=10,
                peso=peso_ultimo,
                rpe=rpe_actual
            )

            st.session_state.guardado_ok = True
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    manual_plancha_key = f"manual_plancha_{st.session_state.manual_input_version}"

    with col_p2:
        manual_plancha = st.number_input(
            "Segundos manuales",
            min_value=0,
            max_value=30000,
            value=0,
            step=10,
            key=manual_plancha_key
        )

    st.markdown('<div class="green-button">', unsafe_allow_html=True)

    if st.button("Guardar segundos escritos", use_container_width=True, key="btn_plancha_manual"):
        if manual_plancha > 0:
            registrar_ejercicio_con_pr(
                tipo=TIPO_PLANCHA,
                cantidad=int(manual_plancha),
                peso=peso_ultimo,
                rpe=rpe_actual
            )

            st.session_state.manual_input_version += 1
            st.session_state.guardado_ok = True
            st.rerun()
        else:
            st.warning("Ingresa una cantidad mayor que 0.")

    st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# TAB DEUDA
# ─────────────────────────────────────────────────────────────

with tab_deuda:
    st.markdown(f"""
    <div class="fitness-card">
      <div class="card-title">Modo Oficina/Calle</div>
      <div class="card-subtitle">
        Anota lo que debes hacer más tarde. Al saldar deuda, se guarda como registro normal.
      </div>

      <div class="debt-display">
        <div class="debt-main">
          {st.session_state.deuda_pendiente_flexiones} flex / {format_seconds(st.session_state.deuda_pendiente_plancha)}
        </div>
        <div class="debt-sub">Deuda pendiente actual</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.number_input(
        "Flexiones pendientes",
        min_value=0,
        max_value=3000,
        step=5,
        key="deuda_pendiente_flexiones"
    )

    st.number_input(
        "Segundos de plancha pendientes",
        min_value=0,
        max_value=30000,
        step=10,
        key="deuda_pendiente_plancha"
    )

    st.markdown('<div class="orange-button">', unsafe_allow_html=True)

    if st.button("Saldar Deuda", use_container_width=True, key="btn_saldar_deuda"):
        flex_deuda = int(st.session_state.deuda_pendiente_flexiones)
        plancha_deuda = int(st.session_state.deuda_pendiente_plancha)

        if flex_deuda > 0:
            registrar_ejercicio_con_pr(
                tipo=TIPO_FLEXIONES,
                cantidad=flex_deuda,
                peso=peso_ultimo,
                rpe=rpe_actual
            )

        if plancha_deuda > 0:
            registrar_ejercicio_con_pr(
                tipo=TIPO_PLANCHA,
                cantidad=plancha_deuda,
                peso=peso_ultimo,
                rpe=rpe_actual
            )

        if flex_deuda > 0 or plancha_deuda > 0:
            st.session_state.deuda_pendiente_flexiones = 0
            st.session_state.deuda_pendiente_plancha = 0
            st.session_state.deuda_ok = True
            st.rerun()
        else:
            st.warning("No hay deuda pendiente para saldar.")

    st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# TAB PESO
# ─────────────────────────────────────────────────────────────

with tab_peso:
    st.markdown("""
    <div class="fitness-card">
      <div class="card-title">Peso y recuperación</div>
      <div class="card-subtitle">
        Registra tu peso desde la barra lateral. El Sick Day está aquí para no competir visualmente con los botones de actividad.
      </div>
    </div>
    """, unsafe_allow_html=True)

    peso_df = preparar_peso_semanal(df)

    if not peso_df.empty:
        st.line_chart(
            peso_df,
            use_container_width=True,
            height=250
        )
    else:
        st.info("Aún no hay suficientes registros de peso para graficar.")

    st.markdown("""
    <div class="fitness-card-soft">
      <div class="card-title">Día Libre / Sick Day</div>
      <div class="card-subtitle">
        Úsalo solo cuando realmente quieras mantener la racha sin sumar repeticiones.
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="subtle-button">', unsafe_allow_html=True)

    if st.button("Día Libre / Sick Day 🤒", use_container_width=True, key="btn_sick_day"):
        hoy_df = obtener_datos_hoy(cargar_datos())

        ya_tiene_sick = False

        if not hoy_df.empty:
            ya_tiene_sick = (hoy_df["Tipo_Ejercicio"] == TIPO_DESCANSO).any()

        if ya_tiene_sick:
            st.warning("Ya registraste Sick Day hoy.")
        else:
            agregar_registro(
                tipo=TIPO_DESCANSO,
                cantidad=0,
                peso=peso_ultimo,
                rpe=None
            )

            st.session_state.sick_ok = True
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# TAB ANÁLISIS
# ─────────────────────────────────────────────────────────────

with tab_analisis:
    st.markdown("""
    <div class="fitness-card">
      <div class="card-title">Calendario de actividad</div>
      <div class="card-subtitle">
        Verde neón = día con actividad. Naranjo = Sick Day. Gris = sin registro.
      </div>
    </div>
    """, unsafe_allow_html=True)

    html_calendario = generar_calendario_html(df, dias=35)

    # CORRECCIÓN URGENTE:
    # Esto renderiza el HTML visualmente y evita que se muestre como texto literal.
    st.markdown(html_calendario, unsafe_allow_html=True)

    st.markdown("""
    <div class="fitness-card">
      <div class="card-title">Récords personales</div>
      <div class="card-subtitle">Máximo acumulado diario registrado en el CSV.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="impact-grid">
      <div class="impact-card">
        <div class="impact-label">PR Flexiones</div>
        <div class="impact-value pink-text">{record_flexiones}</div>
        <div class="impact-detail">reps en un día</div>
      </div>

      <div class="impact-card">
        <div class="impact-label">PR Plancha</div>
        <div class="impact-value green-text">{format_seconds(record_plancha)}</div>
        <div class="impact-detail">tiempo en un día</div>
      </div>

      <div class="impact-card">
        <div class="impact-label">Racha</div>
        <div class="impact-value orange-text">🔥 {racha_actual}</div>
        <div class="impact-detail">días consecutivos</div>
      </div>

      <div class="impact-card">
        <div class="impact-label">Registros</div>
        <div class="impact-value blue-text">{len(df)}</div>
        <div class="impact-detail">filas en CSV</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="fitness-card">
      <div class="card-title">Progreso diario: Flexiones</div>
    </div>
    """, unsafe_allow_html=True)

    flex_chart = preparar_progreso_diario(df, TIPO_FLEXIONES, dias=14)

    if not flex_chart.empty:
        st.bar_chart(
            flex_chart,
            use_container_width=True,
            height=240
        )
    else:
        st.info("Aún no hay registros de flexiones para graficar.")

    st.markdown("""
    <div class="fitness-card">
      <div class="card-title">Progreso diario: Plancha</div>
    </div>
    """, unsafe_allow_html=True)

    plancha_chart = preparar_progreso_diario(df, TIPO_PLANCHA, dias=14)

    if not plancha_chart.empty:
        st.bar_chart(
            plancha_chart,
            use_container_width=True,
            height=240
        )
    else:
        st.info("Aún no hay registros de plancha para graficar.")

    st.markdown("""
    <div class="fitness-card">
      <div class="card-title">Base de datos</div>
      <div class="card-subtitle">
        Formato backend: Fecha, Tipo_Ejercicio, Cantidad, Peso, RPE_Esfuerzo.
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.dataframe(
        df.sort_values("Fecha", ascending=False),
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        label="Descargar base completa CSV para Excel",
        data=descargar_csv(df),
        file_name="data_lagartijas.csv",
        mime="text/csv",
        use_container_width=True
    )

"""
LagartijApp v3.3 — Apple Fitness Dark
=====================================
* Zona horaria forzada a America/Santiago
* Fondo negro absoluto
* Anillos de actividad con flecha estilo Apple Fitness
* Botón superior grande "Fui al baño"
* Métrica Peso en lila Apple Fitness
* Métrica Racha en rosa Apple Fitness
* Sin emojis en textos visibles
"""

import os
from datetime import datetime, timedelta

import altair as alt
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

try:
    from zoneinfo import ZoneInfo
    CHILE_TZ = ZoneInfo("America/Santiago")
except Exception:
    CHILE_TZ = None


# ─────────────────────────────────────────────────────────────
# CONFIGURACIÓN
# ─────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="LagartijApp",
    page_icon="L",
    layout="centered",
    initial_sidebar_state="collapsed",
)

DATA_FILE = "data_lagartijas.csv"
OLD_DATA_FILE = "data_entreno.csv"

COLUMNAS = ["Fecha", "Tipo_Ejercicio", "Cantidad", "Peso", "RPE_Esfuerzo"]

TIPO_FLEXIONES = "Flexiones"
TIPO_PLANCHA = "Plancha"
TIPO_PESO = "Peso"
TIPO_DESCANSO = "Dia Libre"

TIPOS_RACHA = [TIPO_FLEXIONES, TIPO_PLANCHA, TIPO_DESCANSO]

META_FLEXIONES = 50
META_PLANCHA = 120


# ─────────────────────────────────────────────────────────────
# FECHA Y HORA CHILE
# ─────────────────────────────────────────────────────────────

def ahora_chile() -> datetime:
    if CHILE_TZ is not None:
        return datetime.now(CHILE_TZ).replace(tzinfo=None)

    return datetime.utcnow() - timedelta(hours=4)


def hoy_chile():
    return ahora_chile().date()


# ─────────────────────────────────────────────────────────────
# CSS GLOBAL
# ─────────────────────────────────────────────────────────────

st.markdown("""
<style>
:root {
  --bg: #000000;
  --card: #1C1C1E;
  --soft: #2C2C2E;
  --text: #FFFFFF;
  --muted: #8E8E93;
  --border: rgba(255,255,255,0.10);

  --pink: #FF2D55;
  --pink-track: #5C1828;

  --lime: #A1FF00;
  --lime-track: #3E650A;

  --orange: #FF9500;
  --blue: #0A84FF;
  --cyan: #00FFFF;
  --purple: #BF5AF2;
  --gray: #3A3A3C;
}

html, body, [class*="css"] {
  font-family: Inter, -apple-system, BlinkMacSystemFont,
               "SF Pro Display", "Helvetica Neue", Arial, sans-serif;
  background: #000000 !important;
  color: #FFFFFF !important;
  -webkit-font-smoothing: antialiased;
}

[data-testid="stAppViewContainer"],
[data-testid="stBottom"],
.stApp, section.main, .main {
  background: #000000 !important;
  background-color: #000000 !important;
  background-image: none !important;
}

[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
#MainMenu, footer, .stDeployButton {
  display: none !important;
  visibility: hidden !important;
}

[data-testid="collapsedControl"] {
  visibility: visible !important;
  display: flex !important;
  position: fixed !important;
  top: 12px !important;
  left: 12px !important;
  z-index: 999999 !important;
  width: 42px !important;
  height: 42px !important;
  border-radius: 12px !important;
  background: #1C1C1E !important;
  border: 1px solid var(--border) !important;
  align-items: center !important;
  justify-content: center !important;
}

[data-testid="collapsedControl"] svg {
  color: #FFFFFF !important;
}

[data-testid="stSidebar"] {
  background: #111111 !important;
  border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] * {
  color: #FFFFFF;
}

.block-container {
  max-width: 860px;
  padding: 3.5rem 1rem 5rem !important;
  margin: 0 auto;
}

/* Top bar */
.ios-topbar {
  display: flex;
  align-items: baseline;
  gap: 10px;
  padding: 0 4px 8px;
}

.ios-topbar-title {
  font-size: 34px;
  font-weight: 800;
  letter-spacing: -1.4px;
  color: #FFFFFF;
  line-height: 1;
}

.ios-topbar-date {
  font-size: 13px;
  font-weight: 500;
  color: var(--muted);
}

/* Top bath button */
.btn-top-bath div[data-testid="stButton"] > button {
  min-height: 58px !important;
  border-radius: 18px !important;
  background: var(--blue) !important;
  color: #FFFFFF !important;
  font-size: 18px !important;
  font-weight: 800 !important;
  letter-spacing: -0.3px !important;
  border-color: rgba(10,132,255,0.60) !important;
  box-shadow: 0 0 28px rgba(10,132,255,0.25) !important;
}

/* Cards */
.fit-card {
  background: #1C1C1E;
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 22px;
  margin-bottom: 16px;
}

.fit-card-soft {
  background: #2C2C2E;
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 16px;
  margin-bottom: 12px;
}

.card-label {
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.9px;
  text-transform: uppercase;
  color: var(--muted);
  margin-bottom: 6px;
}

.card-title {
  font-size: 22px;
  font-weight: 800;
  letter-spacing: -0.4px;
  color: #FFFFFF;
  margin: 0 0 5px;
}

.card-sub {
  font-size: 13px;
  color: var(--muted);
  line-height: 1.45;
  margin: 0 0 14px;
}

/* Rings */
.rings-master-card {
  background: #1C1C1E;
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 22px;
  margin-bottom: 16px;
  overflow: hidden;
}

.ring-visual-wrap {
  background: #1C1C1E;
  border: none;
  outline: none;
  box-shadow: none;
  border-radius: 20px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

iframe {
  border: 0 !important;
  background: #1C1C1E !important;
  border-radius: 20px !important;
}

[data-testid="stIFrame"] {
  border: 0 !important;
  background: #1C1C1E !important;
  border-radius: 20px !important;
}

.ring-data-stack {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 18px;
  height: 100%;
  min-height: 250px;
}

.ring-stat {
  padding: 14px 0;
  border-bottom: 1px solid rgba(255,255,255,0.08);
}

.ring-stat:last-child {
  border-bottom: none;
}

.ring-stat-label {
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 0.8px;
  text-transform: uppercase;
  color: var(--muted);
  margin-bottom: 8px;
}

.ring-stat-value {
  font-size: 42px;
  line-height: 0.95;
  font-weight: 800;
  letter-spacing: -2px;
}

.ring-stat-sub {
  color: var(--muted);
  font-size: 13px;
  font-weight: 600;
  margin-top: 8px;
}

/* Impact grid */
.impact-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  margin-bottom: 16px;
}

@media (max-width: 700px) {
  .impact-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.impact-card {
  background: #1C1C1E;
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 16px;
  min-height: 100px;
}

.impact-label {
  font-size: 11px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.6px;
  color: var(--muted);
  margin-bottom: 8px;
}

.impact-val {
  font-size: 30px;
  font-weight: 800;
  letter-spacing: -1px;
  line-height: 1;
}

.impact-detail {
  font-size: 11px;
  color: var(--muted);
  margin-top: 6px;
  font-weight: 600;
}

.c-pink { color: var(--pink); }
.c-lime { color: var(--lime); }
.c-orange { color: var(--orange); }
.c-blue { color: var(--blue); }
.c-purple { color: var(--purple); }

/* Exercise module */
.exercise-card {
  background: #1C1C1E;
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 22px;
  margin-bottom: 18px;
}

.exercise-title {
  font-size: 32px;
  font-weight: 800;
  letter-spacing: -1px;
  line-height: 1;
  margin-bottom: 8px;
}

.exercise-subtitle {
  color: var(--muted);
  font-size: 13px;
  line-height: 1.4;
  margin-bottom: 16px;
}

.manual-row {
  margin-top: 10px;
  opacity: 0.86;
}

/* Debt display */
.debt-display {
  background: rgba(255,149,0,0.08);
  border: 1px solid rgba(255,149,0,0.30);
  border-radius: 16px;
  padding: 16px 18px;
  margin-bottom: 16px;
}

.debt-number {
  font-size: 34px;
  font-weight: 800;
  letter-spacing: -1px;
  color: var(--orange);
  line-height: 1;
}

.debt-sub {
  font-size: 11px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.6px;
  color: var(--muted);
  margin-top: 6px;
}

/* Calendar */
.cal-wrap {
  margin-top: 6px;
}

.cal-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 7px;
}

.cal-cell {
  aspect-ratio: 1 / 1;
  border-radius: 12px;
  background: #1C1C1E;
  border: 1px solid rgba(255,255,255,0.07);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  opacity: 0.40;
}

.cal-cell.cal-future {
  opacity: 0.18;
}

.cal-cell.cal-today {
  opacity: 1;
  outline: 2px solid var(--pink);
  outline-offset: 2px;
}

.cal-cell.cal-done {
  background: var(--lime);
  border-color: var(--lime);
  opacity: 0.72;
  box-shadow: 0 0 14px rgba(161,255,0,0.45);
}

.cal-cell.cal-rest {
  background: var(--orange);
  border-color: var(--orange);
  opacity: 0.72;
}

.cal-cell.cal-done.cal-today,
.cal-cell.cal-rest.cal-today {
  opacity: 1;
}

.cal-day {
  font-size: 14px;
  font-weight: 800;
  color: #FFFFFF;
  line-height: 1;
}

.cal-done .cal-day,
.cal-rest .cal-day {
  color: #000000;
}

.cal-wd {
  font-size: 9px;
  font-weight: 700;
  color: rgba(255,255,255,0.5);
  margin-top: 3px;
}

.cal-done .cal-wd,
.cal-rest .cal-wd {
  color: rgba(0,0,0,0.55);
}

.cal-legend {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  margin-top: 12px;
  justify-content: center;
  font-size: 11px;
  font-weight: 700;
  color: var(--muted);
  line-height: 1.3;
}

.dot {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-right: 5px;
  vertical-align: middle;
}

.dot-lime {
  background: var(--lime);
  box-shadow: 0 0 8px rgba(161,255,0,.6);
}

.dot-orange {
  background: var(--orange);
}

.dot-gray {
  background: var(--gray);
}

/* Buttons */
div[data-testid="stButton"] > button {
  border-radius: 16px !important;
  min-height: 52px !important;
  font-size: 15px !important;
  font-weight: 800 !important;
  letter-spacing: -0.2px !important;
  border: 1px solid var(--border) !important;
  background: #2C2C2E !important;
  color: #FFFFFF !important;
  width: 100% !important;
  transition: transform .08s ease, opacity .1s ease !important;
}

div[data-testid="stButton"] > button:hover {
  transform: scale(0.985);
  opacity: .92;
}

div[data-testid="stButton"] > button:active {
  transform: scale(0.96);
  opacity: .78;
}

.btn-pink div[data-testid="stButton"] > button {
  background: var(--pink) !important;
  color: #FFFFFF !important;
  border-color: rgba(255,45,85,0.55) !important;
  min-height: 68px !important;
  font-size: 18px !important;
}

.btn-lime div[data-testid="stButton"] > button {
  background: var(--lime) !important;
  color: #000000 !important;
  border-color: rgba(161,255,0,0.55) !important;
  min-height: 68px !important;
  font-size: 18px !important;
}

.btn-orange div[data-testid="stButton"] > button {
  background: var(--orange) !important;
  color: #000000 !important;
  border-color: rgba(255,149,0,0.55) !important;
}

.btn-subtle div[data-testid="stButton"] > button {
  background: #2C2C2E !important;
  color: var(--muted) !important;
  border-color: rgba(255,255,255,0.07) !important;
}

.btn-blue div[data-testid="stButton"] > button {
  background: var(--blue) !important;
  color: #FFFFFF !important;
  border-color: rgba(10,132,255,0.55) !important;
}

/* Inputs */
div[data-testid="stNumberInput"] label {
  font-size: 11px !important;
  font-weight: 700 !important;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: var(--muted) !important;
}

div[data-testid="stNumberInput"] input {
  border-radius: 12px !important;
  background: #2C2C2E !important;
  border: 1px solid var(--border) !important;
  color: #FFFFFF !important;
  font-size: 15px !important;
  min-height: 42px !important;
}

div[data-testid="stSlider"] label {
  color: var(--muted) !important;
  font-size: 12px !important;
  font-weight: 700 !important;
}

/* Tabs */
[data-testid="stTabs"] button {
  border-radius: 999px !important;
  font-weight: 800 !important;
  font-size: 14px !important;
  color: var(--muted) !important;
}

[data-testid="stTabs"] [aria-selected="true"] {
  color: var(--lime) !important;
}

/* Alerts */
.stSuccess, .stWarning, .stInfo {
  border-radius: 16px !important;
  border: none !important;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# FUNCIONES DE DATOS
# ─────────────────────────────────────────────────────────────

def crear_df_vacio() -> pd.DataFrame:
    return pd.DataFrame(columns=COLUMNAS)


def normalizar_df(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return crear_df_vacio()

    if all(c in df.columns for c in COLUMNAS):
        out = df[COLUMNAS].copy()

    elif "fecha" in df.columns and "cantidad" in df.columns:
        out = pd.DataFrame({
            "Fecha": df["fecha"],
            "Tipo_Ejercicio": TIPO_FLEXIONES,
            "Cantidad": df["cantidad"],
            "Peso": None,
            "RPE_Esfuerzo": None,
        })

    elif "fecha" in df.columns and ("lagartijas" in df.columns or "plancha_segundos" in df.columns):
        rows = []

        for _, row in df.iterrows():
            f = row.get("fecha", ahora_chile().strftime("%Y-%m-%d %H:%M"))
            fl = int(row.get("lagartijas", 0) or 0)
            pl = int(row.get("plancha_segundos", 0) or 0)

            if fl > 0:
                rows.append({
                    "Fecha": f,
                    "Tipo_Ejercicio": TIPO_FLEXIONES,
                    "Cantidad": fl,
                    "Peso": None,
                    "RPE_Esfuerzo": None,
                })

            if pl > 0:
                rows.append({
                    "Fecha": f,
                    "Tipo_Ejercicio": TIPO_PLANCHA,
                    "Cantidad": pl,
                    "Peso": None,
                    "RPE_Esfuerzo": None,
                })

        out = pd.DataFrame(rows, columns=COLUMNAS)

    else:
        out = crear_df_vacio()

    for col in COLUMNAS:
        if col not in out.columns:
            out[col] = None

    out["Fecha"] = pd.to_datetime(out["Fecha"], errors="coerce")
    out = out.dropna(subset=["Fecha"])
    out["Fecha"] = out["Fecha"].dt.tz_localize(None)

    out["Tipo_Ejercicio"] = out["Tipo_Ejercicio"].astype(str)
    out["Cantidad"] = pd.to_numeric(out["Cantidad"], errors="coerce").fillna(0).astype(int)
    out["Peso"] = pd.to_numeric(out["Peso"], errors="coerce")
    out["RPE_Esfuerzo"] = pd.to_numeric(out["RPE_Esfuerzo"], errors="coerce")

    return out[COLUMNAS]


def guardar_df(df: pd.DataFrame) -> None:
    normalizar_df(df).to_csv(DATA_FILE, index=False)


def cargar_datos() -> pd.DataFrame:
    if os.path.exists(DATA_FILE):
        return normalizar_df(pd.read_csv(DATA_FILE))

    if os.path.exists(OLD_DATA_FILE):
        df = normalizar_df(pd.read_csv(OLD_DATA_FILE))
        guardar_df(df)
        return df

    return crear_df_vacio()


def agregar_registro(tipo: str, cantidad: int, peso=None, rpe=None) -> None:
    df = cargar_datos()

    nuevo = pd.DataFrame([{
        "Fecha": ahora_chile(),
        "Tipo_Ejercicio": tipo,
        "Cantidad": int(cantidad),
        "Peso": peso,
        "RPE_Esfuerzo": rpe,
    }])

    guardar_df(pd.concat([df, nuevo], ignore_index=True))


def datos_hoy(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return crear_df_vacio()

    return df[df["Fecha"].dt.date == hoy_chile()]


def total_hoy(df: pd.DataFrame, tipo: str) -> int:
    hoy = datos_hoy(df)

    if hoy.empty:
        return 0

    return int(hoy.loc[hoy["Tipo_Ejercicio"] == tipo, "Cantidad"].sum())


def peso_actual(df: pd.DataFrame):
    if df.empty:
        return None

    p = df.dropna(subset=["Peso"])
    p = p[p["Peso"] > 0]

    if p.empty:
        return None

    return float(p.sort_values("Fecha").iloc[-1]["Peso"])


def fmt(seconds: int) -> str:
    s = int(seconds)

    if s < 60:
        return f"{s}s"

    m, sec = divmod(s, 60)

    if m < 60:
        return f"{m}:{sec:02d}"

    h, m = divmod(m, 60)
    return f"{h}h {m}m {sec}s"


def max_diario(df: pd.DataFrame, tipo: str, excluir_hoy: bool = True) -> int:
    if df.empty:
        return 0

    t = df[df["Tipo_Ejercicio"] == tipo].copy()

    if excluir_hoy:
        t = t[t["Fecha"].dt.date != hoy_chile()]

    if t.empty:
        return 0

    daily = t.groupby(t["Fecha"].dt.date)["Cantidad"].sum()

    if daily.empty:
        return 0

    return int(daily.max())


def registrar_con_pr(tipo: str, cantidad: int, peso=None, rpe=None) -> None:
    if cantidad <= 0:
        return

    df0 = cargar_datos()
    prev = max_diario(df0, tipo, excluir_hoy=True)
    hoy_n = total_hoy(df0, tipo)

    agregar_registro(tipo=tipo, cantidad=int(cantidad), peso=peso, rpe=rpe)

    nuevo = hoy_n + int(cantidad)

    if nuevo > prev:
        val = fmt(nuevo) if tipo == TIPO_PLANCHA else f"{nuevo} reps"
        st.session_state.pr_msg.append(f"Record personal: {tipo} — {val}")
        st.session_state.show_balloons = True


def calcular_racha(df: pd.DataFrame) -> int:
    if df.empty:
        return 0

    temp = df[df["Tipo_Ejercicio"].isin(TIPOS_RACHA)].copy()

    temp = temp[
        ((temp["Tipo_Ejercicio"].isin([TIPO_FLEXIONES, TIPO_PLANCHA])) & (temp["Cantidad"] > 0)) |
        (temp["Tipo_Ejercicio"] == TIPO_DESCANSO)
    ]

    activas = set(temp["Fecha"].dt.date)

    racha = 0
    cur = hoy_chile()

    while cur in activas:
        racha += 1
        cur -= timedelta(days=1)

    return racha


def fechas_descanso(df: pd.DataFrame) -> set:
    if df.empty:
        return set()

    t = df[df["Tipo_Ejercicio"] == TIPO_DESCANSO]
    return set(t["Fecha"].dt.date)


def fechas_activas(df: pd.DataFrame) -> set:
    if df.empty:
        return set()

    temp = df[df["Tipo_Ejercicio"].isin(TIPOS_RACHA)].copy()

    temp = temp[
        ((temp["Tipo_Ejercicio"].isin([TIPO_FLEXIONES, TIPO_PLANCHA])) & (temp["Cantidad"] > 0)) |
        (temp["Tipo_Ejercicio"] == TIPO_DESCANSO)
    ]

    return set(temp["Fecha"].dt.date)


def peso_semanal(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()

    desde = hoy_chile() - timedelta(days=6)

    t = df[
        (df["Fecha"].dt.date >= desde) &
        df["Peso"].notna() &
        (df["Peso"] > 0)
    ].copy()

    if t.empty:
        return pd.DataFrame()

    t["Dia"] = t["Fecha"].dt.strftime("%d/%m")

    return (
        t.sort_values("Fecha")
        .groupby("Dia", as_index=False)["Peso"]
        .last()
        .set_index("Dia")
    )


def progreso_diario(df: pd.DataFrame, tipo: str, dias: int = 14) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()

    desde = hoy_chile() - timedelta(days=dias - 1)

    t = df[
        (df["Tipo_Ejercicio"] == tipo) &
        (df["Fecha"].dt.date >= desde)
    ].copy()

    if t.empty:
        return pd.DataFrame()

    t["Dia"] = t["Fecha"].dt.strftime("%d/%m")

    return t.groupby("Dia", as_index=False)["Cantidad"].sum().set_index("Dia")


def actividad_horaria(df: pd.DataFrame) -> pd.DataFrame:
    hoy = datos_hoy(df)

    if hoy.empty:
        return pd.DataFrame(columns=["Hora", "Tipo_Ejercicio", "Cantidad"])

    t = hoy[hoy["Tipo_Ejercicio"].isin([TIPO_FLEXIONES, TIPO_PLANCHA])].copy()

    if t.empty:
        return pd.DataFrame(columns=["Hora", "Tipo_Ejercicio", "Cantidad"])

    t["Hora"] = t["Fecha"].dt.hour

    resumen = t.groupby(["Hora", "Tipo_Ejercicio"], as_index=False)["Cantidad"].sum()

    base = pd.DataFrame({"Hora": list(range(24))}).merge(
        pd.DataFrame({"Tipo_Ejercicio": [TIPO_FLEXIONES, TIPO_PLANCHA]}),
        how="cross"
    )

    resumen = base.merge(resumen, on=["Hora", "Tipo_Ejercicio"], how="left")
    resumen["Cantidad"] = resumen["Cantidad"].fillna(0).astype(int)

    return resumen


def sync_deuda(input_key: str, state_key: str) -> None:
    st.session_state[state_key] = int(st.session_state.get(input_key, 0) or 0)


def pct(valor: int, meta: int) -> float:
    return min(max(valor / meta, 0.0), 1.0) if meta > 0 else 0.0


# ─────────────────────────────────────────────────────────────
# HTML PURO
# ─────────────────────────────────────────────────────────────

def arrow_polygon(cx: float, cy: float, r: float, progress: float, size: float) -> str:
    """
    Genera una pequeña flecha tangencial al final del progreso del anillo.
    """
    import math

    if progress <= 0.02:
        return ""

    progress = min(progress, 0.995)

    angle_deg = -90 + 360 * progress
    angle = math.radians(angle_deg)

    x = cx + r * math.cos(angle)
    y = cy + r * math.sin(angle)

    tangent = angle + math.pi / 2

    tx = math.cos(tangent)
    ty = math.sin(tangent)

    nx = math.cos(angle)
    ny = math.sin(angle)

    tip_x = x + tx * size * 0.55
    tip_y = y + ty * size * 0.55

    base_x = x - tx * size * 0.55
    base_y = y - ty * size * 0.55

    p1_x = tip_x
    p1_y = tip_y

    p2_x = base_x + nx * size * 0.38
    p2_y = base_y + ny * size * 0.38

    p3_x = base_x - nx * size * 0.38
    p3_y = base_y - ny * size * 0.38

    return f"{p1_x:.2f},{p1_y:.2f} {p2_x:.2f},{p2_y:.2f} {p3_x:.2f},{p3_y:.2f}"


def rings_html(flexiones: int, plancha: int) -> str:
    import math

    pi = math.pi

    outer_r = 100
    inner_r = 62

    outer_c = 2 * pi * outer_r
    inner_c = 2 * pi * inner_r

    flex_progress = pct(flexiones, META_FLEXIONES)
    plan_progress = pct(plancha, META_PLANCHA)

    outer_dash = outer_c * flex_progress
    inner_dash = inner_c * plan_progress

    outer_arrow = arrow_polygon(130, 130, outer_r, flex_progress, 26)
    inner_arrow = arrow_polygon(130, 130, inner_r, plan_progress, 22)

    outer_arrow_svg = ""
    inner_arrow_svg = ""

    if outer_arrow:
        outer_arrow_svg = f'<polygon points="{outer_arrow}" fill="#FF2D55" />'

    if inner_arrow:
        inner_arrow_svg = f'<polygon points="{inner_arrow}" fill="#A1FF00" />'

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }}

  html, body {{
    width: 100%;
    height: 100%;
    background: #1C1C1E;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
  }}

  svg {{
    display: block;
    overflow: visible;
    background: #1C1C1E;
  }}
</style>
</head>
<body>
<svg viewBox="0 0 260 260" width="260" height="260" xmlns="http://www.w3.org/2000/svg">

  <circle
    cx="130"
    cy="130"
    r="{outer_r}"
    fill="none"
    stroke="#5C1828"
    stroke-width="32"
  />

  <circle
    cx="130"
    cy="130"
    r="{outer_r}"
    fill="none"
    stroke="#FF2D55"
    stroke-width="32"
    stroke-linecap="round"
    stroke-dasharray="{outer_dash:.2f} {outer_c:.2f}"
    transform="rotate(-90 130 130)"
  />

  {outer_arrow_svg}

  <circle
    cx="130"
    cy="130"
    r="{inner_r}"
    fill="none"
    stroke="#3E650A"
    stroke-width="32"
  />

  <circle
    cx="130"
    cy="130"
    r="{inner_r}"
    fill="none"
    stroke="#A1FF00"
    stroke-width="32"
    stroke-linecap="round"
    stroke-dasharray="{inner_dash:.2f} {inner_c:.2f}"
    transform="rotate(-90 130 130)"
  />

  {inner_arrow_svg}

</svg>
</body>
</html>"""


def calendario_html(df: pd.DataFrame, dias: int = 35) -> str:
    activas = fechas_activas(df)
    descansos = fechas_descanso(df)
    inicio = hoy_chile() - timedelta(days=dias - 1)
    hoy = hoy_chile()
    sem = ["L", "M", "X", "J", "V", "S", "D"]

    cells = ""

    for i in range(dias):
        d = inicio + timedelta(days=i)

        clases = ["cal-cell"]

        if d > hoy:
            clases.append("cal-future")

        if d in descansos:
            clases.append("cal-rest")
        elif d in activas:
            clases.append("cal-done")

        if d == hoy:
            clases.append("cal-today")

        is_filled = ("cal-done" in clases) or ("cal-rest" in clases)

        wd_color = "rgba(0,0,0,0.55)" if is_filled else "rgba(255,255,255,0.45)"
        day_color = "#000000" if is_filled else "#FFFFFF"

        cells += f"""
<div class="{' '.join(clases)}">
  <div style="font-size:14px;font-weight:800;color:{day_color};line-height:1">{d.day}</div>
  <div style="font-size:9px;font-weight:700;color:{wd_color};margin-top:3px">{sem[d.weekday()]}</div>
</div>
"""

    return f"""
<div class="cal-wrap">
  <div class="cal-grid">
    {cells}
  </div>
  <div class="cal-legend">
    <span><span class="dot dot-lime"></span>Actividad</span>
    <span><span class="dot dot-orange"></span>Dia libre</span>
    <span><span class="dot dot-gray"></span>Sin registro</span>
  </div>
</div>
"""


def descargar_csv(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8-sig")


# ─────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────

defaults = {
    "show_balloons": False,
    "pr_msg": [],
    "deuda_flex": 0,
    "deuda_plan": 0,
    "deuda_ver": 0,
    "manual_ver": 0,
    "express_ok": False,
    "deuda_ok": False,
    "guardado_ok": False,
    "sick_ok": False,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────

df = cargar_datos()

with st.sidebar:
    st.markdown("**Peso diario**")

    peso_input = st.number_input(
        "Peso (kg)",
        min_value=0.0,
        max_value=300.0,
        value=0.0,
        step=0.1,
        format="%.1f"
    )

    st.markdown('<div class="btn-subtle">', unsafe_allow_html=True)

    if st.button("Guardar peso", use_container_width=True):
        if peso_input > 0:
            agregar_registro(TIPO_PESO, 0, peso=float(peso_input))
            st.session_state.guardado_ok = True
            st.rerun()
        else:
            st.warning("Ingresa un peso valido.")

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**Dia libre**")
    st.caption("Mantiene la racha activa.")

    st.markdown('<div class="btn-subtle">', unsafe_allow_html=True)

    if st.button("Marcar dia libre", use_container_width=True):
        hd = datos_hoy(cargar_datos())
        ya = not hd.empty and (hd["Tipo_Ejercicio"] == TIPO_DESCANSO).any()

        if ya:
            st.warning("Ya marcaste dia libre hoy.")
        else:
            agregar_registro(TIPO_DESCANSO, 0)
            st.session_state.sick_ok = True
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**Esfuerzo (RPE)**")

    rpe_actual = st.slider(
        "RPE",
        1,
        10,
        7,
        help="1 = facil · 10 = maximo"
    )


# ─────────────────────────────────────────────────────────────
# CÁLCULOS
# ─────────────────────────────────────────────────────────────

df = cargar_datos()

flex_hoy = total_hoy(df, TIPO_FLEXIONES)
plan_hoy = total_hoy(df, TIPO_PLANCHA)

peso_ult = peso_actual(df)
racha = calcular_racha(df)

pr_flex = max_diario(df, TIPO_FLEXIONES, excluir_hoy=False)
pr_plan = max_diario(df, TIPO_PLANCHA, excluir_hoy=False)

peso_txt = "Sin dato" if peso_ult is None else f"{peso_ult:.1f} kg"


# ─────────────────────────────────────────────────────────────
# TOP BAR + BOTÓN SUPERIOR
# ─────────────────────────────────────────────────────────────

fecha_txt = hoy_chile().strftime("%d/%m/%Y")

col_top_left, col_top_right = st.columns([1.1, 0.9])

with col_top_left:
    st.markdown(f"""
<div class="ios-topbar">
  <span class="ios-topbar-title">LagartijApp</span>
  <span class="ios-topbar-date">{fecha_txt}</span>
</div>
""", unsafe_allow_html=True)

with col_top_right:
    st.markdown('<div class="btn-top-bath">', unsafe_allow_html=True)

    if st.button("Fui al baño", use_container_width=True, key="btn_top_bath"):
        registrar_con_pr(TIPO_FLEXIONES, 5, peso=peso_ult, rpe=rpe_actual)
        registrar_con_pr(TIPO_PLANCHA, 20, peso=peso_ult, rpe=rpe_actual)
        st.session_state.express_ok = True
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# MENSAJES
# ─────────────────────────────────────────────────────────────

if st.session_state.show_balloons:
    st.balloons()
    st.session_state.show_balloons = False

for msg in st.session_state.pr_msg:
    st.success(msg)

st.session_state.pr_msg = []

if st.session_state.express_ok:
    st.success("+5 flexiones y +20 s registrados.")
    st.session_state.express_ok = False

if st.session_state.deuda_ok:
    st.success("Deuda saldada.")
    st.session_state.deuda_ok = False

if st.session_state.guardado_ok:
    st.success("Guardado.")
    st.session_state.guardado_ok = False

if st.session_state.sick_ok:
    st.success("Dia libre registrado.")
    st.session_state.sick_ok = False


# ─────────────────────────────────────────────────────────────
# DASHBOARD DE ANILLOS
# ─────────────────────────────────────────────────────────────

st.markdown('<div class="rings-master-card">', unsafe_allow_html=True)

col_ring, col_data = st.columns([1.05, 0.95])

with col_ring:
    st.markdown('<div class="ring-visual-wrap">', unsafe_allow_html=True)
    components.html(rings_html(flex_hoy, plan_hoy), height=280, scrolling=False)
    st.markdown("</div>", unsafe_allow_html=True)

with col_data:
    st.markdown(f"""
<div class="ring-data-stack">
  <div class="ring-stat">
    <div class="ring-stat-label">Flexiones</div>
    <div class="ring-stat-value c-pink">{flex_hoy} / {META_FLEXIONES}</div>
    <div class="ring-stat-sub">Progreso visual del dia</div>
  </div>

  <div class="ring-stat">
    <div class="ring-stat-label">Plancha</div>
    <div class="ring-stat-value c-lime">{plan_hoy} / {META_PLANCHA}s</div>
    <div class="ring-stat-sub">Progreso visual del dia</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# IMPACT GRID
# ─────────────────────────────────────────────────────────────

st.markdown(f"""
<div class="impact-grid">
  <div class="impact-card">
    <div class="impact-label">Flexiones hoy</div>
    <div class="impact-val c-pink">{flex_hoy}</div>
    <div class="impact-detail">meta visual {META_FLEXIONES}</div>
  </div>

  <div class="impact-card">
    <div class="impact-label">Plancha hoy</div>
    <div class="impact-val c-lime">{fmt(plan_hoy)}</div>
    <div class="impact-detail">meta visual {fmt(META_PLANCHA)}</div>
  </div>

  <div class="impact-card">
    <div class="impact-label">Racha</div>
    <div class="impact-val c-pink">{racha}</div>
    <div class="impact-detail">dias consecutivos</div>
  </div>

  <div class="impact-card">
    <div class="impact-label">Peso</div>
    <div class="impact-val c-purple">{peso_txt}</div>
    <div class="impact-detail">ultimo registro</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────

tab_e, tab_d, tab_p, tab_a = st.tabs(["Entreno", "Oficina / Calle", "Peso", "Analisis"])


# ══════════════════════════════════════════════════════════════
# TAB 1 — ENTRENO
# ══════════════════════════════════════════════════════════════

with tab_e:
    st.markdown("""
<div class="exercise-card">
  <div class="card-label">Ejercicio</div>
  <div class="exercise-title c-pink">FLEXIONES</div>
  <div class="exercise-subtitle">Un toque registra 5 repeticiones. El campo inferior permite ingresar una cifra exacta.</div>
</div>
""", unsafe_allow_html=True)

    st.markdown('<div class="btn-pink">', unsafe_allow_html=True)

    if st.button("+ 5 Flexiones", use_container_width=True, key="btn_f5"):
        registrar_con_pr(TIPO_FLEXIONES, 5, peso=peso_ult, rpe=rpe_actual)
        st.session_state.guardado_ok = True
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    mfk = f"mf_{st.session_state.manual_ver}"

    st.markdown('<div class="manual-row">', unsafe_allow_html=True)

    mf = st.number_input(
        "Cantidad exacta de flexiones",
        min_value=0,
        max_value=3000,
        value=0,
        step=1,
        key=mfk
    )

    st.markdown("</div>", unsafe_allow_html=True)

    if mf > 0:
        st.markdown('<div class="btn-pink">', unsafe_allow_html=True)

        if st.button("Guardar flexiones", use_container_width=True, key="btn_mf"):
            registrar_con_pr(TIPO_FLEXIONES, int(mf), peso=peso_ult, rpe=rpe_actual)
            st.session_state.manual_ver += 1
            st.session_state.guardado_ok = True
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
<div class="exercise-card">
  <div class="card-label">Ejercicio</div>
  <div class="exercise-title c-lime">PLANCHA</div>
  <div class="exercise-subtitle">Un toque registra 10 segundos. El campo inferior permite ingresar segundos exactos.</div>
</div>
""", unsafe_allow_html=True)

    st.markdown('<div class="btn-lime">', unsafe_allow_html=True)

    if st.button("+ 10 segundos", use_container_width=True, key="btn_p10"):
        registrar_con_pr(TIPO_PLANCHA, 10, peso=peso_ult, rpe=rpe_actual)
        st.session_state.guardado_ok = True
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    mpk = f"mp_{st.session_state.manual_ver}"

    st.markdown('<div class="manual-row">', unsafe_allow_html=True)

    mp = st.number_input(
        "Segundos exactos de plancha",
        min_value=0,
        max_value=30000,
        value=0,
        step=5,
        key=mpk
    )

    st.markdown("</div>", unsafe_allow_html=True)

    if mp > 0:
        st.markdown('<div class="btn-lime">', unsafe_allow_html=True)

        if st.button("Guardar plancha", use_container_width=True, key="btn_mp"):
            registrar_con_pr(TIPO_PLANCHA, int(mp), peso=peso_ult, rpe=rpe_actual)
            st.session_state.manual_ver += 1
            st.session_state.guardado_ok = True
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# TAB 2 — DEUDA / OFICINA
# ══════════════════════════════════════════════════════════════

with tab_d:
    st.markdown(f"""
<div class="fit-card">
  <div class="card-label">Modo Oficina / Calle</div>
  <div class="card-title">Deuda pendiente</div>
  <div class="card-sub">Acumula lo que debes y saldalo de un toque.</div>

  <div class="debt-display">
    <div class="debt-number">{st.session_state.deuda_flex} flex &nbsp;/&nbsp; {fmt(st.session_state.deuda_plan)}</div>
    <div class="debt-sub">Pendiente ahora</div>
  </div>
</div>
""", unsafe_allow_html=True)

    dv = st.session_state.deuda_ver
    dfk = f"df_{dv}"
    dpk = f"dp_{dv}"

    st.number_input(
        "Flexiones pendientes",
        min_value=0,
        max_value=3000,
        value=st.session_state.deuda_flex,
        step=5,
        key=dfk,
        on_change=sync_deuda,
        args=(dfk, "deuda_flex")
    )

    st.number_input(
        "Segundos de plancha pendientes",
        min_value=0,
        max_value=30000,
        value=st.session_state.deuda_plan,
        step=10,
        key=dpk,
        on_change=sync_deuda,
        args=(dpk, "deuda_plan")
    )

    st.markdown('<div class="btn-orange">', unsafe_allow_html=True)

    if st.button("Saldar deuda", use_container_width=True, key="btn_saldar"):
        fd = int(st.session_state.deuda_flex)
        pd_ = int(st.session_state.deuda_plan)

        if fd > 0:
            registrar_con_pr(TIPO_FLEXIONES, fd, peso=peso_ult, rpe=rpe_actual)

        if pd_ > 0:
            registrar_con_pr(TIPO_PLANCHA, pd_, peso=peso_ult, rpe=rpe_actual)

        if fd > 0 or pd_ > 0:
            st.session_state.deuda_flex = 0
            st.session_state.deuda_plan = 0
            st.session_state.deuda_ver += 1
            st.session_state.deuda_ok = True
            st.rerun()
        else:
            st.warning("No hay deuda pendiente.")

    st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# TAB 3 — PESO
# ══════════════════════════════════════════════════════════════

with tab_p:
    st.markdown("""
<div class="fit-card">
  <div class="card-label">Peso</div>
  <div class="card-title">Evolucion semanal</div>
  <div class="card-sub">Registra desde la barra lateral. Ultimos 7 dias.</div>
</div>
""", unsafe_allow_html=True)

    pdf = peso_semanal(df)

    if not pdf.empty:
        st.line_chart(pdf, use_container_width=True, height=260, color="#BF5AF2")
    else:
        st.info("Sin registros de peso aun.")


# ══════════════════════════════════════════════════════════════
# TAB 4 — ANALISIS
# ══════════════════════════════════════════════════════════════

with tab_a:
    st.markdown("""
<div class="fit-card">
  <div class="card-label">Hoy</div>
  <div class="card-title">Actividad horaria</div>
  <div class="card-sub">Distribucion de registros por hora local de Chile.</div>
</div>
""", unsafe_allow_html=True)

    hdf = actividad_horaria(df)

    if not hdf.empty and hdf["Cantidad"].sum() > 0:
        hdf["activo"] = hdf["Cantidad"].apply(lambda x: "activo" if x > 0 else "inactivo")

        chart = (
            alt.Chart(hdf)
            .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
            .encode(
                x=alt.X("Hora:O", title="Hora"),
                y=alt.Y("Cantidad:Q", title=""),
                color=alt.Color(
                    "activo:N",
                    scale=alt.Scale(
                        domain=["activo", "inactivo"],
                        range=["#00FFFF", "#3A3A3C"]
                    ),
                    legend=None
                ),
                tooltip=["Hora", "Tipo_Ejercicio", "Cantidad"],
            )
            .properties(height=240)
            .configure_view(strokeWidth=0)
            .configure_axis(
                labelColor="#8E8E93",
                titleColor="#8E8E93",
                gridColor="rgba(255,255,255,0.06)"
            )
            .configure(background="#000000")
        )

        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("Sin actividad registrada hoy.")

    st.markdown("""
<div class="fit-card">
  <div class="card-label">Ultimos 35 dias</div>
  <div class="card-title">Calendario</div>
  <div class="card-sub">Verde: actividad. Naranja: dia libre. Gris: sin registro.</div>
</div>
""", unsafe_allow_html=True)

    st.markdown(calendario_html(df, dias=35), unsafe_allow_html=True)

    st.markdown(f"""
<div class="impact-grid" style="margin-top:16px">
  <div class="impact-card">
    <div class="impact-label">Record Flexiones</div>
    <div class="impact-val c-pink">{pr_flex}</div>
    <div class="impact-detail">reps en un dia</div>
  </div>

  <div class="impact-card">
    <div class="impact-label">Record Plancha</div>
    <div class="impact-val c-lime">{fmt(pr_plan)}</div>
    <div class="impact-detail">tiempo en un dia</div>
  </div>

  <div class="impact-card">
    <div class="impact-label">Racha</div>
    <div class="impact-val c-pink">{racha}</div>
    <div class="impact-detail">dias activos</div>
  </div>

  <div class="impact-card">
    <div class="impact-label">Registros</div>
    <div class="impact-val c-blue">{len(df)}</div>
    <div class="impact-detail">filas en CSV</div>
  </div>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="fit-card" style="margin-top:16px">
  <div class="card-label">14 dias</div>
  <div class="card-title">Progreso</div>
</div>
""", unsafe_allow_html=True)

    fc = progreso_diario(df, TIPO_FLEXIONES, 14)
    pc = progreso_diario(df, TIPO_PLANCHA, 14)

    if not fc.empty:
        st.markdown(
            '<p style="color:#FF2D55;font-size:12px;font-weight:800;text-transform:uppercase;letter-spacing:.6px;margin-bottom:4px">Flexiones</p>',
            unsafe_allow_html=True
        )
        st.bar_chart(fc, use_container_width=True, height=180, color="#FF2D55")
    else:
        st.info("Sin datos de flexiones.")

    if not pc.empty:
        st.markdown(
            '<p style="color:#A1FF00;font-size:12px;font-weight:800;text-transform:uppercase;letter-spacing:.6px;margin:8px 0 4px">Plancha</p>',
            unsafe_allow_html=True
        )
        st.bar_chart(pc, use_container_width=True, height=180, color="#A1FF00")
    else:
        st.info("Sin datos de plancha.")

    st.markdown("""
<div class="fit-card" style="margin-top:16px">
  <div class="card-label">CSV</div>
  <div class="card-title">Base de datos</div>
</div>
""", unsafe_allow_html=True)

    st.dataframe(
        df.sort_values("Fecha", ascending=False),
        use_container_width=True,
        hide_index=True
    )

    st.markdown('<div class="btn-blue">', unsafe_allow_html=True)

    st.download_button(
        label="Descargar CSV",
        data=descargar_csv(df),
        file_name="data_lagartijas.csv",
        mime="text/csv",
        use_container_width=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)

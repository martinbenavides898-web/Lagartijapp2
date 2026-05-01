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
# ESTILO APPLE / MODERNO
# ─────────────────────────────────────────────────────────────

st.markdown("""
<style>
  html {
    color-scheme: light dark;
  }

  :root {
    --ios-bg: #F2F2F7;
    --ios-card: #FFFFFF;
    --ios-text: #1C1C1E;
    --ios-muted: #8E8E93;
    --ios-blue: #007AFF;
    --ios-green: #34C759;
    --ios-orange: #FF9500;
    --ios-red: #FF3B30;
    --ios-gray: #E5E5EA;
    --ios-border: rgba(60, 60, 67, 0.12);
    --ios-input: #FAFAFA;
    --ios-metric-bg: rgba(255,255,255,0.72);
  }

  html, body, [class*="css"] {
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display",
                 "SF Pro Text", "Helvetica Neue", Arial, sans-serif;
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

  [data-testid="collapsedControl"] {
    visibility: visible !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    position: fixed !important;
    top: 14px !important;
    left: 14px !important;
    z-index: 999999 !important;
    width: 44px !important;
    height: 44px !important;
    border-radius: 14px !important;
    background: rgba(255, 255, 255, 0.88) !important;
    backdrop-filter: blur(18px) !important;
    -webkit-backdrop-filter: blur(18px) !important;
    border: 1px solid rgba(60, 60, 67, 0.12) !important;
    box-shadow: 0 8px 24px rgba(0,0,0,.10) !important;
  }

  [data-testid="collapsedControl"] svg {
    color: #1C1C1E !important;
  }

  [data-testid="stSidebar"] {
    background: rgba(255, 255, 255, 0.92) !important;
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    border-right: 1px solid var(--ios-border);
  }

  [data-testid="stAppViewContainer"] {
    background:
      radial-gradient(circle at 20% 0%, rgba(0, 122, 255, 0.16), transparent 32%),
      radial-gradient(circle at 90% 20%, rgba(52, 199, 89, 0.12), transparent 28%),
      var(--ios-bg);
  }

  .block-container {
    max-width: 780px;
    padding: 1.2rem 1rem 4rem;
    margin: 0 auto;
  }

  .app-header {
    text-align: left;
    padding: 20px 4px 18px;
  }

  .eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 13px;
    font-weight: 700;
    color: var(--ios-blue);
    background: rgba(0, 122, 255, 0.10);
    border-radius: 999px;
    padding: 6px 10px;
    margin-bottom: 10px;
  }

  .app-header h1 {
    font-size: 40px;
    line-height: 1;
    margin: 0;
    letter-spacing: -1.4px;
    color: var(--ios-text);
    font-weight: 850;
  }

  .app-header p {
    margin: 8px 0 0;
    color: var(--ios-muted);
    font-size: 15px;
    line-height: 1.35;
  }

  .ios-card {
    background: rgba(255, 255, 255, 0.88);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    border: 1px solid var(--ios-border);
    border-radius: 28px;
    padding: 22px;
    margin-bottom: 16px;
    box-shadow:
      0 1px 2px rgba(0,0,0,.04),
      0 16px 40px rgba(0,0,0,.07);
  }

  .card-title {
    font-size: 20px;
    font-weight: 800;
    letter-spacing: -0.4px;
    color: var(--ios-text);
    margin: 0 0 12px;
  }

  .card-subtitle {
    color: var(--ios-muted);
    font-size: 14px;
    line-height: 1.4;
    margin-top: -4px;
    margin-bottom: 14px;
  }

  .counter-wrap {
    text-align: center;
    padding: 8px 0 14px;
  }

  .counter-number {
    display: block;
    font-size: 62px;
    line-height: 0.95;
    font-weight: 850;
    color: var(--ios-text);
    letter-spacing: -3px;
  }

  .counter-label {
    display: block;
    margin-top: 8px;
    font-size: 14px;
    color: var(--ios-muted);
    font-weight: 600;
  }

  .mini-help {
    font-size: 13px;
    color: var(--ios-muted);
    text-align: center;
    margin-top: 6px;
    margin-bottom: 4px;
  }

  .express-card {
    background:
      linear-gradient(135deg, rgba(52, 199, 89, 0.18), rgba(255,255,255,0.88));
    border: 1px solid rgba(52, 199, 89, 0.22);
  }

  .express-button button {
    background: var(--ios-green) !important;
    color: white !important;
    box-shadow: 0 8px 18px rgba(52, 199, 89, 0.28) !important;
  }

  .debt-box {
    background: rgba(255, 149, 0, 0.12);
    border: 1px solid rgba(255, 149, 0, 0.22);
    color: var(--ios-orange);
    border-radius: 20px;
    padding: 16px;
    text-align: center;
    margin-bottom: 12px;
  }

  .debt-number {
    font-size: 34px;
    font-weight: 850;
    letter-spacing: -1px;
  }

  .debt-label {
    font-size: 13px;
    font-weight: 700;
    color: var(--ios-muted);
    text-transform: uppercase;
    letter-spacing: 0.35px;
    margin-top: 4px;
  }

  div[data-testid="stButton"] > button {
    border-radius: 16px !important;
    min-height: 52px !important;
    font-size: 16px !important;
    font-weight: 750 !important;
    letter-spacing: -0.2px !important;
    border: none !important;
    transition: transform .08s ease, opacity .12s ease !important;
  }

  div[data-testid="stButton"] > button:hover {
    transform: scale(0.985);
    opacity: .92;
  }

  div[data-testid="stButton"] > button:active {
    transform: scale(0.96);
    opacity: .78;
  }

  button[kind="primary"] {
    background: var(--ios-blue) !important;
    color: white !important;
    box-shadow: 0 8px 18px rgba(0, 122, 255, 0.24) !important;
  }

  button[kind="secondary"] {
    background: var(--ios-gray) !important;
    color: #2C2C2E !important;
  }

  .save-button button {
    background: var(--ios-blue) !important;
    color: white !important;
    box-shadow: 0 8px 18px rgba(0, 122, 255, 0.24) !important;
  }

  .debt-button button {
    background: var(--ios-orange) !important;
    color: white !important;
    box-shadow: 0 8px 18px rgba(255, 149, 0, 0.24) !important;
  }

  .sick-button button {
    background: rgba(255, 149, 0, 0.15) !important;
    color: var(--ios-orange) !important;
    border: 1px solid rgba(255, 149, 0, 0.26) !important;
  }

  div[data-testid="stNumberInput"] label,
  div[data-testid="stSlider"] label,
  div[data-testid="stSelectbox"] label {
    color: var(--ios-muted) !important;
    font-size: 13px !important;
    font-weight: 700 !important;
  }

  div[data-testid="stNumberInput"] input {
    border-radius: 14px !important;
    border: 1px solid var(--ios-border) !important;
    background: var(--ios-input) !important;
    min-height: 46px !important;
    font-size: 16px !important;
    color: var(--ios-text) !important;
  }

  [data-testid="stMetric"] {
    background: var(--ios-metric-bg);
    border: 1px solid var(--ios-border);
    border-radius: 20px;
    padding: 14px 16px;
  }

  [data-testid="stMetricLabel"] {
    color: var(--ios-muted);
    font-weight: 700;
  }

  [data-testid="stMetricValue"] {
    color: var(--ios-text);
    font-weight: 850;
  }

  [data-testid="stTabs"] button {
    border-radius: 999px !important;
    font-weight: 750 !important;
  }

  [data-testid="stTabs"] [aria-selected="true"] {
    color: var(--ios-blue) !important;
  }

  .calendar-grid {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 8px;
    margin-top: 12px;
  }

  .calendar-cell {
    min-height: 54px;
    border-radius: 16px;
    padding: 8px 6px;
    text-align: center;
    border: 1px solid var(--ios-border);
    background: rgba(142, 142, 147, 0.10);
  }

  .calendar-day {
    font-size: 16px;
    font-weight: 850;
    color: var(--ios-text);
    line-height: 1;
  }

  .calendar-weekday {
    font-size: 11px;
    color: var(--ios-muted);
    font-weight: 750;
    margin-top: 5px;
  }

  .calendar-done {
    background: rgba(52, 199, 89, 0.18);
    border-color: rgba(52, 199, 89, 0.35);
  }

  .calendar-rest {
    background: rgba(255, 149, 0, 0.18);
    border-color: rgba(255, 149, 0, 0.35);
  }

  .calendar-missed {
    background: rgba(142, 142, 147, 0.09);
  }

  .calendar-today {
    outline: 2px solid var(--ios-blue);
  }

  .legend {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin-top: 12px;
    color: var(--ios-muted);
    font-size: 13px;
    font-weight: 650;
  }

  .dot {
    display: inline-block;
    width: 10px;
    height: 10px;
    border-radius: 99px;
    margin-right: 5px;
  }

  .dot-green { background: var(--ios-green); }
  .dot-orange { background: var(--ios-orange); }
  .dot-gray { background: var(--ios-muted); }

  .stSuccess, .stWarning, .stInfo {
    border-radius: 16px !important;
    border: none !important;
  }

  @media (prefers-color-scheme: dark) {
    :root {
      --ios-bg: #000000;
      --ios-card: #1C1C1E;
      --ios-text: #F2F2F7;
      --ios-muted: #98989D;
      --ios-gray: #2C2C2E;
      --ios-border: rgba(255, 255, 255, 0.12);
      --ios-input: #2C2C2E;
      --ios-metric-bg: rgba(28,28,30,0.70);
    }

    [data-testid="stAppViewContainer"] {
      background:
        radial-gradient(circle at 20% 0%, rgba(0, 122, 255, 0.18), transparent 32%),
        radial-gradient(circle at 90% 20%, rgba(52, 199, 89, 0.12), transparent 28%),
        var(--ios-bg);
    }

    [data-testid="stSidebar"] {
      background: rgba(28, 28, 30, 0.94) !important;
      border-right: 1px solid var(--ios-border);
    }

    [data-testid="collapsedControl"] {
      background: rgba(28, 28, 30, 0.88) !important;
      border: 1px solid rgba(255,255,255,0.12) !important;
      box-shadow: 0 8px 24px rgba(0,0,0,.35) !important;
    }

    [data-testid="collapsedControl"] svg {
      color: #F2F2F7 !important;
    }

    .ios-card {
      background: rgba(28, 28, 30, 0.88);
    }

    .express-card {
      background:
        linear-gradient(135deg, rgba(52, 199, 89, 0.16), rgba(28,28,30,0.88));
    }

    button[kind="secondary"] {
      background: #2C2C2E !important;
      color: #F2F2F7 !important;
    }
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

    # Formato nuevo
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

    hoy = date.today()
    return df[df["Fecha"].dt.date == hoy].copy()


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
    Guarda el ejercicio y evalúa si el total del día supera el récord histórico.
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
        if "pr_messages" not in st.session_state:
            st.session_state.pr_messages = []

        if tipo == TIPO_PLANCHA:
            valor = format_seconds(total_despues_hoy)
        else:
            valor = str(total_despues_hoy)

        st.session_state.pr_messages.append(
            f"¡NUEVO RÉCORD PERSONAL! 🔥 {tipo}: {valor}"
        )
        st.session_state.show_balloons = True


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

    temp["Dia"] = temp["Fecha"].dt.strftime("%d/%m")

    resumen = temp.groupby("Dia", as_index=False)["Cantidad"].sum()
    return resumen.set_index("Dia")


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

    temp["Dia"] = temp["Fecha"].dt.strftime("%d/%m")

    temp = temp.sort_values("Fecha")
    resumen = temp.groupby("Dia", as_index=False)["Peso"].last()

    return resumen.set_index("Dia")


def fechas_activas(df: pd.DataFrame) -> set:
    if df.empty:
        return set()

    temp = df[df["Tipo_Ejercicio"].isin(TIPOS_RACHA)].copy()

    if temp.empty:
        return set()

    # Flexiones/plancha cuentan si cantidad > 0.
    # Sick Day cuenta aunque cantidad sea 0.
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


def generar_calendario_html(df: pd.DataFrame, dias: int = 28) -> str:
    activas = fechas_activas(df)
    descansos = fechas_descanso(df)

    inicio = date.today() - timedelta(days=dias - 1)
    hoy = date.today()

    dias_semana = ["L", "M", "M", "J", "V", "S", "D"]

    html = """
    <div class="legend">
      <span><span class="dot dot-green"></span>Completado</span>
      <span><span class="dot dot-orange"></span>Día libre</span>
      <span><span class="dot dot-gray"></span>Sin registro</span>
    </div>
    <div class="calendar-grid">
    """

    for i in range(dias):
        d = inicio + timedelta(days=i)

        clases = ["calendar-cell"]

        if d in descansos:
            clases.append("calendar-rest")
        elif d in activas:
            clases.append("calendar-done")
        else:
            clases.append("calendar-missed")

        if d == hoy:
            clases.append("calendar-today")

        clase_final = " ".join(clases)

        html += f"""
        <div class="{clase_final}">
          <div class="calendar-day">{d.day}</div>
          <div class="calendar-weekday">{dias_semana[d.weekday()]}</div>
        </div>
        """

    html += "</div>"

    return html


def descargar_csv(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8-sig")


def sync_deuda(source_key: str, target_key: str) -> None:
    st.session_state[target_key] = int(st.session_state.get(source_key, 0) or 0)


# ─────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────

if "guardado_ok" not in st.session_state:
    st.session_state.guardado_ok = False

if "deuda_saldada_ok" not in st.session_state:
    st.session_state.deuda_saldada_ok = False

if "express_ok" not in st.session_state:
    st.session_state.express_ok = False

if "sick_ok" not in st.session_state:
    st.session_state.sick_ok = False

if "show_balloons" not in st.session_state:
    st.session_state.show_balloons = False

if "pr_messages" not in st.session_state:
    st.session_state.pr_messages = []

if "deuda_pendiente_flexiones" not in st.session_state:
    st.session_state.deuda_pendiente_flexiones = 0

if "deuda_pendiente_plancha" not in st.session_state:
    st.session_state.deuda_pendiente_plancha = 0

if "deuda_input_version" not in st.session_state:
    st.session_state.deuda_input_version = 0

if "manual_input_version" not in st.session_state:
    st.session_state.manual_input_version = 0


# ─────────────────────────────────────────────────────────────
# SIDEBAR: PESO + RPE
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
peso_ultimo = peso_actual(df)
racha_actual = calcular_racha(df)

record_flexiones = max_historico_diario(df, TIPO_FLEXIONES, excluir_hoy=False)
record_plancha = max_historico_diario(df, TIPO_PLANCHA, excluir_hoy=False)


# ─────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────

st.markdown("""
<div class="app-header">
  <div class="eyebrow">Fitness log estructurado</div>
  <h1>Entreno diario</h1>
  <p>Control acumulado de flexiones, plancha, deuda, racha, peso y progreso.</p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# CONFETI + MENSAJES TEMPORALES
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

if st.session_state.deuda_saldada_ok:
    st.success("Deuda saldada y registrada correctamente.")
    st.session_state.deuda_saldada_ok = False

if st.session_state.sick_ok:
    st.success("Día libre registrado. La racha sigue viva.")
    st.session_state.sick_ok = False

if st.session_state.guardado_ok:
    st.success("Registro guardado correctamente.")
    st.session_state.guardado_ok = False


# ─────────────────────────────────────────────────────────────
# MÉTRICAS PRINCIPALES
# ─────────────────────────────────────────────────────────────

col_m1, col_m2, col_m3, col_m4 = st.columns(4)

with col_m1:
    st.metric(
        "Total de hoy",
        f"{flexiones_hoy} flex",
        delta=format_seconds(plancha_hoy)
    )

with col_m2:
    st.metric(
        "Deuda pendiente",
        f"{st.session_state.deuda_pendiente_flexiones} flex",
        delta=format_seconds(st.session_state.deuda_pendiente_plancha)
    )

with col_m3:
    if peso_ultimo is None:
        st.metric("Peso actual", "Sin dato")
    else:
        st.metric("Peso actual", f"{peso_ultimo:.1f} kg")

with col_m4:
    st.metric("Racha activa", f"{racha_actual} días")


# ─────────────────────────────────────────────────────────────
# TABS PRINCIPALES
# ─────────────────────────────────────────────────────────────

tab_entreno, tab_deuda, tab_peso, tab_analisis = st.tabs(
    [
        "Entreno",
        "Modo Oficina/Calle",
        "Peso",
        "Análisis"
    ]
)


# ─────────────────────────────────────────────────────────────
# TAB 1: ENTRENAMIENTO
# ─────────────────────────────────────────────────────────────

with tab_entreno:
    st.markdown('<div class="ios-card express-card">', unsafe_allow_html=True)
    st.markdown('<p class="card-title">Botón Express</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="card-subtitle">Para microbloques rápidos durante el día.</p>',
        unsafe_allow_html=True
    )

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

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="ios-card">', unsafe_allow_html=True)
    st.markdown('<p class="card-title">Flexiones</p>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="counter-wrap">
      <span class="counter-number">{flexiones_hoy}</span>
      <span class="counter-label">flexiones acumuladas hoy</span>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])

    with col1:
        if st.button("＋ Sumar 5 flexiones", type="primary", use_container_width=True, key="add_flex_5"):
            registrar_ejercicio_con_pr(
                tipo=TIPO_FLEXIONES,
                cantidad=5,
                peso=peso_ultimo,
                rpe=rpe_actual
            )
            st.session_state.guardado_ok = True
            st.rerun()

    manual_flex_key = f"manual_flexiones_{st.session_state.manual_input_version}"

    with col2:
        manual_flexiones = st.number_input(
            "Manual",
            min_value=0,
            max_value=2000,
            value=0,
            step=5,
            key=manual_flex_key,
            label_visibility="collapsed"
        )

    if st.button("Guardar flexiones escritas", use_container_width=True, key="save_manual_flex"):
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
            st.warning("Escribe una cantidad mayor que 0.")

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="ios-card">', unsafe_allow_html=True)
    st.markdown('<p class="card-title">Plancha</p>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="counter-wrap">
      <span class="counter-number">{format_seconds(plancha_hoy)}</span>
      <span class="counter-label">tiempo acumulado hoy</span>
    </div>
    """, unsafe_allow_html=True)

    col3, col4 = st.columns([3, 2])

    with col3:
        if st.button("＋ Sumar 10 segundos", type="primary", use_container_width=True, key="add_plancha_10"):
            registrar_ejercicio_con_pr(
                tipo=TIPO_PLANCHA,
                cantidad=10,
                peso=peso_ultimo,
                rpe=rpe_actual
            )
            st.session_state.guardado_ok = True
            st.rerun()

    manual_plancha_key = f"manual_plancha_{st.session_state.manual_input_version}"

    with col4:
        manual_plancha = st.number_input(
            "Manual",
            min_value=0,
            max_value=20000,
            value=0,
            step=10,
            key=manual_plancha_key,
            label_visibility="collapsed"
        )

    if st.button("Guardar segundos escritos", use_container_width=True, key="save_manual_plancha"):
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
            st.warning("Escribe una cantidad mayor que 0.")

    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# TAB 2: MODO OFICINA / CALLE
# ─────────────────────────────────────────────────────────────

with tab_deuda:
    st.markdown('<div class="ios-card">', unsafe_allow_html=True)
    st.markdown('<p class="card-title">Modo Oficina/Calle</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="card-subtitle">Anota lo que debes hacer después. Al saldar deuda, se guarda como registro normal en el CSV.</p>',
        unsafe_allow_html=True
    )

    st.markdown(f"""
    <div class="debt-box">
      <div class="debt-number">
        {st.session_state.deuda_pendiente_flexiones} flex / {format_seconds(st.session_state.deuda_pendiente_plancha)}
      </div>
      <div class="debt-label">Deuda pendiente actual</div>
    </div>
    """, unsafe_allow_html=True)

    deuda_version = st.session_state.deuda_input_version

    deuda_flex_key = f"deuda_flexiones_input_{deuda_version}"
    deuda_plancha_key = f"deuda_plancha_input_{deuda_version}"

    flexiones_pendientes = st.number_input(
        "Flexiones pendientes",
        min_value=0,
        max_value=2000,
        value=0,
        step=5,
        key=deuda_flex_key,
        on_change=sync_deuda,
        args=(deuda_flex_key, "deuda_pendiente_flexiones")
    )

    plancha_pendiente = st.number_input(
        "Segundos de Plancha pendientes",
        min_value=0,
        max_value=20000,
        value=0,
        step=10,
        key=deuda_plancha_key,
        on_change=sync_deuda,
        args=(deuda_plancha_key, "deuda_pendiente_plancha")
    )

    st.markdown('<div class="debt-button">', unsafe_allow_html=True)

    if st.button("Saldar Deuda", use_container_width=True, key="saldar_deuda"):
        if flexiones_pendientes > 0:
            registrar_ejercicio_con_pr(
                tipo=TIPO_FLEXIONES,
                cantidad=int(flexiones_pendientes),
                peso=peso_ultimo,
                rpe=rpe_actual
            )

        if plancha_pendiente > 0:
            registrar_ejercicio_con_pr(
                tipo=TIPO_PLANCHA,
                cantidad=int(plancha_pendiente),
                peso=peso_ultimo,
                rpe=rpe_actual
            )

        if flexiones_pendientes > 0 or plancha_pendiente > 0:
            st.session_state.deuda_pendiente_flexiones = 0
            st.session_state.deuda_pendiente_plancha = 0
            st.session_state.deuda_input_version += 1
            st.session_state.deuda_saldada_ok = True
            st.rerun()
        else:
            st.warning("No ingresaste deuda para saldar.")

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# TAB 3: PESO
# ─────────────────────────────────────────────────────────────

with tab_peso:
    st.markdown('<div class="ios-card">', unsafe_allow_html=True)
    st.markdown('<p class="card-title">Peso y composición</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="card-subtitle">Registra tu peso diario desde la barra lateral. El gráfico muestra la evolución de los últimos 7 días.</p>',
        unsafe_allow_html=True
    )

    peso_df = preparar_peso_semanal(df)

    if not peso_df.empty:
        st.line_chart(
            peso_df,
            use_container_width=True,
            height=240
        )
    else:
        st.info("Aún no hay suficientes registros de peso para graficar.")

    if peso_ultimo is not None:
        st.metric("Último peso registrado", f"{peso_ultimo:.1f} kg")

    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# TAB 4: ANÁLISIS
# ─────────────────────────────────────────────────────────────

with tab_analisis:
    st.markdown('<div class="ios-card">', unsafe_allow_html=True)
    st.markdown('<p class="card-title">Récords personales</p>', unsafe_allow_html=True)

    col_pr1, col_pr2, col_pr3 = st.columns(3)

    with col_pr1:
        st.metric("PR Flexiones", f"{record_flexiones} reps")

    with col_pr2:
        st.metric("PR Plancha", format_seconds(record_plancha))

    with col_pr3:
        st.metric("Racha actual", f"{racha_actual} días")

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="ios-card">', unsafe_allow_html=True)
    st.markdown('<p class="card-title">Calendario de cumplimiento</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="card-subtitle">Últimos 28 días. Verde = entreno registrado. Naranjo = día libre justificado.</p>',
        unsafe_allow_html=True
    )

    st.markdown(
        generar_calendario_html(df, dias=28),
        unsafe_allow_html=True
    )

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="ios-card">', unsafe_allow_html=True)
    st.markdown('<p class="card-title">Progreso diario: Flexiones</p>', unsafe_allow_html=True)

    flex_chart = preparar_progreso_diario(df, TIPO_FLEXIONES, dias=14)

    if not flex_chart.empty:
        st.bar_chart(
            flex_chart,
            use_container_width=True,
            height=240
        )
    else:
        st.info("Aún no hay registros de flexiones para graficar.")

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="ios-card">', unsafe_allow_html=True)
    st.markdown('<p class="card-title">Progreso diario: Plancha</p>', unsafe_allow_html=True)

    plancha_chart = preparar_progreso_diario(df, TIPO_PLANCHA, dias=14)

    if not plancha_chart.empty:
        st.bar_chart(
            plancha_chart,
            use_container_width=True,
            height=240
        )
    else:
        st.info("Aún no hay registros de plancha para graficar.")

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="ios-card">', unsafe_allow_html=True)
    st.markdown('<p class="card-title">Base de datos</p>', unsafe_allow_html=True)

    st.caption("Formato backend: Fecha, Tipo_Ejercicio, Cantidad, Peso, RPE_Esfuerzo.")

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

    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# DÍA LIBRE / SICK DAY
# ─────────────────────────────────────────────────────────────

st.markdown('<div class="ios-card">', unsafe_allow_html=True)
st.markdown('<p class="card-title">Día Libre / Sick Day</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="card-subtitle">Úsalo solo cuando realmente quieras mantener la racha sin sumar repeticiones.</p>',
    unsafe_allow_html=True
)

st.markdown('<div class="sick-button">', unsafe_allow_html=True)

if st.button("Día Libre / Sick Day 🤒", use_container_width=True):
    agregar_registro(
        tipo=TIPO_DESCANSO,
        cantidad=0,
        peso=peso_ultimo,
        rpe=None
    )

    st.session_state.sick_ok = True
    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

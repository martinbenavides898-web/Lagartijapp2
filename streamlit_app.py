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
    initial_sidebar_state="expanded",
)

DATA_FILE = "data_lagartijas.csv"
OLD_DATA_FILE = "data_entreno.csv"

COLUMNAS = ["Fecha", "Tipo_Ejercicio", "Cantidad", "Peso", "RPE_Esfuerzo"]

TIPO_FLEXIONES = "Flexiones"
TIPO_PLANCHA = "Plancha"
TIPO_PESO = "Peso"


# ─────────────────────────────────────────────────────────────
# ESTILO APPLE / MODERNO
# ─────────────────────────────────────────────────────────────

st.markdown("""
<style>
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
  }

  html, body, [class*="css"] {
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display",
                 "SF Pro Text", "Helvetica Neue", Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
  }

  #MainMenu, footer, header {
    visibility: hidden;
  }

  .stDeployButton {
    display: none;
  }

  [data-testid="stAppViewContainer"] {
    background:
      radial-gradient(circle at 20% 0%, rgba(0, 122, 255, 0.16), transparent 32%),
      radial-gradient(circle at 90% 20%, rgba(52, 199, 89, 0.12), transparent 28%),
      var(--ios-bg);
  }

  .block-container {
    max-width: 760px;
    padding: 1.4rem 1rem 4rem;
    margin: 0 auto;
  }

  .app-header {
    text-align: left;
    padding: 18px 4px 18px;
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
    font-size: 76px;
    line-height: 0.95;
    font-weight: 850;
    color: var(--ios-text);
    letter-spacing: -3.5px;
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

  .debt-box {
    background: rgba(255, 59, 48, 0.10);
    border: 1px solid rgba(255, 59, 48, 0.18);
    color: var(--ios-red);
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

  .ok-box {
    background: rgba(52, 199, 89, 0.12);
    border: 1px solid rgba(52, 199, 89, 0.20);
    color: var(--ios-green);
    border-radius: 20px;
    padding: 16px;
    text-align: center;
    margin-bottom: 12px;
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
    background: var(--ios-green) !important;
    color: white !important;
    box-shadow: 0 8px 18px rgba(52, 199, 89, 0.24) !important;
  }

  .debt-button button {
    background: var(--ios-orange) !important;
    color: white !important;
    box-shadow: 0 8px 18px rgba(255, 149, 0, 0.24) !important;
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
    background: #FAFAFA !important;
    min-height: 46px !important;
    font-size: 16px !important;
  }

  [data-testid="stMetric"] {
    background: rgba(255,255,255,0.70);
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
    }

    [data-testid="stAppViewContainer"] {
      background:
        radial-gradient(circle at 20% 0%, rgba(0, 122, 255, 0.18), transparent 32%),
        radial-gradient(circle at 90% 20%, rgba(52, 199, 89, 0.12), transparent 28%),
        var(--ios-bg);
    }

    .ios-card {
      background: rgba(28, 28, 30, 0.88);
    }

    div[data-testid="stNumberInput"] input {
      background: #2C2C2E !important;
      color: #F2F2F7 !important;
    }

    button[kind="secondary"] {
      background: #2C2C2E !important;
      color: #F2F2F7 !important;
    }

    [data-testid="stMetric"] {
      background: rgba(28,28,30,0.70);
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
    """
    Deja cualquier archivo antiguo en el formato nuevo:
    Fecha, Tipo_Ejercicio, Cantidad, Peso, RPE_Esfuerzo
    """

    if df.empty:
        return crear_df_vacio()

    # Caso nuevo
    if all(col in df.columns for col in COLUMNAS):
        out = df[COLUMNAS].copy()

    # Caso antiguo 1: fecha, cantidad
    elif "fecha" in df.columns and "cantidad" in df.columns:
        out = pd.DataFrame({
            "Fecha": df["fecha"],
            "Tipo_Ejercicio": TIPO_FLEXIONES,
            "Cantidad": df["cantidad"],
            "Peso": None,
            "RPE_Esfuerzo": None,
        })

    # Caso antiguo 2: fecha, lagartijas, plancha_segundos
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


def guardar_df(df: pd.DataFrame) -> None:
    df = normalizar_df(df)
    df.to_csv(DATA_FILE, index=False)


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


def deuda_texto(hecho: int, meta: int, unidad: str) -> str:
    deuda = hecho - meta

    if unidad == "seg":
        return format_seconds(abs(deuda))

    return str(abs(deuda))


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

    # Si hay más de un peso en el día, se queda con el último
    temp = temp.sort_values("Fecha")
    resumen = temp.groupby("Dia", as_index=False)["Peso"].last()

    return resumen.set_index("Dia")


def descargar_csv(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8-sig")


# ─────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────

if "flexiones_actuales" not in st.session_state:
    st.session_state.flexiones_actuales = 0

if "plancha_actual" not in st.session_state:
    st.session_state.plancha_actual = 0

if "guardado_ok" not in st.session_state:
    st.session_state.guardado_ok = False

if "deuda_saldada_ok" not in st.session_state:
    st.session_state.deuda_saldada_ok = False


# ─────────────────────────────────────────────────────────────
# SIDEBAR: CONFIGURACIÓN + PESO
# ─────────────────────────────────────────────────────────────

df = cargar_datos()

st.sidebar.markdown("## Configuración diaria")

meta_flexiones = st.sidebar.number_input(
    "Meta diaria de flexiones",
    min_value=0,
    max_value=2000,
    value=50,
    step=5
)

meta_plancha = st.sidebar.number_input(
    "Meta diaria de plancha (segundos)",
    min_value=0,
    max_value=20000,
    value=120,
    step=10
)

st.sidebar.markdown("---")
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
        st.sidebar.success("Peso guardado.")
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

flexiones_guardadas_hoy = total_hoy(df, TIPO_FLEXIONES)
plancha_guardada_hoy = total_hoy(df, TIPO_PLANCHA)

flexiones_hechas_hoy = flexiones_guardadas_hoy + st.session_state.flexiones_actuales
plancha_hecha_hoy = plancha_guardada_hoy + st.session_state.plancha_actual

deuda_flexiones = flexiones_hechas_hoy - meta_flexiones
deuda_plancha = plancha_hecha_hoy - meta_plancha

peso_ultimo = peso_actual(df)


# ─────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────

st.markdown("""
<div class="app-header">
  <div class="eyebrow">Fitness log estructurado</div>
  <h1>Entreno diario</h1>
  <p>Control de flexiones, plancha, deuda diaria, peso y progreso.</p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# MÉTRICAS PRINCIPALES
# ─────────────────────────────────────────────────────────────

col_m1, col_m2, col_m3 = st.columns(3)

with col_m1:
    st.metric(
        "Hecho hoy",
        f"{flexiones_hechas_hoy} flex / {format_seconds(plancha_hecha_hoy)}"
    )

with col_m2:
    deuda_flex_txt = f"{deuda_flexiones}" if deuda_flexiones < 0 else f"+{deuda_flexiones}"
    deuda_plancha_txt = f"{deuda_plancha}s" if deuda_plancha < 0 else f"+{deuda_plancha}s"

    st.metric(
        "Pendiente / Deuda",
        f"{deuda_flex_txt} flex",
        delta=deuda_plancha_txt
    )

with col_m3:
    if peso_ultimo is None:
        st.metric("Peso actual", "Sin dato")
    else:
        st.metric("Peso actual", f"{peso_ultimo:.1f} kg")


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
    st.markdown('<div class="ios-card">', unsafe_allow_html=True)
    st.markdown('<p class="card-title">Flexiones</p>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="counter-wrap">
      <span class="counter-number">{st.session_state.flexiones_actuales}</span>
      <span class="counter-label">flexiones en sesión actual</span>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])

    with col1:
        if st.button("＋ Sumar 5 flexiones", type="primary", use_container_width=True):
            st.session_state.flexiones_actuales += 5
            st.session_state.guardado_ok = False
            st.rerun()

    with col2:
        if st.button("↺", use_container_width=True, key="reset_flex"):
            st.session_state.flexiones_actuales = 0
            st.session_state.guardado_ok = False
            st.rerun()

    manual_flexiones = st.number_input(
        "Agregar flexiones manualmente",
        min_value=0,
        max_value=2000,
        value=0,
        step=5,
        key="manual_flexiones"
    )

    if st.button("Sumar flexiones escritas", use_container_width=True):
        if manual_flexiones > 0:
            st.session_state.flexiones_actuales += int(manual_flexiones)
            st.session_state.guardado_ok = False
            st.rerun()
        else:
            st.warning("Escribe una cantidad mayor que 0.")

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="ios-card">', unsafe_allow_html=True)
    st.markdown('<p class="card-title">Plancha</p>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="counter-wrap">
      <span class="counter-number">{format_seconds(st.session_state.plancha_actual)}</span>
      <span class="counter-label">tiempo de plancha en sesión actual</span>
    </div>
    """, unsafe_allow_html=True)

    col3, col4 = st.columns([3, 1])

    with col3:
        if st.button("＋ Sumar 10 segundos", type="primary", use_container_width=True):
            st.session_state.plancha_actual += 10
            st.session_state.guardado_ok = False
            st.rerun()

    with col4:
        if st.button("↺", use_container_width=True, key="reset_plancha"):
            st.session_state.plancha_actual = 0
            st.session_state.guardado_ok = False
            st.rerun()

    manual_plancha = st.number_input(
        "Agregar segundos de plancha manualmente",
        min_value=0,
        max_value=20000,
        value=0,
        step=10,
        key="manual_plancha"
    )

    if st.button("Sumar segundos escritos", use_container_width=True):
        if manual_plancha > 0:
            st.session_state.plancha_actual += int(manual_plancha)
            st.session_state.guardado_ok = False
            st.rerun()
        else:
            st.warning("Escribe una cantidad mayor que 0.")

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="save-button">', unsafe_allow_html=True)

    if st.button("Guardar sesión del día", use_container_width=True):
        if st.session_state.flexiones_actuales > 0:
            agregar_registro(
                tipo=TIPO_FLEXIONES,
                cantidad=st.session_state.flexiones_actuales,
                peso=peso_ultimo,
                rpe=rpe_actual
            )

        if st.session_state.plancha_actual > 0:
            agregar_registro(
                tipo=TIPO_PLANCHA,
                cantidad=st.session_state.plancha_actual,
                peso=peso_ultimo,
                rpe=rpe_actual
            )

        if st.session_state.flexiones_actuales > 0 or st.session_state.plancha_actual > 0:
            st.session_state.flexiones_actuales = 0
            st.session_state.plancha_actual = 0
            st.session_state.guardado_ok = True
            st.rerun()
        else:
            st.warning("No hay nada que guardar todavía.")

    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.guardado_ok:
        st.success("Sesión guardada correctamente.")


# ─────────────────────────────────────────────────────────────
# TAB 2: MODO OFICINA / CALLE
# ─────────────────────────────────────────────────────────────

with tab_deuda:
    st.markdown('<div class="ios-card">', unsafe_allow_html=True)
    st.markdown('<p class="card-title">Modo Oficina/Calle</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="card-subtitle">Úsalo cuando estés fuera y quieras dejar registrada una deuda o saldar ejercicios hechos en bloques chicos.</p>',
        unsafe_allow_html=True
    )

    deuda_flex_real = meta_flexiones - flexiones_hechas_hoy
    deuda_plancha_real = meta_plancha - plancha_hecha_hoy

    if deuda_flex_real <= 0 and deuda_plancha_real <= 0:
        st.markdown("""
        <div class="ok-box">
          <div class="debt-number">Meta saldada</div>
          <div class="debt-label">No tienes deuda pendiente</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="debt-box">
          <div class="debt-number">-{max(deuda_flex_real, 0)} flex / -{format_seconds(max(deuda_plancha_real, 0))}</div>
          <div class="debt-label">Deuda contra la meta diaria</div>
        </div>
        """, unsafe_allow_html=True)

    flexiones_pendientes = st.number_input(
        "Flexiones pendientes",
        min_value=0,
        max_value=2000,
        value=max(deuda_flex_real, 0),
        step=5
    )

    plancha_pendiente = st.number_input(
        "Segundos de Plancha pendientes",
        min_value=0,
        max_value=20000,
        value=max(deuda_plancha_real, 0),
        step=10
    )

    st.info(
        "Cuando presiones “Saldar Deuda”, esos valores se agregarán al registro final del día como ejercicio completado."
    )

    st.markdown('<div class="debt-button">', unsafe_allow_html=True)

    if st.button("Saldar Deuda", use_container_width=True):
        if flexiones_pendientes > 0:
            agregar_registro(
                tipo=TIPO_FLEXIONES,
                cantidad=int(flexiones_pendientes),
                peso=peso_ultimo,
                rpe=rpe_actual
            )

        if plancha_pendiente > 0:
            agregar_registro(
                tipo=TIPO_PLANCHA,
                cantidad=int(plancha_pendiente),
                peso=peso_ultimo,
                rpe=rpe_actual
            )

        if flexiones_pendientes > 0 or plancha_pendiente > 0:
            st.session_state.deuda_saldada_ok = True
            st.rerun()
        else:
            st.warning("No ingresaste deuda para saldar.")

    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.deuda_saldada_ok:
        st.success("Deuda saldada y agregada al registro del día.")

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
        label="Descargar base completa CSV",
        data=descargar_csv(df),
        file_name="data_lagartijas.csv",
        mime="text/csv",
        use_container_width=True
    )

    st.markdown('</div>', unsafe_allow_html=True)
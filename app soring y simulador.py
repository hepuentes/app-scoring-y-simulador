import streamlit as st

# Función de autenticación básica
def check_password():
    """Devuelve True si la contraseña ingresada es correcta."""
    def password_entered():
        if st.session_state["password"] == "test123":
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # No guardar la contraseña en el estado
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # Mostrar entrada para contraseña en el primer intento
        st.text_input("Contraseña", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.error("Contraseña incorrecta. Inténtalo de nuevo.")
        return False
    else:
        return True

# Funciones para el scoring
def calcular_puntaje(ingresos, edad, historial_crediticio):
    """Calcula el puntaje del cliente."""
    puntaje = ingresos * 0.2 + (edad * 5)
    if historial_crediticio == "Bueno":
        puntaje += 100
    elif historial_crediticio == "Regular":
        puntaje += 50
    return puntaje

def determinar_perfil_riesgo(puntaje):
    """Determina el perfil de riesgo basado en el puntaje."""
    if puntaje >= 700:
        return "Bajo"
    elif puntaje >= 500:
        return "Medio"
    else:
        return "Alto"

def determinar_tasa_interes(perfil_riesgo):
    """Asigna una tasa de interés según el perfil de riesgo."""
    if perfil_riesgo == "Bajo":
        return 10
    elif perfil_riesgo == "Medio":
        return 15
    else:
        return 20

# Inicio de la aplicación
if check_password():
    page = st.sidebar.selectbox("Selecciona la página", ["Configuración de Tasas", "Scoring Interno", "Simulador de Crédito", "Evaluación de Clientes"])

    if page == "Configuración de Tasas":
        st.title("Configuración de Tasas de Interés")
        if 'interest_rate' not in st.session_state:
            st.session_state['interest_rate'] = 19.0

        new_rate = st.number_input("Tasa de Interés (%)", value=st.session_state['interest_rate'])

        if st.button("Actualizar Tasa"):
            st.session_state['interest_rate'] = new_rate
            st.success(f"Tasa de interés actualizada a {new_rate}%")

    elif page == "Scoring Interno":
        st.title("Configuración del Scoring Interno")
        if 'score_threshold' not in st.session_state:
            st.session_state['score_threshold'] = 600

        new_threshold = st.number_input("Umbral de Scoring", value=st.session_state['score_threshold'])

        if st.button("Actualizar Umbral"):
            st.session_state['score_threshold'] = new_threshold
            st.success(f"Umbral de scoring actualizado a {new_threshold}")

    elif page == "Simulador de Crédito":
        st.title("Simulador de Crédito")
        interest_rate = st.session_state.get('interest_rate', 19.0)
        st.write(f"Tasa de Interés Actual: {interest_rate}%")
        monto = st.number_input("Monto del Crédito", min_value=0)
        plazo = st.number_input("Plazo (meses)", min_value=1)

        if st.button("Calcular"):
            cuota = monto * (1 + (interest_rate / 100)) / plazo
            st.write(f"Cuota Mensual: ${cuota:,.2f}")

    elif page == "Evaluación de Clientes":
        st.title("Evaluación de Clientes")
        ingresos = st.number_input("Ingresos mensuales", min_value=0)
        edad = st.number_input("Edad", min_value=18, max_value=100)
        historial_crediticio = st.selectbox("Historial crediticio", ["Bueno", "Regular", "Malo"])

        if st.button("Evaluar Cliente"):
            puntaje = calcular_puntaje(ingresos, edad, historial_crediticio)
            perfil_riesgo = determinar_perfil_riesgo(puntaje)
            tasa_interes = determinar_tasa_interes(perfil_riesgo)

            st.write(f"Puntaje del Cliente: {puntaje}")
            st.write(f"Perfil de Riesgo: {perfil_riesgo}")
            st.write(f"Tasa de Interés Recomendada: {tasa_interes}%")

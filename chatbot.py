import streamlit as st
from google import genai
from google.genai import types

# Configuración de la página web
st.set_page_config(page_title="Asistente Pedagógico IA", page_icon="🍎", layout="centered")
st.title("🍎 Asistente Pedagógico para Docentes")
st.markdown("Un espacio seguro para consultar estrategias de aula, dinámicas de grupo y apoyo socioemocional.")

# 1. Configura tu llave maestra
mi_clave = "AQ.Ab8RN6II46aBHC58qb_BO3Wz5TWb6b2fZa9mTLqOhZ01lSZJuw"

instrucciones_docente = """
Eres un asesor pedagógico y especialista en psicología educativa, cálido, empático y práctico. 
Tu objetivo es ayudar a los docentes a conectar mejor con sus estudiantes, mejorar el clima del aula, 
fomentar la participación de alumnos tímidos o desmotivados y ofrecer estrategias de estudio efectivas.
Da consejos concretos, dinámicas fáciles de aplicar en clase y mantén siempre un tono de apoyo colega a colega.
"""

# Función para iniciar o reiniciar el chat
def iniciar_chat():
    st.session_state.client = genai.Client(api_key=mi_clave)
    st.session_state.chat = st.session_state.client.chats.create(
        model='gemini-3.8-flash',
        config=types.GenerateContentConfig(
            system_instruction=instrucciones_docente,
            temperature=0.7
        )
    )
    st.session_state.mensajes = [
        {"role": "assistant", "content": "¡Hola, docente! Soy tu asistente pedagógico. ¿En qué te ayudo hoy con tu clase?"}
    ]

# 2. Guardar cliente y chat en la memoria si es la primera vez
if "client" not in st.session_state:
    iniciar_chat()

# --- BARRA LATERAL CON HERRAMIENTAS RÁPIDAS ---
pregunta_rapida = None

with st.sidebar:
    st.header("🧰 Caja de Herramientas")
    st.markdown("Haz clic en una opción para generar ideas al instante:")
    
    if st.button("🧊 Dinámica rompehielos (10 min)", use_container_width=True):
        pregunta_rapida = "Dame una dinámica rompehielos de 10 minutos para que mis estudiantes se suelten y participen más en clase."
        
    if st.button("🤫 Motivar alumnos tímidos", use_container_width=True):
        pregunta_rapida = "¿Qué estrategias prácticas puedo usar para integrar a los estudiantes muy callados sin hacerlos sentir incómodos?"
        
    if st.button("🧩 Inclusión y neurodiversidad", use_container_width=True):
        pregunta_rapida = "Dame 3 ajustes razonables y sencillos para apoyar la concentración y participación de un alumno neurodivergente en clase."
        
    if st.button("🧠 Técnicas de estudio activas", use_container_width=True):
        pregunta_rapida = "Sugiéreme una actividad dinámica para repasar un tema difícil antes del examen sin que sea una clase aburrida."

    st.divider()
    
    if st.button("🗑️ Nueva conversación", type="primary", use_container_width=True):
        iniciar_chat()
        st.rerun()

# 3. Mostrar el historial de mensajes con burbujas de chat
for msg in st.session_state.mensajes:
    icono = "🧑‍🏫" if msg["role"] == "user" else "🍎"
    with st.chat_message(msg["role"], avatar=icono):
        st.markdown(msg["content"])

# 4. Capturar la pregunta (ya sea escrita abajo o desde un botón lateral)
pregunta_escrita = st.chat_input("Escribe tu consulta o situación de clase aquí...")
pregunta = pregunta_rapida or pregunta_escrita

if pregunta:
    # Mostrar pregunta del docente
    st.session_state.mensajes.append({"role": "user", "content": pregunta})
    with st.chat_message("user", avatar="🧑‍🏫"):
        st.markdown(pregunta)

    # Generar y mostrar respuesta de la IA
    with st.chat_message("assistant", avatar="🍎"):
        with st.spinner("Pensando estrategias..."):
            try:
                response = st.session_state.chat.send_message(pregunta)
                st.markdown(response.text)
                st.session_state.mensajes.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Error exacto: {e}")
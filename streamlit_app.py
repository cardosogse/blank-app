import streamlit as st
import google.generativeai as genai

# Configurar la página
st.set_page_config(page_title="Tutor de Élite", page_icon="🧠", layout="centered")

# Recuperar la API Key desde los Secrets de Streamlit
api_key = st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("Por favor, configura tu GOOGLE_API_KEY en las credenciales secretas de Streamlit.")
else:
    genai.configure(api_key=api_key)
    
    st.title("🧠 Tutor de Élite AI")
    st.subheader("Tu mentor personalizado en Ciencias Biológicas y Veterinaria")

    # Inicializar el historial de chat si no existe
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "¡Hola, Sinaí! Estoy listo. ¿Qué concepto de biología, estadística o medicina veterinaria vamos a dominar hoy?"}
        ]

    # Mostrar los mensajes anteriores
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Entrada del usuario
    if user_query := st.chat_input("Escribe tu duda aquí..."):
        # Mostrar mensaje del usuario
        with st.chat_message("user"):
            st.write(user_query)
        st.session_state.messages.append({"role": "user", "content": user_query})

        # Generar respuesta de la IA
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            # Contexto del sistema implícito para guiar las respuestas de forma profesional
            full_prompt = f"Eres un Tutor de Élite, un mentor experto en ciencias biológicas, bioestadística y veterinaria. Responde de forma clara, rigurosa y didáctica a la consulta del usuario de manera que demuestre madurez profesional y rigor académico. Consulta: {user_query}"
            
            response = model.generate_content(full_prompt)
            
            # Mostrar respuesta del asistente
            with st.chat_message("assistant"):
                st.write(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            st.error(f"Hubo un error al conectar con Gemini: {e}")

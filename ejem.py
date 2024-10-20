import streamlit as st
from langchain_community.llms import Ollama
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import random

# CSS personalizado para mejorar el diseño visual
st.markdown("""
    <style>
    body {
        background-color: #f0f2f6; /* Fondo general suave */
    }
    .text-input-container {
        position: relative;
        width: 100%;
        display: flex;
        align-items: center;
        background-color: #ffffff;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }
    .text-input {
        width: 100%;
        padding-right: 40px;
    }
    .arrow {
        position: absolute;
        right: 10px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 20px;
        color: #007bff; /* Color de la flecha */
    }
    .chat-message {
        padding: 15px;
        border-radius: 12px;
        margin: 10px 0;
        max-width: 75%;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    .human-message {
        background-color: #f7f9fc; /* Fondo del mensaje humano */
        text-align: left;
        border-left: 4px solid #007bff; /* Línea de color azul a la izquierda */
    }
    .bot-message {
        background-color: #007bff;
        text-align: right;
        color: white;
        border-right: 4px solid #007bff; /* Línea azul a la derecha */
    }
    .container {
        display: flex;
        justify-content: space-between;
        margin: 10px 0;
    }
    /* Añadir sombra a las secciones de recursos */
    .resource-section {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    /* Mejorar el diseño del botón */
    .stButton button {
        background-color: #007bff;
        color: white;
        border-radius: 6px;
        padding: 10px 20px;
    }
    .stButton button:hover {
        background-color: #0056b3;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Inicialización del modelo LLaMA
llm = Ollama(model="llama3.1:latest")

# Lista de frases de apoyo emocional
frases_apoyo_emocional = [
    "Recuerda que los tiempos difíciles no duran para siempre, ¡tú puedes con esto!",
    "No estás solo, siempre hay alguien dispuesto a ayudarte.",
    "Todo pasa, incluso los momentos más oscuros.",
    "Eres más fuerte de lo que crees. Sigue adelante.",
    "Siempre hay una luz al final del túnel, confía en ti mismo.",
    "Respira profundamente y da un paso a la vez, lo lograrás.",
    "Es normal sentirse abrumado a veces, date permiso para descansar."
]

# Función para obtener una frase de apoyo emocional aleatoria
def obtener_frase_apoyo():
    return random.choice(frases_apoyo_emocional)

# Función principal que controla la lógica del asistente emocional
def main():
    # Título principal de la aplicación
    st.title("AI Padrino 🤖")

    # Sección donde el usuario puede introducir el nombre del asistente
    bot_name = st.text_input("Nombre de tu Asistente Virtual:", value="Bot")

    # Prompt o mensaje base que define el comportamiento del asistente
    prompt = f"""Hola, me llamo {bot_name}. Respondo preguntas con respuestas simples y hago preguntas personales para conocerte mejor. Estoy aquí para ofrecerte apoyo emocional y frases motivacionales cuando lo necesites. "Aquí estoy para ayudarte"."""

    # Área para mostrar y permitir que el usuario edite la descripción del asistente
    bot_description = st.text_area("Descripción de tu Asistente Virtual:", value=prompt)

    # Historial de chat que se mantiene en la sesión de Streamlit
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    # Configuración del prompt del asistente con Langchain
    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", bot_description),  # Mensaje inicial del sistema que define el comportamiento del asistente
            MessagesPlaceholder(variable_name="chat_history"),  # Historial de mensajes para mantener la conversación
            ("human", "{input}"),  # Mensaje que introduce el usuario en el chat
        ]
    )

    # Unir el template del prompt con el modelo de lenguaje (LLaMA)
    chain = prompt_template | llm

    # Contenedor para el input del usuario
    st.markdown("<div class='text-input-container'>", unsafe_allow_html=True)

    # Entrada del usuario para hacer preguntas o comentarios
    user_input = st.text_input("Escribe tu pregunta o cuéntame cómo te sientes:", key="user_input", on_change=lambda: process_input(st.session_state.user_input), placeholder="Escribe aquí...")

    # Procesar la entrada del usuario
    def process_input(input_text):
        # Comprobar si el usuario ha ingresado texto
        if input_text:
            # Si el usuario dice "adios", se detiene la aplicación
            if input_text.lower() == "adios":
                st.stop()
            else:
                # Si el usuario pide frases emocionales o motivacionales
                if any(phrase in input_text.lower() for phrase in ["frases emocionales", "frase de apoyo", "motivación", "frase motivacional"]):
                    frase_apoyo = obtener_frase_apoyo()  # Obtener frase motivacional
                    st.session_state["chat_history"].append(HumanMessage(content=input_text))  # Guardar mensaje del usuario
                    st.session_state["chat_history"].append(AIMessage(content=f"{bot_name}: {frase_apoyo}"))  # Respuesta del bot
                else:
                    # Si es otro tipo de mensaje, se envía al modelo LLaMA para generar una respuesta
                    response = chain.invoke({"input": input_text, "chat_history": st.session_state["chat_history"]})
                    st.session_state["chat_history"].append(HumanMessage(content=input_text))  # Guardar mensaje del usuario
                    st.session_state["chat_history"].append(AIMessage(content=response))  # Respuesta del bot

                # Si el usuario menciona un problema o emociones negativas, el asistente ofrece apoyo emocional
                if any(word in input_text.lower() for word in ["problema", "alcoholismo", "preocupación", "ansiedad", "estrés", "tristeza", "mal"]):
                    st.session_state["chat_history"].append(
                        AIMessage(content=f"{bot_name}: Parece que estás pasando por un momento difícil. ¿Te gustaría hablar más sobre eso?")
                    )
                    # Enviar una frase de apoyo emocional
                    frase_apoyo = obtener_frase_apoyo()
                    st.session_state["chat_history"].append(
                        AIMessage(content=f"{bot_name}: {frase_apoyo}")
                    )

                # Limpiar el campo de entrada después de procesar
                st.session_state.user_input = ""

    # Mostrar el historial del chat con diseño mejorado
    st.subheader("Chat")
    chat_container = st.empty()  # Contenedor para el historial de chat

    # Iterar sobre el historial y mostrar mensajes
    for msg in st.session_state["chat_history"]:
        if isinstance(msg, HumanMessage):
            # Estilo para el mensaje del usuario
            chat_container.markdown(f"<div class='chat-message human-message'><b>Humano:</b> {msg.content}</div>", unsafe_allow_html=True)
        elif isinstance(msg, AIMessage):
            # Estilo para el mensaje del asistente
            chat_container.markdown(f"<div class='chat-message bot-message'><b>{bot_name}:</b> {msg.content}</div>", unsafe_allow_html=True)

    # Sección de enlaces útiles
    st.subheader("Centros de ayuda")

    # Diccionario con enlaces útiles
    links = {
        "Gabriela Vizzi Merlo": "https://www.psychologytoday.com/mx/psicologos/gabriela-vizzi-merlo-ciudad-de-mexico-df/896968",
        "Alejandra Quintos Alonso": "https://www.psychologytoday.com/mx/psicologos/alejandra-quintos-alonso-ciudad-de-mexico-df/1199946 ",
        "Mónica Diaz Almazán": "https://www.psycho  logytoday.com/mx/psicologos/monica-diaz-almazan-ciudad-de-mexico-df/939986 ",
    }

    # Desplegable para que el usuario seleccione un enlace
    selected_link = st.selectbox("Selecciona un enlace para abrir:", options=list(links.keys()))

    # Botón para abrir el enlace seleccionado
    if st.button("Abrir enlace"):
        link_url = links[selected_link]
        st.write(f"Haz clic en el siguiente enlace: [Ir a {selected_link}]({link_url})")

# Ejecución principal de la aplicación
if __name__ == '__main__':
    main()
import streamlit as st
from groq import Groq


def initialize_groq_client(api_key):
    try:
        return Groq(api_key=api_key)
    except Exception as e:
        st.error(f"Error initializing Groq client: {e}")
        return None

def windy_assistant_response(client, input_text, context=None):
    system_prompt = f"""
    You are a smart assistant for a wind energy platform designed to provide useful information and solve queries related to wind energy. Your task is to answer questions from users about wind turbines, energy generation, environmental impact, efficiency, maintenance, and industry trends. 
Your responses should be concise, informative, and based on reliable data. Where applicable, include relevant metrics, tips, or industry standards. Some possible types of queries include:

1. **Wind Turbine Operation**: Explain how wind turbines generate energy and the factors affecting their performance (wind speed, turbine height, rotor size, etc.).
2. **Energy Generation Calculations**: Help users calculate potential energy output based on turbine specifications and wind conditions.
3. **Environmental Impact**: Provide information about the environmental benefits of wind energy, including reduction in carbon emissions and other environmental impacts.
4. **System Maintenance**: Advise on routine maintenance needs for wind turbines and common issues to look out for in wind energy systems.
5. **Cost and Investment**: Explain the cost-benefit analysis of wind energy investments, including upfront costs, long-term savings, and subsidies.
6. **Global Wind Energy Trends**: Provide updates on new technologies, global energy policies, or industry trends in wind energy.

Always ensure that your information is up-to-date, reliable, and tailored to the user's specific question.
    """

    conversation = f"{context}\nStudent: {input_text}\nAssistant:" if context else f"Student: {input_text}\nAssistant:"

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": conversation}
            ],
            model="llama3-70b-8192",
            temperature=0.5
        )
        response = chat_completion.choices[0].message.content
        return response
    except Exception as e:
        st.error(f"Error generating chat completion: {e}")
        return "An error occurred while generating the response."

# Streamlit app
def main():
    st.set_page_config(page_title="Windy", page_icon=":books:")

    st.title("Windy 💨")

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you today?"}]


    conversation_str = "\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in st.session_state.messages])
    for msg in st.session_state.messages:
        if msg["role"] == "assistant":
            st.chat_message("assistant").write(msg["content"])
        elif msg["role"] == "user":
            st.chat_message("user").write(msg["content"])


    user_input = st.chat_input("Enter your question or response:")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.chat_message("user").write(user_input)


        client_groq = initialize_groq_client("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")
        if client_groq is None:
            st.error("Failed to initialize the Groq client. Please check your API key.")
            st.stop()


        context = conversation_str

 
        try:
            full_response = windy_assistant_response(client_groq, user_input, context=context)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            st.chat_message("assistant").write(full_response)

        except Exception as e:
            st.error(f"An error occurred while generating the response: {e}")

if __name__ == "__main__":
    main()

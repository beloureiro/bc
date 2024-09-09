import streamlit as st  # Certifique-se de que esta linha esteja presente
import streamlit.components.v1 as components  # Importando o componente


def render_sequence_diagram():
    # Código Mermaid
    mermaid_code = """
    sequenceDiagram
        participant Inputs as 1 ⨠ Inputs ⨠
        participant Processes as 2 ⨠ Processes ⨠
        participant Outputs as 3 ⨠ Outputs ⨠
        participant Customer as 4 ⨠ Customer ⨠

        Note over Inputs: Trigger to start the process
        Note over Inputs,Processes: Processes entirely focus on transforming inputs into outputs
        Inputs->>+Processes: Process initiation
        Note over Processes: Steps that transform inputs into outputs
        Processes-->>+Outputs: Output Production
        Note over Outputs: Outputs prepared for delivery
        Outputs->>Customer: Deliver Outputs to Customer
        Note over Customer: Fulfilling the expected function communicated to the customer
    """

    # HTML com o script Mermaid e o diagrama
    html = f"""
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script>
        mermaid.initialize({{
            startOnLoad: true,
            theme: 'default',
            securityLevel: 'loose',
            fontFamily: 'Arial',
        }});
    </script>
    <div class="mermaid">
    {mermaid_code}
    </div>
    """

    # Renderiza o HTML
    components.html(html, height=600, scrolling=True)  # Aumentei a altura para acomodar o diagrama maior

    # Exibe o código Mermaid
    # st.code(mermaid_code, language="mermaid")

# Chame a função onde você precisar renderizar o diagrama

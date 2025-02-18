import streamlit as st
import requests

st.title("💡 AI Code Analysis & Auto-Fix Tool")

uploaded_file = st.file_uploader("📂 Upload a Code File", type=["py", "js", "cpp", "java", "c"])

if uploaded_file is not None:
    code_content = uploaded_file.getvalue().decode("utf-8")
    st.write(f"📄 **Analyzing:** `{uploaded_file.name}`")

    api_url = "http://127.0.0.1:5000/analyze"
    response = requests.post(api_url, json={"code": code_content})

    if response.status_code == 200:
        result = response.json().get("message", "No response from AI.")
        st.markdown(result)

        # Show corrected code only if the user has approved applying changes
        if st.button("✅ Approve & Apply Changes"):
            apply_url = "http://127.0.0.1:5000/apply_changes"
            apply_response = requests.post(apply_url, json={"code": code_content})

            if apply_response.status_code == 200:
                st.success(apply_response.json().get("message", "Changes applied successfully!"))
                
                # Display the corrected code on the UI
                corrected_code = apply_response.json().get("corrected_code")
                if corrected_code:
                    st.subheader("Corrected Code:")
                    st.code(corrected_code, language="python")  # Adjust language as needed (e.g., python, js, etc.)
            else:
                st.error("❌ Failed to apply changes.")
    else:
        st.error("❌ Error: Could not connect to the AI API.")
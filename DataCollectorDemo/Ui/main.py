import streamlit as st

SELECT_VIEW: str = "Select view"
HOME: str = "Home"
CONFIG_EDITOR: str = "Config Editor"
DASHBOARD: str = "Dashboard"
CLIENT: str = "Client"
SERVER: str = "OPC UA Server"
SERVICES: str = "Registered Services"

st.title("Microservice Demo")
st.text("(c) 2025 Dierck Matern, all rights reserved.")
st.divider()

pages = {
    SELECT_VIEW: [
        st.Page("Frames/page_services.py", title=SERVICES),
        st.Page("Frames/page_dashboard.py", title=DASHBOARD),
        st.Page("Frames/page_client.py", title=CLIENT),
        st.Page("Frames/page_editor.py", title=CONFIG_EDITOR),
        st.Page("Frames/page_server_control.py", title=SERVER)
    ]
}

pg = st.navigation(pages)
pg.run()



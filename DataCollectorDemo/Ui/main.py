import streamlit as st
import Communication
import asyncio

SELECT_VIEW: str = "Select view"
HOME: str = "Home"
CONFIG_EDITOR: str = "Config Editor"
DASHBOARD: str = "Dashboard"
CLIENT: str = "Client"

st.title("Microservice Demo")
st.text("(c) Dierck Matern, all rights reserved.")

pages = {
    SELECT_VIEW: [
        st.Page("Frames/page_dashboard.py", title=DASHBOARD),
        st.Page("Frames/page_client.py", title=CLIENT),
        st.Page("Frames/page_editor.py", title=CONFIG_EDITOR)
    ]
}

pg = st.navigation(pages)

services = asyncio.run(Communication.get_services_async())
st.text("Registered services:")
for s in services:
#
    st.markdown(
        f"""
        <div style="border:0px solid #d9dee9; padding:10px; border-radius:5px; background-color:#eff1f6; margin-bottom:10px">
            <strong>{s}</strong>
        </div>
        """,
    unsafe_allow_html=True)

pg.run()



if __name__ == '__main__':
    pass
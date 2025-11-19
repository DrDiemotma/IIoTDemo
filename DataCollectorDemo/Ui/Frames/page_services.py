import streamlit as st
import asyncio
from Ui import Communication

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
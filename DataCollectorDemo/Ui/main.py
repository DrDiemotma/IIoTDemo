import streamlit as st

SELECT_VIEW: str = "Select view"
HOME: str = "Home"
CONFIG_EDITOR: str = "Config Editor"
DASHBOARD: str = "Dashboard"
CLIENT: str = "Client"

def main():
    pages = {
        SELECT_VIEW: [
            st.Page("Frames/page_dashboard.py", title=DASHBOARD),
            st.Page("Frames/page_client.py", title=CLIENT),
            st.Page("Frames/page_editor.py", title=CONFIG_EDITOR)
        ]
    }

    pg = st.navigation(pages)
    pg.run()


if __name__ == '__main__':
    main()
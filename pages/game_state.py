import streamlit as st
import utils_and_widgets as utils

st.markdown("# 🔧 Game State")
st.caption("Developer page, for peering behind the scenes")

if "debug_history" in st.session_state:
    history = ""
    for event in st.session_state.debug_history:
        history += f"> {event}\n\n"
    utils.custom_scroller(history, 600)

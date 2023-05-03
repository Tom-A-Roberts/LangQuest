import streamlit as st
import utils_and_widgets as utils

st.markdown("# 🔧 Game State")
st.caption("Developer page, for peering behind the scenes")

if "compute_state" in st.session_state:
    st.markdown(f"Current game state: `{st.session_state.game_state.name}`")

if "debug_history" in st.session_state:
    history = ""
    for event in st.session_state.debug_history:
        history += f"> {event}\n\n"
    utils.custom_scroller(history, 600)


if "player_2" in st.session_state:
    with st.sidebar:
        st.markdown("# Player 2 (AI) Status")
        my_bar = st.progress(
            st.session_state.player_2.health,
            text=f"❤️ :red[Health]: {st.session_state.player_2.health}/{st.session_state.player_2.max_health}",
        )
        st.markdown(f"### Player 2 (AI) Location:")
        st.markdown(f"{st.session_state.player_2.location}")
        st.markdown(f"### Player 2 (AI) Inventory:")
        inventory_output_string = ""
        for item in st.session_state.player_2.items:
            inventory_output_string += f"- {item}\n"
        if inventory_output_string == "":
            inventory_output_string = "(Empty)"
        st.markdown(inventory_output_string)
else:
    with st.sidebar:
        st.markdown("# Player 2 (AI) Status")
        my_bar = st.progress(0, text=f"❤️ :red[Health]: N/A")
        st.markdown(f"### Player 2 (AI) Location:")
        st.markdown(f"No location yet.")
        st.markdown(f"### Player 2 (AI) Inventory:\n(Empty)")
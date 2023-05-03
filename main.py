import pathlib
import streamlit as st
from PIL import Image, ImageOps
import entities
import utils_and_widgets as utils
from enum import Enum
import langchain_functions as lang

st.set_page_config(
    page_title="LangQuest",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "Created by Tom Roberts: https://github.com/Tom-A-Roberts"},
)

skip_intro = False


with open(pathlib.Path("content/style.css")) as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)


@st.cache_data
def get_image(image_path: str, grayscale: bool = False):
    image = Image.open(image_path)
    if grayscale:
        image = ImageOps.grayscale(image)
    return image


main_title_image = get_image("content/LangQuestTitle.jpeg")
starting_image = get_image("content/Starting_Image.jpeg", grayscale=True)
secondary_title_image = get_image("content/TitleSmaller.jpeg")

@st.cache_resource
class GameState(Enum):
    WAITING_TO_START = 1
    DUNGEON_MASTER_COMPUTING = 2
    WAITING_FOR_PLAYER = 3
    WAITING_FOR_AI = 4

# Initialize session state
if "compute_state" not in st.session_state:
    st.session_state.compute_state = ""

if "game_state" not in st.session_state:
    st.session_state.game_state = GameState.WAITING_TO_START.value

if "turn_number" not in st.session_state:
    st.session_state.turn_number = 0

if "latest_image" not in st.session_state:
    st.session_state.latest_image = starting_image

if "dungeon_master_thoughts" not in st.session_state:
    st.session_state.dungeon_master_thoughts = ""

if "user_input" not in st.session_state:
    st.session_state.user_input = ""

if "debug_history" not in st.session_state:
    st.session_state.debug_history = []

if "compute_progress" not in st.session_state:
    st.session_state.compute_progress = 0

if "has_password" not in st.session_state:
    if st.secrets._secrets is None or "use_password" not in st.secrets:
        st.session_state.has_password = True
    else:
        if st.secrets["use_password"].strip().lower() == "false":
            st.session_state.has_password = True
            lang.api_key.set_key(st.secrets["api_key"])
        else:
            st.session_state.has_password = False

if "entered_pass_this_session" not in st.session_state:
    st.session_state.entered_pass_this_session = False

# Set up sidebar
if "dungeon_master" in st.session_state:
    with st.sidebar:
        st.markdown("## Session Summary")
        scrollbar_text = ""
        for i in range(len(st.session_state.dungeon_master.player_summaries)):
            scrollbar_text += (
                f"><span class='player-1'>Player 1:</span> {st.session_state.dungeon_master.player_summaries[i]}\n"
            )
        scrollbar_text = scrollbar_text[:-1]
        utils.custom_scroller(scrollbar_text, height=500)
else:
    with st.sidebar:
        scrollbar_text = "> Waiting for game to start..."
        utils.custom_scroller(scrollbar_text, height=500)

# Set up initial intro page
if st.session_state.game_state == GameState.WAITING_TO_START.value:
    st.markdown(
        "<p style = 'text-align: center; color: grey;' > " + utils.img_to_html(main_title_image, 550) + "</p> ",
        unsafe_allow_html=True,
    )


    if not st.session_state.has_password:
        pass_input = st.text_input("Enter the password in order to access the API Key", key="player_password")
        if pass_input == st.secrets["app_password"]:
            st.session_state.has_password = True
            st.session_state.entered_pass_this_session = True
            lang.api_key.set_key(st.secrets["api_key"])
            st._rerun()
    if st.session_state.entered_pass_this_session:
        st.info("Password accepted")


    with st.expander("Game Settings", expanded=False):
        st.write("This will change what setup is given to the AI Dungeon Master.")
        scene_tab, player_tab = st.tabs(["Scene", "Player 1"])
        with scene_tab:
            world_desc = st.text_area(
                "Description of World",
                """The village of Laketown is a precarious place to live."""
                """ Built on wooden stilts above a vast lake, it is constantly threatened by floods, storms, and aquatic monsters."""
                """ Since village is entirely surrounded by water, the villagers scrape by on fishing, trading, and crafting goods from whatever materials they can scavenge."""
                """ They also face constant attacks from goblins, orcs, and other foes who crave their resources and loot. Currently, the village is peaceful.""",
                height=200,
            )
        with player_tab:
            player_description = st.text_area(
                "Player 1's Character Description",
                """You are a hunter and a craftsman in Laketown."""
                """ You have learned how to track, trap, and kill various animals that live around the lake."""
                """ You also know how to use their skins, bones, and meat to make useful items such as clothing, weapons, and food."""
                """ You are brave, resourceful, and loyal to your fellow villagers."""
                """ You have a personal vendetta against goblins, who killed your family when you were young.""",
                height=200,
            )
            player_items = st.text_area(
                "Player 1's Starting Items",
                """A rickety hatchet made from a broken axe and a stick\n"""
                """A hunting knife made from deer antlers and iron\n"""
                """A fishing rod and a net made from reeds and rope\n"""
                """A leather jacket and trousers made from wolf skin\n"""
                """A pouch of dried meat and berries\n"""
                """A flask of water""",
                height=200,
            )
            player_objective = st.text_area(
                "Player 1's Objective",
                "Find and defeat the Goblin before he can sabotage Laketown or flee with valuable loot.",
                height=50,
            )
            player_starting_location = st.text_input(
                "Player 1's Starting Location", "You are standing on the wooden dock attatched to Laketown"
            )
            player_starting_text = st.text_area(
                "Player 1's Starting Text",
                """You are on the docks of Laketown, You hear the sound of waves crashing against the wooden stilts that support the village."""
                """ You smell fish and smoke in the air. You see several boats, huts, and villagers around you."""
                """ You swear you saw a suspicious looking raft going towards the market district earlier.""",
            )

    st.header("Scenario")
    st.write(world_desc)
    st.markdown(
        "<p style = 'text-align: center; color: grey;' > "
        + utils.img_to_html(st.session_state.latest_image, 350)
        + " </p> ",
        unsafe_allow_html=True,
    )
    st.subheader("Player 1 (You)")
    st.write(player_description)
    st.write(f"Objective: {player_objective}")
    st.divider()
    st.write("Now begin your quest!")
    if skip_intro:
        start_button = True
    else:
        if st.session_state.has_password:
            start_button = st.button("🏔️ Begin LangQuest!", help="Click to start the game with the current settings.")
        else:
            start_button = st.button("🏔️ Begin LangQuest!", help="Click to start the game with the current settings.", disabled=True)
            st.warning("You must enter the password in order to start the game. See the top of the page.")
    if start_button:
        st.session_state.world_state = entities.World(world_desc)
        st.session_state.player = entities.Player(
            "Player 1", player_description, player_items, player_objective, player_starting_location
        )
        st.session_state.dungeon_master = entities.DungeonMaster(
            player_starting_text, world_desc, st.session_state.player
        )

        st.session_state.game_state = GameState.WAITING_FOR_PLAYER.value
        st._rerun()


# Main game loop
if st.session_state.game_state != GameState.WAITING_TO_START.value and st.session_state.has_password:
    assert "player" in st.session_state, "Player is None"
    assert "world_state" in st.session_state, "World State is None"
    assert "dungeon_master" in st.session_state, "Dungeon Master is None"
    assert lang.api_key.key != "", "API Key is empty"

    full_col1, full_col2 = st.columns(2)
    with full_col1:
        with st.columns(5)[1]:
            st.image(secondary_title_image, width=400)
        history = ""
        for i in range(len(st.session_state.dungeon_master.player_history)):
            role_text = f"<span class='dungeon-master'>🧙‍Dungeon Master:</span>"
            event_text = st.session_state.dungeon_master.player_history[i].action
            history += f"> {role_text} {event_text}\n\n"
            if i < len(st.session_state.player.turn_history):
                role_text = f"<span class='player-1'>Player 1:</span>"
                event_text = st.session_state.player.turn_history[i].action
                history += f"> {role_text} {event_text}\n\n"
        if st.session_state.dungeon_master_thoughts != "":
            history += f"\n<span class='thought'>‍💭 Dungeon Master Thoughts: {st.session_state.dungeon_master_thoughts}</span>"
        if len(history) > 0:
            history = history[:-1]

        utils.custom_scroller(history, 400)

    with full_col2:
        tab1, tab2, tab3 = st.tabs(["💡 Status", "🧳 Inventory", "📖 Character Description"])
        with tab1:
 
            stats_col1, stats_col2 = st.columns(2)

            stats_col1.image(st.session_state.latest_image, width=345)
            if "image_prompt" in st.session_state:
                with stats_col1.expander("🎨 Event Image Prompt"):
                    st.write(st.session_state.image_prompt)

            stats_col2.markdown(f"#### ❤️ Health")
            my_bar = stats_col2.progress(
                st.session_state.player.health,
                text=f":red[{st.session_state.player.health}/{st.session_state.player.max_health}]",
            )
            stats_col2.markdown(f"#### 🌏 Location:")
            stats_col2.markdown(f" {st.session_state.player.location}")
            stats_col2.markdown(f"#### 🧭 Objective:")
            stats_col2.markdown(f" {st.session_state.player.objective}")
        with tab2:
            cl1expander = st.expander("🧳 Inventory", expanded=False)
            inventory_output_string = ""
            for item in st.session_state.player.items:
                inventory_output_string += f"- {item}\n"
            if inventory_output_string == "":
                inventory_output_string = "(Empty)"
            st.markdown(f"#### 🧳 Your Inventory:\n\n{inventory_output_string}")

        with tab3:
            st.markdown(f"#### Your Character Description")
            st.markdown(f"{st.session_state.player.description}")
            cl2expander4 = st.expander("🌏 Area Background", expanded=False)
            cl2expander4.markdown(f"{st.session_state.world_state.description}")

    st.markdown("What would you like to do next?")

    input_is_disabled = st.session_state.game_state != GameState.WAITING_FOR_PLAYER.value

    with st.form("my_form", clear_on_submit=True):
        custom_action = st.text_input(
            "Custom Action:",
            key="user_input_text",
        )
        submit_button = st.form_submit_button("Submit", disabled=input_is_disabled)
        if submit_button:
            st.session_state.user_input = custom_action

    if (
        skip_intro
        and st.session_state.game_state == GameState.WAITING_FOR_PLAYER.value
        and st.session_state.turn_number == 0
    ):
        st.session_state.user_input = "I walk towards the market."

    if st.session_state.compute_progress > 0:
        if st.session_state.compute_progress >= 100:
            st.session_state.compute_progress = 100
        st.progress(st.session_state.compute_progress)

    if st.session_state.user_input != "" and st.session_state.game_state == GameState.WAITING_FOR_PLAYER.value:
        st.session_state.player.play_action(st.session_state.user_input)
        st.session_state.debug_history.append(f"Player turn: {st.session_state.user_input}")
        st.session_state.game_state = GameState.WAITING_FOR_AI.value
        st._rerun()

    if st.session_state.game_state == GameState.WAITING_FOR_AI.value:
        player = st.session_state.player
        dungeon_master = st.session_state.dungeon_master
        if st.session_state.compute_state == "done" or st.session_state.compute_state == "":
            st.session_state.user_input = ""
            with st.spinner("Waiting for Dungeon Master to compute... (working on understanding users input)"):
                st.session_state.player_action = st.session_state.player.turn_history[-1].action
                st.session_state.player_action = lang.sanitize_action(player, st.session_state.player_action)
                st.session_state.debug_history.append(f"Player turn sanitized: {st.session_state.player_action}")
            st.session_state.compute_state = "Finished sanitizing"
            st.session_state.dungeon_master_thoughts = f"Player's wish: {st.session_state.player_action}"
            st.session_state.compute_progress = 2
            st._rerun()
        if st.session_state.compute_state == "Finished sanitizing":
            with st.spinner("Waiting for Dungeon Master to compute... (thinking...)"):
                st.session_state.player_thoughts = lang.get_dungeon_master_thoughts(
                    st.session_state.player_action, player, dungeon_master
                )
            st.session_state.debug_history.append(f"DM thoughts about player: {st.session_state.player_thoughts}")
            st.session_state.compute_state = "Finished Thoughts"
            st.session_state.dungeon_master_thoughts = f"{st.session_state.player_thoughts}"
            st.session_state.compute_progress += 8
            st._rerun()
        if st.session_state.compute_state == "Finished Thoughts":
            with st.spinner("Waiting for Dungeon Master to compute... (assessing likely outcomes)"):
                st.session_state.player_likely_outcome = lang.get_likely_outcome(
                    player,
                    st.session_state.player_action,
                    st.session_state.player_thoughts,
                    dungeon_master,
                )
            st.session_state.debug_history.append(
                f"DMs likely outcome for player: {st.session_state.player_likely_outcome}"
            )
            st.session_state.compute_state = "Finished Likely Outcomes"
            st.session_state.dungeon_master_thoughts = f"{st.session_state.player_likely_outcome}"
            st.session_state.compute_progress += 13
            st._rerun()
        if st.session_state.compute_state == "Finished Likely Outcomes":
            with st.spinner("Waiting for Dungeon Master to compute... (computing and writing outcome)"):
                st.session_state.player_result = lang.get_dungeon_master_outcome(
                    player,
                    st.session_state.player_action,
                    st.session_state.player_thoughts,
                    st.session_state.player_likely_outcome,
                    dungeon_master,
                )
            st.session_state.debug_history.append(f"DMs outcome for player: {st.session_state.player_result}")
            st.session_state.dungeon_master.player_result(st.session_state.player_result)
            st.session_state.dungeon_master_thoughts = f""
            st.session_state.compute_state = "Finished Computing Outcome"
            st.session_state.compute_progress += 23
            st._rerun()
        if st.session_state.compute_state == "Finished Computing Outcome":
            with st.spinner("Summarising Event..."):
                st.session_state.player_action_summary = lang.summarise_event(
                    st.session_state.player_action, st.session_state.player_result
                )
            st.session_state.dungeon_master.player_summary_result(st.session_state.player_action_summary)
            st.session_state.debug_history.append(
                f"Summary outcome for player: {st.session_state.player_action_summary}"
            )
            st.session_state.dungeon_master_thoughts = f""
            st.session_state.compute_state = "Finished Summary"
            st.session_state.compute_progress += 8
            st._rerun()
        if st.session_state.compute_state == "Finished Summary":
            with st.spinner("Generating Visual Description..."):
                st.session_state.visual_description = lang.write_visual_description(
                    player, dungeon_master, st.session_state.player_action_summary
                )
            st.session_state.dungeon_master_thoughts = f"{st.session_state.visual_description}"
            st.session_state.debug_history.append(f"visual_description: {st.session_state.visual_description}")
            st.session_state.compute_state = "Finished Visual Description"
            st.session_state.compute_progress += 16
            st._rerun()
        if st.session_state.compute_state == "Finished Visual Description":
            with st.spinner("Generating Image Prompt..."):
                st.session_state.image_prompt = lang.write_scenario_prompt(st.session_state.visual_description)
            st.session_state.dungeon_master_thoughts = f"{st.session_state.image_prompt}"
            st.session_state.debug_history.append(f"image prompt: {st.session_state.image_prompt}")
            st.session_state.compute_state = "Finished Image Prompt"
            st.session_state.compute_progress += 10
            st._rerun()
        if st.session_state.compute_state == "Finished Image Prompt":
            with st.spinner("Generating Image..."):
                st.session_state.latest_image = lang.generate_image(st.session_state.image_prompt)
            st.session_state.debug_history.append(f"image_url: {st.session_state.latest_image}")
            st.session_state.dungeon_master_thoughts = f""
            st.session_state.compute_state = "Finished DM Turn"
            st.session_state.compute_progress += 20
            st._rerun()

        if st.session_state.compute_state == "Finished DM Turn":
            st.session_state.compute_state = "done"
            st.session_state.game_state = GameState.WAITING_FOR_PLAYER.value
            # st.session_state.dungeon_master_thoughts = ""
            st.session_state.turn_number += 1
            st.session_state.compute_progress = 0
            st._rerun()

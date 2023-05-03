![Title Image](content/LangQuestTitle.jpeg)

# LangQuest
Using LangChain, GPT-3.5, and Chain of Thought reasoning to create a Dungeons and Dragons type experience.

## Technology 💻
LangQuest is written in **Python** 🐍 and uses **Streamlit** for the front end. Streamlit is an open-source framework that provides a quick interactive web app.

## Features 🌟
Some of the features that make LangQuest unique and fun are:

- **Image generation**: LangQuest uses image generation to enhance the visual aspect of the game. You can see pictures of the places, characters, and items you encounter in your adventure.
- **Hitpoints**: You have a health bar that decreases when you take damage and increases when you heal. If your hitpoints reach zero, you lose the game.
- **Location**: Persistent location, kept track of by the Dungeon Master. You can move around the world and explore different places.
- **Inventory**: You have a backpack that stores the items you find or buy along your journey. You can use them for various purposes, such as healing, attacking, or solving puzzles.
- **Storyline**: You can choose from different scenarios that set the background and the goal of your adventure. Each scenario has multiple endings depending on your choices and actions.
- **Customisable scenario**: You can also create your own scenario by changing the setup. LangQuest will generate a new world for you to explore based on your input.



## Quickstart
1. Get an OpenAI [API Key](https://platform.openai.com/account/api-keys)
2. Clone the repo to somewhere locally.
3. Add a new file in the root called `api.txt`
    - This file should be next to `main.py`
    - Inside the file, paste your API Key, so the contents of the file looks like 
```
sk-aBcDeF***************************************XyZ
```
4. (Optional) Create a virtual environment with `python3 -m venv .venv`
    - Linux/MacOS, enter the env with: `source .venv/bin/activate`
    - Windows Powershell, enter with: `.venv/Scripts/Activate.ps1`
5. install required packages: `pip install -r requirements-dev.txt`
6. Ensure streamlit installed correctly by running the command below. If this fails, see [Here](https://docs.streamlit.io/library/get-started/installation) for more information.
```
streamlit hello
```

## How to play 🕹️
Run the command:
```
streamlit run main.py
```

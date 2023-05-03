![Title Image](content/LangQuestTitle.jpeg)

# LangQuest
Using LangChain, GPT-3.5, Chain of thought reasoning to create a Dungeons and Dragons type experience.
Written in Python, front end uses streamlit.
Complete with hitpoints, inventory, storyline, immersive image generation, and more.

## Quickstart
1. Get an OpenAI [API Key](https://platform.openai.com/account/api-keys)
2. Clone the repo to somewhere locally.
3. Add a new file in the root called `api.txt`
    - This file should be next to `main.py`
    - Inside the file, paste your API Key, so the contents of the file looks like `sk-aBcDeF***************************************XyZ`
4. (Optional) Create a virtual environment with `python3 -m venv .venv`
    - Linux/MacOS, enter the env with: `source .venv/bin/activate`
    - Windows Powershell, enter with: `.venv/Scripts/Activate.ps1`
5. install required packages: `pip install -r requirements-dev.txt`
6. Ensure streamlit installed correctly by running `streamlit hello`. If this fails, see [Here](https://docs.streamlit.io/library/get-started/installation) for more information.

## Running the game
Run the command:
`streamlit run main.py`

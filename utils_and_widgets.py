import base64
from pathlib import Path
from PIL import Image, ImageOps
import PIL
from io import BytesIO
import streamlit.components.v1 as components

def convert_event_to_html(event: str):
    pass

def img_to_bytes(image: PIL.Image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())
    return img_str.decode()
    # img_bytes = Path(img_path).read_bytes()
    # encoded = base64.b64encode(img_bytes).decode()
    # return encoded



def img_to_html(image: PIL.Image, size: int):
    img_html = "<img style='width:{}px' src='data:image/png;base64,{}' class='img-fluid'>".format(
        size,
        img_to_bytes(image)
    )
    return img_html

def custom_scroller(html_content: str, height: int):
    """A custom scroller that allows for scrolling of a text area."""
    script = """
    window.onload=function(){
    const scrollingElement = document.getElementById("scroller");
    scrollingElement.scrollTop = scrollingElement.scrollHeight;}
        """
    style_sheet = """
    #scroller {
    background: #0e1117;
    font-family: 'Times New Roman', serif;
    }
    .player-1 {
    color: #8888ff;
    text-shadow: 0 0 0px #333399;
    }
    .player-2 {
    color: #ff8888;
    text-shadow: 0 0 0px #993333;
    }
    .dungeon-master {
    color: #55ff55;
    text-shadow: 0 0 0px #999933;
    }
    .glow {
    text-shadow: 0 0 0px #555555;
    }
    .thought{
    color: #666666;
    }
    """
    style = f"""
    height: {height - 20}px;
    padding: 5px;
    overflow: scroll;
    color: #dddddd;
    white-space: pre-wrap;
    border: solid 1px #88888855;
    border-radius: 5px;
        """
    components.html(
        f"""
<style>{style_sheet}</style>
<div id="scroller" style="{style}"
<p>{html_content}</p>
</div>
<script>{script}</script>""",
        height=height,
    )
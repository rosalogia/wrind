from urllib.parse import urlparse, unquote
import wikipedia
from pysubparser import parser as psparser
from .set_generator import generate_sets


def wikipedia_parser(parsed_url, splits=1, set_directory="."):
    lang = parsed_url.netloc.split(".")[0]
    title = parsed_url.path.split("/")[-1]

    wikipedia.set_lang(lang)
    page = wikipedia.page(title=title)

    generate_sets(page.content, splits, set_directory)


def subtitles_parser(subtitle_file, splits=1, set_directory="."):
    subs = psparser.parse(subtitle_file)

    try:
        lines = [line.text for line in subs]
    except UnicodeDecodeError:
        subs = psparser.parse(subtitle_file, encoding="ISO-8859-1")
        lines = [line.text for line in subs]

    text = " ".join(lines)
    generate_sets(text, splits, set_directory)


def router(inData, url=True, splits=1, set_directory="."):
    if url:
        parsed_url = urlparse(unquote(inData))
        if "wikipedia" in parsed_url.netloc:
            wikipedia_parser(parsed_url, splits, set_directory)
    elif inData.endswith((".srt", ".ass", ".ssa", ".sub")):
        subtitles_parser(inData, splits, set_directory)
    elif inData.endswith((".txt", ".md")):
        with open(inData) as f:
            text = f.read()
        generate_sets(text, splits, set_directory)
    else:
        generate_sets(inData, splits, set_directory)

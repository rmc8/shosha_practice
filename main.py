import PySimpleGUI as sg
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def get_input_text():
    sg.theme("Black")
    layout = [
        [sg.Text("書写用のテキストを入力してください。")],
        [sg.Multiline("", size=(40, 8))],
        [sg.Submit(button_text="OK")],
    ]
    window = sg.Window("ASIN Input", layout)
    while True:
        event, values = window.read()
        if event is None or event in (sg.WIN_CLOSED, "Exit"):
            window.close()
            exit()
        elif event == "OK":
            window.close()
            return values[0]


def web_driver() -> webdriver:
    """
    Return Chrome's webdriver
    :return: Chrome's webdriver
    """
    options = Options()
    options.add_argument("log-level=3")
    return webdriver.Chrome(ChromeDriverManager().install(), options=options)


def add_style():
    with open("style.css", mode="r", encoding="utf-8") as f:
        return f.read()


def add_type(char):
    return f"""<span class="type">{char}</span>"""


def gen_js(txt):
    style = f"<style>{add_style()}</style>"
    start = """<div id="output" class="output vertical" style="-ms-writing-mode:tb-rl;writing-mode:vertical-rl;float:right;padding-right:40px;">"""
    end = "</div>"
    char_list = list(txt)
    tag_list = [add_type(c) for c in char_list]
    span_html = "".join(tag_list)
    html = f"{style}{start}{span_html}{end}"
    js = f"document.write(`{html}`);"
    return js


def get_url_text(text):
    ts = set(list(text))
    return "".join(list(ts))


def main():
    input_text = get_input_text()
    driver = web_driver()
    try:
        driver.maximize_window()
        url_text = get_url_text(input_text)
        driver.get(f"https://www.kenjisugimoto.com/penji/index.html?penji={url_text}")
        js = gen_js(input_text)
        driver.execute_script(js)
        input("OK")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()

import pytest
from bs4 import BeautifulSoup
import datetime
import re
import os

def load_html(filename):
    """Betölti a HTML fájlt, és hibát kezel."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return BeautifulSoup(f.read(), "html.parser")
    except FileNotFoundError:
        pytest.fail(f"A fájl nem található: {filename}")
    except Exception as e:
        pytest.fail(f"Hiba történt a fájl betöltése során: {e}")

def test_html_file_exists():
    """Ellenőrzi, hogy a index.html fájl létezik-e."""
    try:
        load_html("index.html")
        assert True
    except FileNotFoundError:
        assert False, "A index.html fájl nem létezik."

def test_language_setting():
    """Ellenőrzi a nyelv beállítását."""
    soup = load_html("index.html")
    assert soup.html.get("lang") == "hu", "A nyelv beállítása nem magyar."

def test_browser_tab_title():
    """Ellenőrzi a böngészőfülön megjelenő címet."""
    soup = load_html("index.html")
    assert soup.title.text == "AIX", "A böngészőfülön nem az 'AIX' felirat jelenik meg."

def test_main_heading():
    """Ellenőrzi a főcímet."""
    soup = load_html("index.html")
    h1 = soup.find("h1")
    assert h1 is not None, "Nem található egyes szintű főcím (h1)."
    assert h1.text == "AIX", "A főcím tartalma nem 'AIX'."

def test_paragraph_count():
    """Ellenőrzi a bekezdések számát."""
    soup = load_html("index.html")
    paragraphs = soup.find_all("p")
    assert len(paragraphs) == 4, "Nem pontosan 4 bekezdés található."

def test_subheadings():
    """Ellenőrzi a bekezdések alcímeit."""
    soup = load_html("index.html")
    h2_elements = soup.find_all("h2")
    assert len(h2_elements) == 3, "Nem pontosan 3 darab kettes szintű fejezetcím található."

    expected_h2_texts = ["Egy", "Kettő", "Három"]
    for i, h2 in enumerate(h2_elements):
        assert h2.text == expected_h2_texts[i], f"A {i+1}. alcím szövege nem megfelelő."

def test_bold_text():
    """Ellenőrzi a félkövér szöveget."""
    soup = load_html("index.html")
    bold_text = soup.find("b")
    assert bold_text is not None, "Nem található félkövér szöveg."
    assert bold_text.text == "Advanced Interactive eXecutive", "A félkövér szöveg tartalma nem 'Advanced Interactive eXecutive'."

def test_emphasized_text():
    """Ellenőrzi a kiemelt szöveget."""
    soup = load_html("index.html")
    em_elements = soup.find_all("em")
    assert em_elements, "Nem található kiemelt szöveg."
    
    # Ellenőrizzük, hogy az összes AIX ki van-e emelve
    aix_count = 0
    for p in soup.find_all("p"):
        aix_count += p.text.count("AIX")
    
    assert len(em_elements) == aix_count, "Nem az összes AIX szó van kiemelve"
    for em in em_elements:
        assert em.text == "AIX", "A kiemelt szöveg tartalma nem 'AIX'."


def test_html_comment():
    """Ellenőrzi a HTML kommentet (bármilyen névvel)."""
    soup = load_html("index.html")
    today = datetime.date.today().strftime("%Y.%m.%d")
    
    # Reguláris kifejezés a komment kereséséhez, ami legalább egy karaktert és a dátumot is tartalmazza
    comment_pattern = re.compile(rf".+\s*{today}")

    comment = soup.find(string=lambda text: isinstance(text, str) and comment_pattern.match(text))
    
    assert comment is not None, f"Nem található komment, ami nevet és a mai dátumot ({today}) tartalmaz."
    
if __name__ == "__main__":
    pytest.main()
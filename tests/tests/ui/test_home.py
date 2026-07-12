from pathlib import Path

from streamlit.testing.v1 import AppTest

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"


def _logged_in_at():
    at = AppTest.from_file("pages/home.py")
    at.session_state["access_token"] = "hardcoded-admin-token"
    at.session_state["user"] = {"email": "admin@surfacedetect.com", "full_name": "Admin"}
    return at


def test_page_renders():
    at = _logged_in_at()
    at.run()
    assert not at.exception
    assert any("Surface Crack Detection" in m.value for m in at.markdown)


def test_sidebar_has_nav_buttons():
    at = _logged_in_at()
    at.run()
    buttons = at.sidebar.button
    assert len(buttons) >= 5
    labels = [b.label for b in buttons]
    for expected in ["Dashboard", "Predict", "User", "About Us", "Logout"]:
        assert any(expected in lbl for lbl in labels), f"'{expected}' not found in button labels"


def test_predict_radio_exists():
    at = _logged_in_at()
    at.session_state["nav"] = "Predict"
    at.run()
    radio = at.radio
    assert len(radio) > 0
    assert "Category you expect" in radio[0].label


def test_predict_radio_default():
    at = _logged_in_at()
    at.session_state["nav"] = "Predict"
    at.run()
    assert at.radio[0].value == "Potholes"


def test_predict_radio_change_class():
    at = _logged_in_at()
    at.session_state["nav"] = "Predict"
    at.run()
    at.radio[0].set_value("Cracks").run()
    assert at.radio[0].value == "Cracks"


def test_severity_info_before_prediction():
    at = _logged_in_at()
    at.run()
    assert any("No predictions yet" in i.value for i in at.info)


def test_prediction_without_upload():
    at = _logged_in_at()
    at.run()
    at.button[0].click().run()
    assert not any("error" in str(e.value).lower() for e in at.error)

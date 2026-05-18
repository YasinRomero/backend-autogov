from app.modules.auth.service import clean_text


def test_clean_text_greeting_with_spaces_and_special_characters():
    text_to_clean = "   ¡Hola, Señor Mûller!   "
    expected_result = "hola senor muller!"
    assert clean_text(text_to_clean) == expected_result


def test_clean_text_uppercase_and_accents():
    text_to_clean = "Café, Té y Chocolate"
    expected_result = "cafe te y chocolate"
    assert clean_text(text_to_clean) == expected_result


def test_clean_text_languages_and_numerical_versions():
    text_to_clean = "Python 3.12, JavaScript"
    expected_result = "python 3.12 javascript"
    assert clean_text(text_to_clean) == expected_result


def test_clean_text_french_phrase_and_trailing_period():
    text_to_clean = "Crème brûlée, por favor."
    expected_result = "creme brulee por favor."
    assert clean_text(text_to_clean) == expected_result


def test_clean_text_identifier_with_hyphens_and_symbols():
    text_to_clean = "usuario_123-test!"
    expected_result = "usuario_123-test!"
    assert clean_text(text_to_clean) == expected_result

from app.config.settings import APP_INFO


def test_app_info_contains_repository() -> None:
    assert APP_INFO["repository"] == "https://github.com/yahya06/pdf-safetools"

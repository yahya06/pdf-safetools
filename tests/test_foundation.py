from app.config.settings import APP_INFO


def test_app_info_hides_unconfigured_repository() -> None:
    assert APP_INFO["repository"] is None

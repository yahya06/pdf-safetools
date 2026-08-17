from pathlib import Path

from app.config.settings import cleanup_temp_dir, temporary_directory


def test_temporary_directory_context_manager(tmp_path: Path) -> None:
    with temporary_directory() as temp_dir:
        assert temp_dir.exists()
        assert temp_dir.is_dir()
    assert not temp_dir.exists()


def test_cleanup_temp_dir_removes_contents(tmp_path: Path) -> None:
    test_dir = tmp_path / "cleanup_test"
    test_dir.mkdir()
    (test_dir / "file.txt").write_text("test")
    (test_dir / "subdir").mkdir()
    (test_dir / "subdir" / "nested.txt").write_text("nested")
    assert (test_dir / "file.txt").exists()
    assert (test_dir / "subdir" / "nested.txt").exists()
    cleanup_temp_dir()

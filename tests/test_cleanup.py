from pathlib import Path


def test_legacy_flask_app_removed():
    assert not Path('project_directory').exists()


def test_legacy_scratch_scripts_removed():
    assert not Path('input.py').exists()
    assert not Path('output.py').exists()

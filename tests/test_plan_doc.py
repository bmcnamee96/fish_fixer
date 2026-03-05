from pathlib import Path


def test_plan_file_exists():
    assert Path('plan.md').exists()


def test_plan_contains_required_sections():
    content = Path('plan.md').read_text(encoding='utf-8')
    required = [
        'Goals',
        'Recommended Target Stack',
        'Product Flows to Implement',
        'Testing Strategy',
        'Migration Execution Plan',
    ]
    for section in required:
        assert section in content

import os
from pathlib import Path
from unittest.mock import patch

import pytest


def test_get_compose_files_fixture_environment_variable(
    pytester: pytest.Pytester,
) -> None:

    pytester.makepyfile(
        """
        import pytest
        import os
        from unittest.mock import patch
        from pathlib import Path

        def test_example(request: pytest.FixtureRequest, tmp_path: Path) -> None:
            test_compose_files = [
                tmp_path / "a" / "docker-compose.yml",
                tmp_path / "b" / "docker-compose.yml",
            ]
            for path in test_compose_files:
                path.parent.mkdir(parents=True)
                path.touch()

            with patch.dict(
                os.environ,
                {
                    "PDC2_COMPOSE_FILES": f"{tmp_path}/a/docker-compose.yml,{tmp_path}/b/docker-compose.yml"
                }):
                compose_files: list[Path] = request.getfixturevalue("compose_files")
                assert compose_files == test_compose_files
    """
    )
    result = pytester.runpytest()
    result.assert_outcomes(passed=1)


def test_get_compose_files_fixture_pytest_args(
    pytester: pytest.Pytester,
    tmp_path: Path,
) -> None:
    example_compose_file = tmp_path / "docker-compose.yml"
    example_compose_file.touch()

    pytester.makepyfile(
        f"""
        import pytest
        from pathlib import Path

        def test_example(compose_files: list[Path]) -> None:
            example_compose_file = Path("{example_compose_file}")
            assert compose_files == [example_compose_file]
    """
    )
    result = pytester.runpytest(f"--docker-compose={example_compose_file}")
    result.assert_outcomes(passed=1)


@pytest.mark.parametrize("scope", ["session", "package", "module", "class", "function"])
def test_compose_files_fixture_scope(scope: str, pytester: pytest.Pytester) -> None:
    pytester.makepyfile(
        f"""
        import pytest

        def test_example(request: pytest.FixtureRequest) -> None:
            func_fixture = request._fixturemanager.getfixturedefs("compose_files", request.node.nodeid)[0]
            assert func_fixture.scope == "{scope}"
    """
    )

    result = pytester.runpytest(f"--docker-project-scope={scope}")
    result.assert_outcomes(passed=1)

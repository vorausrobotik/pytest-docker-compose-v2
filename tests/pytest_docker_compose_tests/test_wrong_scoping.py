import pytest


@pytest.mark.should_fail
def test_read_all_module(module_scoped_container_getter):
    assert module_scoped_container_getter.get("my_api_service").network_info[0]


@pytest.mark.should_fail
def test_read_all_function(function_scoped_container_getter):
    assert function_scoped_container_getter.get("my_api_service").network_info[0]


def test_invalid_docker_project_scope(pytester: pytest.Pytester) -> None:
    result = pytester.runpytest_inprocess("--docker-project-scope=invalid")
    assert result.ret != 0
    result.stderr.fnmatch_lines(
        ["*error: argument --docker-project-scope: invalid choice: 'invalid'*"]
    )


@pytest.fixture(scope="function")
def test_foo(request: pytest.FixtureRequest) -> None:
    docker_project = request.getfixturevalue("docker_project")

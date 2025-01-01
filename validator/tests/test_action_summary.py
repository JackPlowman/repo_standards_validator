from ..action_summary import generate_action_summary


def test_generate_action_summary() -> None:
    # Arrange
    analysed_repositories = {
        "owner": "test",
        "repositories": [
            {
                "name": "test",
                "checks": [
                    {
                        "name": "test",
                        "result": "test",
                        "output": "test",
                    }
                ],
            }
        ],
    }
    # Act
    generate_action_summary(analysed_repositories)

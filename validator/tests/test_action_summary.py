from typing import TYPE_CHECKING

from validator.action_summary import generate_action_summary

if TYPE_CHECKING:
    from validator.custom_types import AnalysedRepositories


def test_generate_action_summary() -> None:
    # Arrange
    analysed_repositories: AnalysedRepositories = {
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

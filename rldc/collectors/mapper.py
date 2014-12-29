github_repo_stats = {
    "github_repo_stats": {
        "properties": {
            "repo_name": {
                "type": "string",
                "index": "not_analyzed"
            },
            "name": {
                "type": "string",
                "index": "not_analyzed"
            },
            "stargazers_count": {"type": "long"},
            "subscribers_count": {"type": "long"},
            "open_issues_count": {"type": "long"},
            "forks_count": {"type": "long"}
        }
    }
}

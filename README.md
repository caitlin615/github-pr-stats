pr-stats
---

Outputs statistics of Github team members contributions to PR reviews.

# Setup
Create a `.env` with the following information. You will need a
[Github Access Token](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line)

```bash
GITHUB_ACCESS_TOKEN=GithubAccessToken
GITHUB_ORG=GithubOrg
GITHUB_REPOS=comma,separated,list,of,repos
GITHUB_TEAM=teamToGatherStats
```

# Build and Run
To build the docker image
```
make build
```

To run the docker image
```
make run
```

To access the docker image's shell
```
make shell
```

# Rules

* 1 point for providing a PR review (ie approval/dismissed approval)
* 1 point for each PR comment
* 1 point for each regular comment
* 0 points on your own PRs

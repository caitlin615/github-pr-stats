#!/usr/bin/env python3

from github import Github
import os
from datetime import datetime, timedelta

# TODO: Query by date instead of by number of PRs
NUM_PRS = os.getenv("NUM_PRS", 10)

def main():
  repo_names = os.getenv("GITHUB_REPOS").split(",")
  g = Github(os.getenv("GITHUB_ACCESS_TOKEN"))
  team = g.get_organization(os.getenv("GITHUB_ORG")).get_team_by_slug(os.getenv("GITHUB_TEAM"))
  team_members = dict((m.login, {"total": 0, "comment": 0, "pr-comment": 0, "review": 0}) for m in team.get_members())

  for repo in (g.get_repo("{}/{}".format(os.getenv("GITHUB_ORG"), r)) for r in repo_names):
    print("--- ", repo.name)
    for pr in repo.get_pulls(state="all")[:NUM_PRS]:
      author = pr.user.login
      print("#{} | merged: {} | state: {} | author: {} | title: {}".format(pr.number, pr.is_merged(), pr.state, pr.user.login, pr.title))

      for comment in pr.get_comments():
        # Don't count if the comments are by the author or if the commenter isn't on the team
        if comment.user.login == author or comment.user.login not in team_members: continue
        team_members[comment.user.login]["pr-comment"] += 1
        print("    * pr-comment: {}: {}".format(comment.user.login, comment.body.splitlines()[0]))

      for issue_comment in pr.get_issue_comments():
        # Don't count if the comments are by the author or if the commenter isn't on the team
        if issue_comment.user.login == author or issue_comment.user.login not in team_members: continue
        team_members[comment.user.login]["comment"] += 1
        print("    * issue-comment: {}: {}".format(comment.user.login, comment.body.splitlines()[0]))

      # This is just for logging
      for review in [review for review in pr.get_reviews() if review.state != "COMMENTED"]:
        if review.user.login not in team_members: continue
        print("    * pr-review: {}: {}".format(review.user.login, review.state, review.body))

      # Using `set` handles the uniqueness. You can approve a PR multiple times, but you should only get one point
      for approver in set([review.user.login for review in pr.get_reviews() if review.state != "COMMENTED"]):
        # Don't count if the reviewer isn't on the team
        if approver not in team_members: continue
        team_members[approver]["review"] += 1
    print()

  # Calculate the totals
  for i in team_members:
    team_members[i]["total"] = team_members[i]["comment"] + team_members[i]["pr-comment"] + team_members[i]["review"]

  print()
  for x in sorted(team_members.items(), key=lambda x: x[1]["total"], reverse=True):
    print("{}: {}".format(x[0], x[1]))

if __name__== "__main__":
  main()

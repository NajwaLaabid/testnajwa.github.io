---
title: 'Useful GitHub commands'
date: 2022-02-04T15:41:03+02:00
redirect_from:
  - /gp
  - /blog/github
tags:
  - GitHub
---

# Branches
`git branch -d`
- set a local git branch to track a new remote branch: 
    `git fetch`
    `git checkout -b <local-branch-name> <remote-name><remote-branch-name>`
- add a file created in one branch to a different branch (locally):
    `git add <file-name>` # add the file 
    `git stash` # stash the changes
    `git checkout <target-branch>` # checkout the target branch
    `git stash pop` # add the latest stash to the new branch
- create a new branch, then add/commit new changes there:
  - could just checkout/switch to a new branch then add files there
    `git switch -c <new-branch>`
    or
    `git checkout -b <new-branch>`

# Concepts
## Stashing
- What it is
- When to use it

## Git Tricks

### Basing Error

Sometimes I encouter this error message when trying to pull from remote: "fatal: Not possible to fast-forward, aborting.". This is because the branch is no longer directly based off of the branch you're trying to merge it into - e.g. another commit was added to the destination branch that isn't in your branch. Thus, you can't fast-forward into it (because fast-forward requires your branch to completely contain the destination branch).
But sometimes even more weirdly, there's only one main branch in the reporsitory.

What you can do is:
- You can rebase your branch on top of the destination branch (`git rebase <destination branch>`) to rework the commits such that they will fast forward into it. This works when you don't have local changes or commits. Also you can do `git pull --rebase`.
- If you do have local changes, you can merge both the current changes and the changes that'd come from the pull of the branch from origin: `git merge origin/BRANCH_NAME`. After that, resolve the merge conflicts if any and push you local commits.

### Personal Access Token

Starting Aug 13rd, GitHub only uses personal access token for code push approval, which is hard to remember.
For convenience, you can store the credentials and save your time typing the username and the long personal access token.

```
# first, run
git config --global credential.helper store

# then, pull the repository
git pull
# provide the username and personal access token once
```

If you only want to do this for a single repository, run `git config credential.helper store` within the repository and use `git pull/push` once to store the username and personal access token.

If the personal access token is updated, you can delete the saved credentials by deleting `.git-credentials` and then run `git pull/push` again to provide the new personal access token.

**Attention**: This method saves the credentials in plaintext on your PC's disk. Everyone on your computer can access it, e.g. malicious NPM modules.

### Identity

- Set your username (globally): `git config --global user.name "FIRST_NAME LAST_NAME"`
- Set your email address (globally): `git config --global user.email "MY_NAME@example.com"`
- For repository-specific setting, remove the flag `--global`

### Undo `git add`

```
git restore --staged <file>
```

### Squash Commits and Merge into One

```
git reset --soft HEAD~3 && git commit
git push -f
```

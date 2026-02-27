## Git Tricks

### Commit Changes in Branch A to Branch B

```
git stash
git checkout other-branch
git stash pop
```

The first `stash` hides away your changes (basically making a temporary commit), and the subsequent `stash pop` re-applies them. This lets Git use its merge capabilities.

### Upstream and Downstream

After forking a repo, you might want to have a branch to keep tracking of the upstream repo.

Check our current configured remote repo for our fork.

```
$ git remote -v
origin <fork-repo-url> (fetch)
origin <fork-repo-url> (push)
```

That means we haven't configured a remote that points to the `upstream` repo.

To add a new `upstream` repo that will be used to sync with the `origin` repo:

```
$ git remote add upstream <original-repo-url>
```

`original-repo-url` is the HTTPS URL of the repo that we fork.

Now `git remote -v` should give us:

```
origin <fork-repo-url> (fetch)
origin <fork-repo-url> (push)
upstream <original-repo-url> (fetch)
upstream <original-repo-url> (push)
```

Fetch data from the upstream:

```
$ git fetch upstream
```

Now we can create a branch at the local repo that is synced with the latest upstream repo:

```
$ git checkout -b newbranch upstream/main
```

You can push to have the branch committed, or commit something and push to the newly created branch.

```
$ git push -u origin newbranch
```

### Basing Error

Sometimes I encounter this error message when trying to pull from the remote: "fatal: Not possible to fast-forward, aborting.". This is because the branch is no longer directly based off of the branch you're trying to merge it into - e.g. another commit was added to the destination branch that isn't in your branch. Thus, you can't fast-forward into it (because fast-forward requires your branch to completely contain the destination branch).
But sometimes even more weirdly, there's only one main branch in the repository.

What you can do is:
- You can rebase your branch on top of the destination branch (`git rebase <destination branch>`) to rework the commits such that they will fast forward into it. This works when you don't have local changes or commits. Also you can do `git pull --rebase`.
- If you do have local changes, you can merge both the current changes and the changes that'd come from the pull of the branch from origin: `git merge origin/BRANCH_NAME`. After that, resolve the merge conflicts if any and push you local commits.

If you just want your branch to be up to date with main, but don’t care about linear history:
```
git checkout your-branch
git fetch origin
git merge origin/main
# resolve any conflicts
git push --force-with-lease
``` 

### Personal Access Token

Starting Aug 13th, GitHub only uses personal access tokens for code push approval, which is hard to remember.
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
- Set the account credential: `git config credential.username "new name"`

### Undo `git add`

```
git restore --staged <file>
```

### Revert a Particular File to a Particular Commit

Especially after you've changed a lot to the file but found that it is stupid...

```
git checkout <SHA-HASH> -- file/file-path
```

### Squash Commits and Merge into One

```
git reset --soft HEAD~3 && git commit
git push -f
```

### Git Unset Credentials

```
git config --unset credential.helper
```

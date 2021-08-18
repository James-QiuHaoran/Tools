## Git Tricks

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

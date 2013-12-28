Dot Files
=========

Git repo of personal dot/setting files

Affects
-------
Bash, vim, git, terminal (tested under Ubuntu)

Installation
------------
For most files create a soft link from the intended location to the repo. For instance .bashrc in ~/ will become a soft link to the .bashrc in the repo.

For .gitconfig this line will allow you to mix personal settings (email, name) with the repo's .gitconfig


```
[include] 
  path = /path/to/github/dotfiles/.gitconfig
```

To Do
-----
- Convert vim solarized and pathogen, dir colors and .git-* to git repos (using submodules?)
- setup script

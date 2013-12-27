Linux Settings
==============

Git repo of personal linux settings

Affects
-------
Bash, vim, git

Installation
------------
For most files create a soft link from the intended location to the repo for instance .bashrc in ~/ will become soft link to the .basrc in the repo.

For .gitconfig this line will allow you to mix personal settings (email, name) with the repo .gitconfig

[include] 
  path = /path/to/github/linux-settings/.gitconfig

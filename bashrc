alias ls="ls -F --color=auto"
alias ll="ls -altr"
alias aptgetupdate="sudo apt-get update && sudo apt-get upgrade"
alias pipupdate="pip list --outdated | cut -d ' ' -f1 | xargs -n1 sudo -H pip install -U"
export GREP_OPTIONS='--color=auto'

export TERM=xterm-256color

# virtualenvwrapper
export WORKON_HOME=$HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper_lazy.sh

eval `dircolors ~/.dir_colors`

source ~/.git-completion.bash
source ~/.git-prompt.sh

EDITOR=vim
GIT_EDITOR=vim

PS1='\[\e[31m\][\u@\h] \w\[\e[33m\]$(__git_ps1)\[\e[31m\] \$ \[\e[39m\]'

function settitle() { echo -ne "\e]2;$@\a\e]1;$@\a"; }

function sett() { tempstr=$(pwd); settitle `basename "$tempstr"`:`hostname`;}

#function cd() { command cd "$@"; sett;}
#function ssh() { command ssh "$@"; sett;}

#sett

#settitle "TESTSTRING"
if [ -t 1 ]
then
  bind '"\e[A": history-search-backward'
  bind '"\e[B": history-search-forward'
fi

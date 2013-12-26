alias ls="ls -F --color=auto"
export GREP_OPTIONS='--color=auto' 

export TERM=xterm-256color

eval `dircolors ~/.dir_colors`

source ~/.git-completion.bash
source ~/.git-prompt.sh

EDITOR=vim
GIT_EDITOR=vim

PS1='\e[31m[\u@\h] \w\e[33m$(__git_ps1)\e[31m \$ \e[39m'

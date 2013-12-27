
execute pathogen#infect()
syntax on
filetype plugin indent on

syntax enable
set background=dark
colorscheme solarized

set mouse=a
set number
set smartindent
set wildmenu
set wildmode=list:longest
set tabstop=2
set softtabstop=2
set shiftwidth=2
set expandtab
set hlsearch

xnoremap p pgvy

:nmap <F9> :tabprevious<CR>
:nmap <F10> :tabnext<CR>
:nmap <C-t> :tabnew<CR>
:map <F7> :set paste<CR>
:map <F8> :set nopaste<CR>


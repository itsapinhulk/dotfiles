call plug#begin('~/.vim/plugged')
Plug 'tpope/vim-sensible'
Plug 'vim-airline/vim-airline'
Plug 'tpope/vim-fugitive'
Plug 'altercation/vim-colors-solarized'
Plug 'tmhedberg/SimpylFold'
Plug 'vim-scripts/indentpython.vim'
call plug#end()

set background=dark
colorscheme solarized

set mouse=a
set number
set splitbelow
set wildmenu
set wildmode=list:longest
set tabstop=2
set softtabstop=2
set shiftwidth=2
set expandtab
set autoindent
set guifont=Liberation\ Mono\ for\ Powerline\ 10

set encoding=utf-8
set hlsearch
set laststatus=2
set backspace=2
set backspace=indent,eol,start
nnoremap <space> za
vnoremap <space> zf

let g:airline_powerline_fonts = 1
let g:SimpylFold_docstring_preview = 1

xnoremap p pgvy

:nmap <F9> :tabprevious<CR>
:nmap <F10> :tabnext<CR>
:nmap <C-t> :tabnew<CR>
:map <F7> :set paste<CR>
:map <F8> :set nopaste<CR>

:nnoremap <silent> <F5> :let _s=@/<Bar>:%s/\s\+$//e<Bar>:let @/=_s<Bar>:nohl<CR>

augroup python
  autocmd!
  autocmd Filetype python setlocal tabstop=2 shiftwidth=2 softtabstop=2
augroup end

let autoload_plug_path = stdpath('config') . '/autoload/plug.vim'
if !filereadable(autoload_plug_path)
    silent exe '!mkdir $(dirname ' . autoload_plug_path . ')'
    silent exe '!wget -L -O ' . autoload_plug_path .
        \ ' https://raw.github.com/junegunn/vim-plug/master/plug.vim'
    execute 'source ' . fnameescape(autoload_plug_path)
endif
unlet autoload_plug_path

call plug#begin(stdpath('data') . '/plugged')
Plug 'mhartington/oceanic-next'
Plug 'vim-airline/vim-airline'
Plug 'tmhedberg/SimpylFold'
Plug 'Shougo/deoplete.nvim', { 'do': ':UpdateRemotePlugins' }
Plug 'zchee/deoplete-jedi'
Plug 'vhdirk/vim-cmake'
Plug 'SirVer/ultisnips'
call plug#end()

set encoding=utf-8

set nocompatible            " disable compatibility to old-time vi
set showmatch               " show matching brackets.
set ignorecase              " case insensitive matching
set mouse=a                 " Enable all mouse support
set hlsearch                " highlight search results

set tabstop=2               " number of columns occupied by a tab character
set softtabstop=2           " see multiple spaces as tabstops so <BS> does the right thing
set shiftwidth=2            " width for autoindents
set expandtab               " converts tabs to white space


set clipboard=unnamedplus   " Allow interop with system clipboard
"set clipboard+=ideaput      " Allow interop with IntelliJ's clipboard

set autoindent              " indent a new line the same amount as the line just typed
set number                  " add line numbers
set wildmode=longest,list   " get bash-like tab completions

set termguicolors           " true colors
set noeol                   " highlight missing newline at end of file
set splitbelow
set splitright
set laststatus=2
set backspace=indent,eol,start  " Fix backspace behavior

set cc=81                   " set a 80 column border for good coding style

filetype plugin indent on   " allows auto-indenting depending on file type
syntax on                   " syntax highlighting

set background=dark         " Select theme
let g:oceanic_next_terminal_bold = 1
let g:oceanic_next_terminal_italic = 1
colorscheme OceanicNext
let g:airline_theme='oceanicnext'

" Enable powerline for vim-airline
let g:airline_powerline_fonts = 1

" Enable completion at startup
let g:deoplete#enable_at_startup = 1

let g:SimpylFold_docstring_preview = 1     " Show docstring in folds
set foldlevel=0                            " Start with some folds open

" Tab navigation and creation (Ctrl-T)
:nmap <F9> :tabprevious<CR>
:nmap <F10> :tabnext<CR>
:nmap <C-t> :tabnew<CR>

" Switch between paste mode to disable indentation in pasted content
:map <F7> :set paste<CR>
:map <F8> :set nopaste<CR>

" Switch between panes with simpler shortcuts
nnoremap <C-J> <C-W><C-J>
nnoremap <C-K> <C-W><C-K>
nnoremap <C-L> <C-W><C-L>
nnoremap <C-H> <C-W><C-H>

" Remove trailing whitespace with <F5>
:nnoremap <silent> <F5> :let _s=@/<Bar>:%s/\s\+$//e<Bar>:let @/=_s<Bar>:nohl<CR>

" Better undo behavior
set undofile                " Save undos after file closes
set undolevels=1000         " How many undos are stored
set undoreload=10000        " number of lines to save for undo

" Make space shortcut for folding
nnoremap <space> za
vnoremap <space> zf

" Better paste behavior
xnoremap p pgvy

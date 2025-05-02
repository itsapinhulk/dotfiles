vim.o.encoding='utf-8'

vim.o.compatible=false  -- Disable compatibility with old-time vi
vim.o.showmatch=true    -- Show matching brackets
vim.o.ignorecase=true   -- Case insensitive matching
vim.o.mouse='a'         -- Enable all mouse support
vim.o.hlsearch=true     -- Highlight searchBresults

-- 2 spaces for a tab
vim.o.tabstop=2
vim.o.softtabstop=2
vim.o.shiftwidth=2
vim.o.expandtab=true  -- Convert tabs to spaces

-- Allow interop with System clipboard
vim.opt.clipboard:append{'unnamedplus'}

-- Indent a new line with same amount as current line
vim.o.autoindent=true

vim.o.number=true   -- Show line numbers

-- Hightlight current line and number
vim.o.cursorline=true
vim.o.cursorlineopt='both'

-- Bash-like tab completions
vim.opt.wildmode={'longest', 'list'}

vim.o.termguicolors=true  -- True colors
vim.o.eol=false           -- Highlight missing newline at end of file
vim.o.splitbelow=true	  -- Open split window below
vim.o.splitright=true   -- Open split window to right
vim.o.laststatus=2    	-- ??

-- Fix backspace behavior
vim.opt.backspace = {'indent', 'eol', 'start'}

vim.o.colorcolumn='101'     -- Suggestion for maximum line width

vim.o.foldlevel=1   -- Start with some folds open

-- Save undo after file closes and long history (num and lines)
vim.o.undofile=true
vim.o.undolevels=1000
vim.o.undoreload=10000

-- Autosave on losing focus, ignore any errors
vim.api.nvim_create_autocmd({"BufLeave", "FocusLost"}, {
  pattern = {"*"},
  command = "silent! wall",
})

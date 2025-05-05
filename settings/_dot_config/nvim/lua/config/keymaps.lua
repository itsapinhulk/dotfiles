-- Keymaps are automatically loaded on the VeryLazy event
-- Default keymaps that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/keymaps.lua

-- Retain clipboard after pasting (in visual mode)
vim.keymap.set('x', 'p', 'pgvy')

-- Remove trailing whitespace on pressing <F5>
vim.keymap.set('n', '<F5>',
  ':let _s=@/<Bar>:%s/\\s\\+$//e<Bar>:let @/=_s<Bar>:nohl<CR>',
  {silent=true})

-- Switch between panes with simpler shortcuts
vim.keymap.set('n', '<C-J>', '<C-W><C-J>')
vim.keymap.set('n', '<C-K>', '<C-W><C-K>')
vim.keymap.set('n', '<C-L>', '<C-W><C-L>')
vim.keymap.set('n', '<C-H>', '<C-W><C-H>')

vim.keymap.set('n', '<F9>', ':tabprevious<CR>', {remap=true})
vim.keymap.set('n', '<F10>', ':tabnext<CR>', {remap=true})
vim.keymap.set('n', '<C-t>', ':tabnew<CR>', {remap=true})

-- Switch between paste modes to disable indentation in
-- pasted content.
vim.keymap.set('', '<F7>', ':set paste<CR>', {remap=true})
vim.keymap.set('', '<F8>', ':set nopaste<CR>', {remap=true})

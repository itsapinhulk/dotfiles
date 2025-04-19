return {
  "vim-airline/vim-airline",
  lazy = false,
  priority = 999,  -- Load after theme
  dependencies = {
    "vim-airline/vim-airline-themes",
    "ryanoasis/vim-devicons",
  },
  init = function()
    vim.g.airline_powerline_fonts = true
  end,
}

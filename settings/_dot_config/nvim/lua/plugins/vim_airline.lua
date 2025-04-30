return {
  "vim-airline/vim-airline",
  lazy = false,
  priority = 999,  -- Load after theme
  dependencies = {
    "vim-airline/vim-airline-themes",
    "nvim-tree/nvim-web-devicons",
  },
  init = function()
    vim.g.airline_powerline_fonts = true
  end,
}

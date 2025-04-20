return {
  "julienvincent/hunk.nvim",
  cmd = { "DiffEditor" },
  dependencies = {
    "MunifTanjim/nui.nvim",
    "ryanoasis/vim-devicons",
  },
  config = function()
    require("hunk").setup()
  end,
}

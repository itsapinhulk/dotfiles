return {
  "julienvincent/hunk.nvim",
  cmd = { "DiffEditor" },
  dependencies = {
    "MunifTanjim/nui.nvim",
    "nvim-tree/nvim-web-devicons",
  },
  config = function()
    require("hunk").setup()
  end,
}

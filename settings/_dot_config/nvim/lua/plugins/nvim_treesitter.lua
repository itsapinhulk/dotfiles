return {
    "nvim-treesitter/nvim-treesitter",
    build = ":TSUpdate",
    config = function ()
      local configs = require("nvim-treesitter.configs")

      configs.setup({
          ensure_installed = {
            "c", "cpp", "lua", "vim", "vimdoc", "query", "elixir", "heex", "javascript", "html" ,
            "markdown", "markdown_inline", "rust", "java", "go", "python", "javascript", "swift",
            "typescript", "html", "css", "matlab", "bash", "cmake", "csv", "cuda", "sql", "tsx",
            "yaml", "kotlin", "json", "latex",
          },
          auto_install = false,
          sync_install = false,
          highlight = { enable = true },
          indent = { enable = true },
        })
    end
 }

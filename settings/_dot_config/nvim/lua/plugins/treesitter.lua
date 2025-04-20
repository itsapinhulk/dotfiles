return {
    "nvim-treesitter/nvim-treesitter",
    build = ":TSUpdate",
    config = function ()
      local configs = require("nvim-treesitter.configs")

      configs.setup({
          ensure_installed = {
            "c", "cpp", "lua", "vim", "vimdoc", "query", "elixir", "heex", "javascript", "html" ,
            "markdown", "markdown_inline", "rust", "java", "go", "python", "javascript", "tsx",
            "typescript", "html", "css", "matlab", "bash", "cmake", "csv", "cuda", "sql",
            "yaml", "kotlin", "json", "diff", "asm", "haskell", "ini", "toml", "wgsl", "glsl",
          },
          auto_install = false,
          sync_install = false,
          highlight = { enable = true },
          indent = { enable = true },
        })
    end
 }

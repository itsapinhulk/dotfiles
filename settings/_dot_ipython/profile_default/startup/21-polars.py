import shutil

try:
    import polars as pl
except ImportError:
    pass
else:
    # A width cap makes polars shrink every column to fit, so wide frames come
    # out unreadable; render at natural width instead and let the terminal wrap.
    pl.Config(
        tbl_cols=-1,
        tbl_rows=50,
        tbl_width_chars=65_535,
        fmt_str_lengths=100,
        fmt_table_cell_list_len=10,
    )

    def pl_fit(*, width=None):
        """Squeeze tables into `width` (default: terminal width) columns."""
        return pl.Config(
            tbl_width_chars=width or shutil.get_terminal_size((250, 50)).columns
        )

    def pl_natural():
        """Undo pl_fit(): render tables at their natural width."""
        return pl.Config(tbl_width_chars=65_535)

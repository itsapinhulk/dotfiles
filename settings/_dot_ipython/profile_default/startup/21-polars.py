try:
    import polars as pl
except ImportError:
    pass
else:
    pl.Config(tbl_cols=-1, tbl_rows=50, tbl_width_chars=250)

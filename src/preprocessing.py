def clean_ais(df):
    df = df.dropna(subset=["lat", "lon", "speed", "heading"])
    df = df[(df["lat"] != 0) & (df["lon"] != 0)]
    return df

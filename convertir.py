import pandas as pd

df = pd.read_csv("data/datos_categoria_ESCUELAS.csv")

df.to_json(
    "data/escuelas_mexico.json",
    orient="records",
    force_ascii=False,
    indent=4
)

import os, json
import polars as pl
from pathlib import Path

def transform_array_into_list(df:pl.DataFrame,column_name):
    df = df.with_columns(
    pl.when(pl.col((f"{column_name}")).is_null())
      .then(pl.lit([]).cast(pl.List(pl.Utf8)))
      .otherwise(pl.col((f"{column_name}")).cast(pl.List(pl.Utf8)))
      .alias((f"{column_name}"))
    )
    return df
def get_from_string_to_datetime(df:pl.DataFrame,column_name:str):
    df=df.with_columns(pl.col((f"{column_name}")).str.strptime(pl.Datetime, "%Y-%m-%dT%H:%M").dt.convert_time_zone("UTC")
                       .alias((f"{column_name}")))
    return df

def get_from_string_to_date(df:pl.DataFrame,column_name:str):
    df=df.with_columns(pl.col((f"{column_name}")).str.strptime(pl.Datetime, "%Y-%m-%dT%H:%M:%S%.f%:z").dt.date()
                       .alias((f"{column_name}")))
    return df


ROOT_PATH = os.getcwd()
file_path = os.path.join(ROOT_PATH, "all_news.ndjson")
records = []
pathlist=Path(ROOT_PATH).glob("**/*.ndjson")
filelist=sorted([str(file) for file in pathlist])
records=[]
for file in filelist:
    with open(file,"r",encoding="utf-8") as f:
        for ln, line in enumerate(f, start=1):
            s = line.strip()
            if not s:
                continue
            try:
                records.append(json.loads(s))
            except json.JSONDecodeError as e:
                print(f"[NDJSON] Línea {ln} inválida: {e}. Fragmento: {s[:120]!r}")


df=pl.DataFrame(records)
df=df.filter(pl.col("text")!='')
df=df.unique('id')
file_path = os.path.join(ROOT_PATH, "all_news_added_final_final.ndjson")
records = []
with open(file_path, "r", encoding="utf-8") as f:
    for ln, line in enumerate(f, start=1):
        s = line.strip()
        if not s:
            continue
        try:
            records.append(json.loads(s))
        except json.JSONDecodeError as e:
            print(f"[NDJSON] Línea {ln} inválida: {e}. Fragmento: {s[:120]!r}")
df2=pl.DataFrame(records)
df2=df2.select(['headline','dateModified','url','practices','industries','lawyer_names','lawyer_links','text','id','publicationDate'])
df=pl.concat([df,df2])
df=df.unique('id')
df=transform_array_into_list(df,"lawyer_links")
df=transform_array_into_list(df,"industries")
df=transform_array_into_list(df,"practices")
df=transform_array_into_list(df,"lawyer_names")
df=get_from_string_to_datetime(df,"dateModified")
df=get_from_string_to_date(df,"publicationDate")
pl.Config.set_tbl_cols(10)
print(df)

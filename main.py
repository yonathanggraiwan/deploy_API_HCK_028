# Import package
# Fastapi -> package untuk membuat API

from fastapi import FastAPI, HTTPException, Header
import pandas as pd
# FastAPI -> class untuk membuat API
app = FastAPI()

# api function -> get, put, post, delete

# bikin key untuk mengakses data rahasia
api_key = "admin28gacor"

# membuat endpoint
# @object.function_api_type("url")
@app.get("/")
def home():
    return {"message": "Welcome to HCK028!"}

# menjalankan API
# uvicorn nama_file_tanpa_py:nama_object --reload <-reload terus
# uvicorn main:app --reload
# ctrl + c untuk stop

# membuat endpoint untuk membaca data
@app.get("/data")
def readData():
    # baca file
    df = pd.read_csv("dataToko.csv")
    # keluarkan output
    return df.to_dict(orient='records')

@app.get("/data/{user_input}")
def searchData(user_input: int):
    # baca file
    df = pd.read_csv("dataToko.csv")

    # bikin filter  # id pertama adalah nama kolom, id yang kedua yang diinput sama user
    filter = df[df["id"] == user_input]

    # buat condition kalau barang gaada
    if len(filter) == 0:
        raise HTTPException(status_code=404, detail="Barangnya nggak ada coy! :( ")

    # return output kalau barang ada
    return filter.to_dict(orient="records")

# bikin endpoint untuk update data
@app.post("/item/{item_name}")
def updateData(item_id:int, item_name:str, item_price:int):
    # baca file yang sudah ada
    df = pd.read_csv("dataToko.csv")

    # data tambahan
    update_data = {"id":item_id,"namaBarang":item_name,"harga":item_price}

    # convert dictionary to data frame
    update_data_df = pd.DataFrame(update_data, index= [0]) # Setiap pembuatan data frame butuh indeks, mulainya dari 0

    # menggabungkan data lama dengan data baru (concat), concat konsepnya adalah update data
    df = pd.concat([df, update_data_df], ignore_index=True)

    # simpan data terupdate di csv (di overwrite atau ditimpa data lamanya)
    df.to_csv("dataToko.csv", index = False)
    
    # keluarkan output
    return {"message": f"Item dengan nama {item_name} telah berhasil ditambahkan :3"}

@app.put("/update/{item_id}")
def updateData(item_id: int, item_name: str, item_price: int):
    # baca file yang sudah ada
    df = pd.read_csv("dataToko.csv")

    # data tambahan
    update_data = {"id": item_id, "namaBarang": item_name, "harga": item_price}

    # create condition to check the existing data
    if update_data["id"] not in df["id"].values:
        print("id barang tidak ada")
    else:
        # update data
        df.loc[df["id"] == update_data["id"], "namaBarang"] = update_data["namaBarang"]
        df.loc[df["id"] == update_data["id"], "harga"] = update_data["harga"]

    # simpan data ter-update (overwrite data lama)
    df.to_csv("dataToko.csv", index=False)

    # output
    return {"message": f"Item dengan nama {item_name} telah berhasil diupdate :D"}


# bikin endpoint baru untuk read data rahasia
@app.get("/datarahasia")
def readSecret(password: str = Header(None)): # header di swagger dihilangkan
    # baca data rahasia
    df_income = pd.read_csv("dataIncome.csv")

    # Kondisi untu matching password diinputan dengan api_key
    if password != api_key or None:
        raise HTTPException(status_code=401, detail = "Akses ditolak!")
    
    # output
    return df_income.to_dict(orient = "records")

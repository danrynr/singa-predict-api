import tempfile
import os

from time import sleep
from dotenv import load_dotenv
# from typing import Union
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

from predict.predict import LoadModel
from service.gcloud_storage import get_model

load_dotenv()
app = FastAPI()


def load_model():
    load_model = LoadModel(get_model())
    return load_model


@app.get("/")
async def read_root():
    return JSONResponse(
        content={
            "error": False, 
            "message": "ML Prediction API is running!"}, 
        status_code=200)


@app.post("/predict")
def predict(video: UploadFile = File(
    media_type=["video/mp4", "video/x-m4v", "video/*"]
)):
    try:
        # with tempfile.NamedTemporaryFile() as tmp_file:
        #     tmp_file.write(video.file.read())
        #     print(f"This is the temp file path: {tmp_file.name}")
        #     lm = load_model()
        #     result = lm.predict_v(tmp_file.name)
        #     tmp_file.close()

        with open("file.mp4", "wb") as f:
            f.write(video.file.read())

            lm = load_model()
            result = lm.predict_v("file.mp4")


            f.close()

        return JSONResponse(
            content={
                "error": False, 
                "message": "Prediction successful!", 
                "data": result}, 
            status_code=200)
    except Exception as e:
        return JSONResponse(
            content={
                "error": True, 
                "message": "Prediction failed!", 
                "data": str(e)}, 
            status_code=500)


@app.post("/init")
def init_model():
    try:
        get_model()
        return JSONResponse(
            content={
                "error": False, 
                "message": "Model initialized!"}, 
            status_code=200)
    except Exception as e:
        return JSONResponse(
            content={
                "error": True, 
                "message": "Model initialization failed!", 
                "data": str(e)}, 
            status_code=500)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host=str(os.getenv('HOST')), 
        port=int(os.getenv('PORT')),
        reload=True
        )
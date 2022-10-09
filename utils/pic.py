import base64
from fastapi import UploadFile, HTTPException


async def pic_to_base64(pic: UploadFile):
    if pic:
        if pic.content_type != "image/jpeg":
            raise HTTPException(400, detail="File is not an image")
        result = base64.b64encode(await pic.read()).decode('utf-8')
        return result

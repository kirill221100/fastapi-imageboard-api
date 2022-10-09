from typing import Optional
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from db.db_setup import get_db
from db.utils.thread import get_threads, get_thread, make_new_thread, message_to_thread, reply_to_msg

router = APIRouter()


@router.get('/get_threads')
async def main_get(sort: str = 'bump', page: int = 0, db: AsyncSession = Depends(get_db)):
    return await get_threads(db, sort, page)


@router.get('/get_thread')
async def get_one_thread(id: int, db: AsyncSession = Depends(get_db)):
    return await get_thread(db, id)


@router.post('/new_thread')
async def new_thread(text: str, pic: Optional[UploadFile] = File(None), db: AsyncSession = Depends(get_db)):
    return await make_new_thread(db, text, pic)


@router.post('/new_message_to_thread')
async def new_message_to_thread(id: int, text: str, pic: Optional[UploadFile] = File(None),
                                db: AsyncSession = Depends(get_db)):
    return await message_to_thread(db, id, pic, text)


@router.post('/reply_to_message')
async def reply_to_message(thread_id: int, msg_id: int, text: str, pic: Optional[UploadFile] = File(None),
                           db: AsyncSession = Depends(get_db)):
    return await reply_to_msg(db, thread_id, msg_id, pic, text)

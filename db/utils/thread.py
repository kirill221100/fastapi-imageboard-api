from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager
from sqlalchemy import select, func, desc
from fastapi import HTTPException, status, UploadFile
from db.models.thread import Thread, Message
from core.config import Config as cfg
from utils.pic import pic_to_base64


async def get_threads(db: AsyncSession, sort: str = 'bump', page: int = 0):
    if sort == 'bump':
        threads = await db.execute(select(Thread).outerjoin(Thread.messages).group_by(Thread)
                                   .order_by(desc(func.count(Thread.messages))).offset(page * cfg.THREADS_PER_PAGE)
                                   .limit(cfg.THREADS_PER_PAGE))
        return threads.scalars().all()
    threads = await db.execute(select(Thread).order_by(desc(Thread.date)).offset(page * cfg.THREADS_PER_PAGE)
                               .limit(cfg.THREADS_PER_PAGE))
    return threads.scalars().all()


async def get_thread(db: AsyncSession, id: int):
    thr = await db.execute(select(Thread).outerjoin(Thread.messages).filter(Thread.id == id)
                           .options(contains_eager(Thread.messages)).order_by(Message.id))
    thread = thr.scalars().first()
    if thread:
        return thread
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Thread is not found")


async def make_new_thread(db: AsyncSession, text: str, pic: UploadFile):
    pic = await pic_to_base64(pic)
    thread = Thread(text=text, pic=pic)
    db.add(thread)
    await db.commit()
    return thread


async def message_to_thread(db: AsyncSession, id: int, pic: UploadFile, text: str = None):
    thr = await db.execute(select(Thread).filter(Thread.id == id))
    thread = thr.scalars().first()
    if thread:
        pic = await pic_to_base64(pic)
        message = Message(text=text, pic=pic, thread=thread, replies=[])
        db.add(message)
        await db.commit()
        return message
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Thread is not found")


async def reply_to_msg(db: AsyncSession, thread_id: int, message_id: int, pic: UploadFile, text: str = None):
    thr = await db.execute(select(Thread).filter(Thread.id == thread_id))
    msg = await db.execute(select(Message).filter(Message.thread_id == thread_id, Message.id == message_id))
    thread = thr.scalars().first()
    message = msg.scalars().first()
    if thread and message:
        pic = await pic_to_base64(pic)
        reply = Message(text=text, pic=pic, thread=thread, replies=[])
        db.add(reply)
        await db.flush()
        await db.refresh(reply)
        message.replies.append(reply.id)
        reply.reply_id = message.id
        await db.commit()
        return reply
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Thread or message is not found")

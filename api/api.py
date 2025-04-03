import uvicorn
from fastapi import FastAPI, Depends
from bd.bd import get_db, tableGolosov, tablePocemons
from faker import Faker
from sqlalchemy import text
app=FastAPI()

def generate_pocemon():
    n=10
    fake=Faker()
    session=get_db()
    session.query(tablePocemons).delete()
    session.execute(text("ALTER SEQUENCE pocemon_id_seq RESTART WITH 1"))
    for _ in range(n):
        pocemon = fake.user_name()
        stroke=tablePocemons(pocemon=pocemon)
        session.add(stroke)
    session.commit()
    result = session.query(tablePocemons.id, tablePocemons.pocemon).all()
    pocemon_dict = {id_: pocemon for id_, pocemon in result}

    return pocemon_dict

@app.post("/api/createPoll")
def create_golos(db=Depends(get_db)):
    pocemon_dict = generate_pocemon(db)

    # Создание нового голосования
    new_poll = tableGolosov(amount=0)
    db.add(new_poll)
    db.commit()

    return {"poll_id": new_poll.id, "choices": pocemon_dict}



@app.post("/api/poll")
def poll_golos(poll_id: int, choice_id: int, db = Depends(get_db)):
    # Проверяем, существует ли голосование с данным poll_id
    poll = db.query(tableGolosov).filter_by(id=poll_id).first()
    if not poll:
        raise Exception("Poll not found")

    # Проверяем, существует ли выбор с данным choice_id
    pocemon = db.query(tablePocemons).filter_by(id=choice_id).first()
    if not pocemon:
        raise Exception("Choice not found")

    # Добавляем голос
    poll.amount += 1
    db.commit()

    return {"message": f"You voted for {pocemon.pocemon} in poll {poll_id}!"}


if __name__=="__main__":
    uvicorn.run(app=app, host="127.0.0.1", port=8000)
#
# @app.post("/api/getResult")


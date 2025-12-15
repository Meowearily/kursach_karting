import uvicorn
from contextlib import asynccontextmanager
from datetime import date, time

from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, SQLModel, create_engine

from model import (
    # Таблицы БД
    Karts, Tracks, Races, Racers, Workers, 
    Race_Racer_Kart, Workers_Race,
    # Базовые классы для API
    KartBase, TrackBase, RaceBase, RacerBase, 
    WorkerBase, RaceResultBase
)
import request as req


# ========== DATABASE CONFIGURATION ==========

# Создаем SQLite базу данных (можно заменить на PostgreSQL/MySQL)
#DATABASE_URL = "sqlite:///./kart_club.db"
#engine = create_engine(f"postgresql://postgres:1234@localhost:5432/karting")

# Создаем engine - пул соединений к БД
engine = create_engine(
     f"postgresql://postgres:1234@localhost:5432/karting",
     #DATABASE_URL,
     echo=True,  # Логирование SQL запросов (отключите в production)
#     connect_args={"check_same_thread": False}  # Только для SQLite
 )


def create_db_and_tables():
    """Создать все таблицы в БД"""
    SQLModel.metadata.create_all(engine)


def seed_database():
    """Заполнить БД начальными данными"""
    with Session(engine) as session:
        # Проверяем, есть ли уже данные
        existing_tracks = req.read_all_tracks(session)
        if existing_tracks:
            return  # БД уже заполнена
        
        # Создаем трассы
        track1 = Tracks(
            name="Monaco Circuit",
            state=True,
            open=True,
            length=1.5
        )
        track2 = Tracks(
            name="Speed Track",
            state=True,
            open=False,
            length=2.3
        )
        session.add(track1)
        session.add(track2)
        session.commit()
        session.refresh(track1)
        session.refresh(track2)
        
        # Создаем карты
        kart1 = Karts(
            model="SuperKart X1",
            state=True,
            tires="Soft",
            tires_change_date=date(2025, 1, 1),
            rain=False
        )
        kart2 = Karts(
            model="RacingKart Pro",
            state=True,
            tires="Hard",
            tires_change_date=date(2025, 1, 5),
            rain=True
        )
        session.add(kart1)
        session.add(kart2)
        session.commit()
        session.refresh(kart1)
        session.refresh(kart2)
        
        # Создаем гонщиков
        racer1 = Racers(
            name="Ivan Petrov",
            club_card=True,
            date_of_birth=date(1995, 5, 15),
            date_of_registration=date(2023, 1, 10),
            best_time=time(1, 25, 30)
        )
        racer2 = Racers(
            name="Anna Smirnova",
            club_card=True,
            date_of_birth=date(1998, 8, 20),
            date_of_registration=date(2023, 3, 15),
            best_time=time(1, 23, 45)
        )
        session.add(racer1)
        session.add(racer2)
        session.commit()
        session.refresh(racer1)
        session.refresh(racer2)
        
        # Создаем гонку (демонстрация foreign key)
        race1 = Races(
            track_id=track1.id,
            race_date=date(2025, 12, 15)
        )
        session.add(race1)
        session.commit()
        session.refresh(race1)
        
        # Создаем результаты гонки (демонстрация множественных foreign keys)
        result1 = Race_Racer_Kart(
            race_id=race1.id,
            racer_id=racer1.id,
            kart_id=kart1.id,
            duration=time(1, 28, 15)
        )
        result2 = Race_Racer_Kart(
            race_id=race1.id,
            racer_id=racer2.id,
            kart_id=kart2.id,
            duration=time(1, 26, 30)
        )
        session.add(result1)
        session.add(result2)
        session.commit()
        
        print("==> База данных успешно заполнена начальными данными!")


# ========== LIFESPAN CONTEXT MANAGER ==========

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager для FastAPI
    Выполняется при запуске и остановке приложения
    """
    # Startup: создание таблиц и заполнение БД
    print("==> Запуск приложения...")
    create_db_and_tables()
    seed_database()
    print("==> База данных готова!")
    
    yield  # Приложение работает
    
    # Shutdown: очистка ресурсов (если нужно)
    print("==> Остановка приложения...")


# ========== DEPENDENCY INJECTION ==========

def get_session():
    """
    Dependency для получения сессии БД
    Используется в endpoints через Depends()
    """
    with Session(engine) as session:
        yield session


# ========== FASTAPI APPLICATION ==========

app = FastAPI(
    title="Kart Club API",
    description="API для управления картинг-клубом с демонстрацией работы foreign keys",
    version="1.0.0",
    lifespan=lifespan
)


# ========== API ENDPOINTS ==========

# ===== ROOT =====
@app.get("/", tags=["Root"])
def read_root():
    """Корневой endpoint"""
    return {
        "message": "Добро пожаловать в Kart Club API!",
        "docs": "/docs",
        "redoc": "/redoc"
    }


# ===== KARTS ENDPOINTS =====
@app.get("/karts", response_model=list[Karts], tags=["Karts"])
def get_all_karts(session: Session = Depends(get_session)):
    """Получить все карты"""
    return req.read_all_karts(session)


@app.get("/karts/{kart_id}", response_model=Karts, tags=["Karts"])
def get_kart(kart_id: int, session: Session = Depends(get_session)):
    """Получить карт по ID"""
    kart = req.read_kart_by_id(session, kart_id)
    if not kart:
        raise HTTPException(status_code=404, detail="Карт не найден")
    return kart

@app.put("/karts/{kart_id}", response_model=Karts, tags=["Karts"])
def update_kart(kart_id: int, kart_data: KartBase, session: Session = Depends(get_session)):
    """Обновить карт по ID"""
    kart = req.update_kart(session, kart_id, kart_data.state, kart_data.model,
                           kart_data.tires, kart_data.tires_change_date, kart_data.rain)
    if not kart:
        raise HTTPException(status_code=404, detail="Карт не найден")
    return kart


@app.post("/karts", response_model=Karts, tags=["Karts"])
def create_new_kart(kart_data: KartBase, session: Session = Depends(get_session)):
    """Создать новый карт"""
    kart = Karts(**kart_data.model_dump())  # Используем model_dump() для конверсии
    return req.create_kart(kart, session)


@app.delete("/karts/{kart_id}", tags=["Karts"])
def delete_kart_by_id(kart_id: int, session: Session = Depends(get_session)):
    """Удалить карт"""
    if req.delete_kart(kart_id, session):
        return {"message": f"Карт {kart_id} успешно удален"}
    raise HTTPException(status_code=404, detail="Карт не найден")


# ===== TRACKS ENDPOINTS =====
@app.get("/tracks", response_model=list[Tracks], tags=["Tracks"])
def get_all_tracks(session: Session = Depends(get_session)):
    """Получить все трассы"""
    return req.read_all_tracks(session)


@app.get("/tracks/{track_id}", response_model=Tracks, tags=["Tracks"])
def get_track(track_id: int, session: Session = Depends(get_session)):
    """Получить трассу по ID"""
    track = req.read_track_by_id(session, track_id)
    if not track:
        raise HTTPException(status_code=404, detail="Трасса не найдена")
    return track


@app.post("/tracks", response_model=Tracks, tags=["Tracks"])
def create_new_track(track_data: TrackBase, session: Session = Depends(get_session)):
    """Создать новую трассу"""
    track = Tracks(**track_data.model_dump())
    return req.create_track(track, session)


# ===== RACES ENDPOINTS (демонстрация foreign key) =====
@app.get("/races", response_model=list[Races], tags=["Races"])
def get_all_races(session: Session = Depends(get_session)):
    """Получить все гонки"""
    return req.read_all_races(session)


@app.get("/races/{race_id}", response_model=Races, tags=["Races"])
def get_race(race_id: int, session: Session = Depends(get_session)):
    """Получить гонку по ID (с информацией о трассе через foreign key)"""
    race = req.read_race_by_id(session, race_id)
    if not race:
        raise HTTPException(status_code=404, detail="Гонка не найдена")
    return race


@app.post("/races", response_model=Races, tags=["Races"])
def create_new_race(race_data: RaceBase, session: Session = Depends(get_session)):
    """
    Создать новую гонку
    ПРИМЕР РАБОТЫ С FOREIGN KEY: track_id должен существовать в таблице tracks
    """
    # Проверяем существование трассы
    track = req.read_track_by_id(session, race_data.track_id)
    if not track:
        raise HTTPException(
            status_code=400, 
            detail=f"Трасса с ID {race_data.track_id} не существует"
        )
    
    # Создаем объект Races из базового класса
    race = Races(**race_data.model_dump())
    return req.create_race(race, session)


@app.get("/tracks/{track_id}/races", response_model=list[Races], tags=["Races"])
def get_races_by_track_id(track_id: int, session: Session = Depends(get_session)):
    """
    Получить все гонки на определенной трассе
    ПРИМЕР РАБОТЫ С FOREIGN KEY: фильтрация по track_id
    """
    return req.get_races_by_track(session, track_id)


# ===== RACERS ENDPOINTS =====
@app.get("/racers", response_model=list[Racers], tags=["Racers"])
def get_all_racers(session: Session = Depends(get_session)):
    """Получить всех гонщиков"""
    return req.read_all_racers(session)


@app.post("/racers", response_model=Racers, tags=["Racers"])
def create_new_racer(racer_data: RacerBase, session: Session = Depends(get_session)):
    """Создать нового гонщика"""
    racer = Racers(**racer_data.model_dump())
    return req.create_racer(racer, session)


# ===== RACE RESULTS ENDPOINTS (множественные foreign keys) =====
@app.post("/race-results", response_model=Race_Racer_Kart, tags=["Race Results"])
def create_race_result(
    result_data: RaceResultBase, 
    session: Session = Depends(get_session)
):
    """
    Записать результат гонки
    ПРИМЕР РАБОТЫ С МНОЖЕСТВЕННЫМИ FOREIGN KEYS:
    - race_id должен существовать в races
    - racer_id должен существовать в racers
    - kart_id должен существовать в karts
    """
    # Проверяем существование всех связанных объектов
    race = req.read_race_by_id(session, result_data.race_id)
    if not race:
        raise HTTPException(status_code=400, detail="Гонка не найдена")
    
    # Создаем объект из базового класса
    result = Race_Racer_Kart(**result_data.model_dump())
    return req.create_race_racer_kart(result, session)


@app.get("/races/{race_id}/results", response_model=list[Race_Racer_Kart], tags=["Race Results"])
def get_race_results(race_id: int, session: Session = Depends(get_session)):
    """
    Получить все результаты конкретной гонки
    ПРИМЕР РАБОТЫ С RELATIONSHIPS: автоматически загружаются связанные racer и kart
    """
    return req.get_race_results(session, race_id)


@app.get("/racers/{racer_id}/history", response_model=list[Race_Racer_Kart], tags=["Race Results"])
def get_racer_history(racer_id: int, session: Session = Depends(get_session)):
    """
    Получить историю всех гонок гонщика
    ПРИМЕР РАБОТЫ С RELATIONSHIPS: автоматически загружаются связанные race и kart
    """
    return req.get_racer_history(session, racer_id)


# ===== WORKERS ENDPOINTS =====
@app.get("/workers", response_model=list[Workers], tags=["Workers"])
def get_all_workers(session: Session = Depends(get_session)):
    """Получить всех работников"""
    return req.read_all_workers(session)


@app.post("/workers", response_model=Workers, tags=["Workers"])
def create_new_worker(worker_data: WorkerBase, session: Session = Depends(get_session)):
    """Создать нового работника"""
    worker = Workers(**worker_data.model_dump())
    return req.create_worker(worker, session)


# ========== MAIN ==========

if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Автоперезагрузка при изменении кода
    )
from sqlmodel import Session, select
from typing import Sequence
from datetime import date, time

from model import Karts, Races, Tracks, Workers, Racers, Race_Racer_Kart, Workers_Race

# ========== KARTS ==========

def read_all_karts(session: Session) -> Sequence[Karts]:
    """Получить все карты"""
    return session.exec(select(Karts)).all()


def read_kart_by_id(session: Session, kart_id: int) -> Karts | None:
    """Получить карт по ID"""
    return session.get(Karts, kart_id)


def create_kart(kart: Karts, session: Session) -> Karts:
    """Создать новый карт"""
    session.add(kart)
    session.commit()
    session.refresh(kart)  # refresh принимает объект!
    return kart


def update_kart(session: Session, kart_id: int, state: bool, model: str, tires: str, 
                tires_change_date: date, rain: bool) -> Karts | None:
    """Обновить карт"""
    kart = session.get(Karts, kart_id)
    if not kart:
        return None
    
    if state != None:
        kart.state = state

    if model != None:
        kart.model = model
    
    if tires != None:
        kart.tires = tires

    if tires_change_date != None:
        kart.tires_change_date = tires_change_date

    if rain != None:
        kart.rain = rain
    
    session.add(kart)
    session.commit()
    session.refresh(kart)
    return kart


def delete_kart(kart_id: int, session: Session) -> bool:
    """Удалить карт"""
    kart = session.get(Karts, kart_id)
    if not kart:
        return False
    
    session.delete(kart)
    session.commit()
    return True


# ========== TRACKS ==========

def read_all_tracks(session: Session) -> Sequence[Tracks]:
    """Получить все трассы"""
    return session.exec(select(Tracks)).all()


def read_track_by_id(session: Session, track_id: int) -> Tracks | None:
    """Получить трассу по ID"""
    return session.get(Tracks, track_id)


def create_track(track: Tracks, session: Session) -> Tracks:
    """Создать новую трассу"""
    session.add(track)
    session.commit()
    session.refresh(track)
    return track


# ========== RACES ==========

def read_all_races(session: Session) -> Sequence[Races]:
    """Получить все гонки"""
    return session.exec(select(Races)).all()


def read_race_by_id(session: Session, race_id: int) -> Races | None:
    """Получить гонку по ID с relationships"""
    return session.get(Races, race_id)


def create_race(race: Races, session: Session) -> Races:
    """Создать новую гонку"""
    session.add(race)
    session.commit()
    session.refresh(race)
    return race


def get_races_by_track(session: Session, track_id: int) -> Sequence[Races]:
    """Получить все гонки на определенной трассе"""
    statement = select(Races).where(Races.track_id == track_id)
    return session.exec(statement).all()


# ========== RACERS ==========

def read_all_racers(session: Session) -> Sequence[Racers]:
    """Получить всех гонщиков"""
    return session.exec(select(Racers)).all()


def create_racer(racer: Racers, session: Session) -> Racers:
    """Создать нового гонщика"""
    session.add(racer)
    session.commit()
    session.refresh(racer)
    return racer


# ========== RACE_RACER_KART (связующая таблица) ==========

def create_race_racer_kart(race_racer_kart: Race_Racer_Kart, session: Session) -> Race_Racer_Kart:
    """
    Создание связи между гонкой, гонщиком и картом
    """
    session.add(race_racer_kart)
    session.commit()
    session.refresh(race_racer_kart)
    return race_racer_kart


def get_race_results(session: Session, race_id: int) -> Sequence[Race_Racer_Kart]:
    """
    Получение всех результатов гонки с информацией о гонщиках и картах
    """
    statement = select(Race_Racer_Kart).where(Race_Racer_Kart.race_id == race_id)
    return session.exec(statement).all()


def get_racer_history(session: Session, racer_id: int) -> Sequence[Race_Racer_Kart]:
    """
    Получение истории гонок гонщика
    """
    statement = select(Race_Racer_Kart).where(Race_Racer_Kart.racer_id == racer_id)
    return session.exec(statement).all()


# ========== WORKERS ==========

def read_all_workers(session: Session) -> Sequence[Workers]:
    """Получение всех работников"""
    return session.exec(select(Workers)).all()


def create_worker(worker: Workers, session: Session) -> Workers:
    """Создание нового работника"""
    session.add(worker)
    session.commit()
    session.refresh(worker)
    return worker


#----------------

#def read_all_karts(session: Session) -> list[Karts]:
#    return session.exec(select(Karts)).all()

#def create_kart(karts: Karts, session: Session) -> list[Karts]:

    #check commit refresh 
#    session.begin()
#    session.add(karts)
#    session.commit()
#    session.refresh()

#    return karts


#def update_kart(id, state, model, tires, tires_change_date, rain, session: Session) -> list[Karts]:
#    karts = session.get(Karts, id)
#    karts.state = state
#    karts.model = model
#    karts.tires = tires
#    karts.tires_change_date = tires_change_date
#    karts.rain = rain

#    session.begin()
#    session.add(karts)
#    session.commit()
#    session.refresh()

#    return karts

#def delete_kart(karts: Karts, session: Session) -> list[Karts]:
#    session.begin()
#    session.delete(karts)
#    session.commit()
#    session.refresh()

#    return None

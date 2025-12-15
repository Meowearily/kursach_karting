from sqlmodel import Field, Relationship, SQLModel

from datetime import date, time


# ========== БАЗОВЫЕ КЛАССЫ (для API) ==========

class RacerBase(SQLModel):
    """Базовый класс для гонщика (используется в API)"""
    name: str
    club_card: bool
    date_of_birth: date
    date_of_registration: date
    best_time: time


class KartBase(SQLModel):
    """Базовый класс для карта (используется в API)"""
    model: str
    state: bool
    tires: str
    tires_change_date: date
    rain: bool


class TrackBase(SQLModel):
    """Базовый класс для трассы (используется в API)"""
    name: str
    state: bool
    open: bool
    length: float


class WorkerBase(SQLModel):
    """Базовый класс для работника (используется в API)"""
    name: str
    date_of_birth: date
    status: str
    salary: float


class RaceBase(SQLModel):
    """Базовый класс для гонки (используется в API)"""
    track_id: int
    race_date: date | None = None


class RaceResultBase(SQLModel):
    """Базовый класс для результата гонки (используется в API)"""
    race_id: int
    racer_id: int
    kart_id: int
    duration: time


# ========== ТАБЛИЦЫ БД (наследуют базовые классы) ==========

class Racers(RacerBase, table=True):
    """Таблица гонщиков"""
    id: int | None = Field(default=None, primary_key=True)
    
    # Relationships
    race_racer_karts: list["Race_Racer_Kart"] = Relationship(back_populates="racer")


class Karts(KartBase, table=True):
    """Таблица картов"""
    id: int | None = Field(default=None, primary_key=True)
    
    # Relationships
    race_racer_karts: list["Race_Racer_Kart"] = Relationship(back_populates="kart")


class Tracks(TrackBase, table=True):
    """Таблица трасс"""
    id: int | None = Field(default=None, primary_key=True)

    # Relationships
    races: list["Races"] = Relationship(back_populates="track")


class Workers(WorkerBase, table=True):
    """Таблица работников"""
    id: int | None = Field(default=None, primary_key=True)
    
    # Relationships
    workers_races: list["Workers_Race"] = Relationship(back_populates="worker")


class Races(RaceBase, table=True):
    """Таблица гонок"""
    id: int | None = Field(default=None, primary_key=True)
    track_id: int = Field(foreign_key="tracks.id")

    # Relationships
    track: Tracks = Relationship(back_populates="races")
    workers_races: list["Workers_Race"] = Relationship(back_populates="race")
    race_racer_karts: list["Race_Racer_Kart"] = Relationship(back_populates="race")


class Workers_Race(SQLModel, table=True):
    """Связующая таблица: работники ↔ гонки"""
    id: int | None = Field(default=None, primary_key=True)
    worker_id: int = Field(foreign_key="workers.id")
    race_id: int = Field(foreign_key="races.id")

    # Relationships
    worker: Workers = Relationship(back_populates="workers_races")
    race: Races = Relationship(back_populates="workers_races")


class Race_Racer_Kart(RaceResultBase, table=True):
    """Связующая таблица: гонки ↔ гонщики ↔ карты"""
    id: int | None = Field(default=None, primary_key=True)
    race_id: int = Field(foreign_key="races.id")
    racer_id: int = Field(foreign_key="racers.id")
    kart_id: int = Field(foreign_key="karts.id")
    
    # Relationships
    race: Races = Relationship(back_populates="race_racer_karts")
    racer: Racers = Relationship(back_populates="race_racer_karts")
    kart: Karts = Relationship(back_populates="race_racer_karts")



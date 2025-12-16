from sqlmodel import Field, Relationship, SQLModel

from datetime import date, time

class RacerBase(SQLModel):
    name: str
    club_card: bool
    date_of_birth: date
    date_of_registration: date
    best_time: time


class KartBase(SQLModel):
    model: str
    state: bool
    tires: str
    tires_change_date: date
    rain: bool


class TrackBase(SQLModel):
    name: str
    state: bool
    open: bool
    length: float


class WorkerBase(SQLModel):
    name: str
    date_of_birth: date
    status: str
    salary: float


class RaceBase(SQLModel):
    track_id: int
    race_date: date | None = None


class RaceResultBase(SQLModel):
    race_id: int
    racer_id: int
    kart_id: int
    duration: time

class Racers(RacerBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    
    # Relationships
    race_racer_karts: list["Race_Racer_Kart"] = Relationship(back_populates="racer")


class Karts(KartBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    
    # Relationships
    race_racer_karts: list["Race_Racer_Kart"] = Relationship(back_populates="kart")


class Tracks(TrackBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    # Relationships
    races: list["Races"] = Relationship(back_populates="track")


class Workers(WorkerBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    
    # Relationships
    workers_races: list["Workers_Race"] = Relationship(back_populates="worker")


class Races(RaceBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    track_id: int = Field(foreign_key="tracks.id")

    # Relationships
    track: Tracks = Relationship(back_populates="races")
    workers_races: list["Workers_Race"] = Relationship(back_populates="race")
    race_racer_karts: list["Race_Racer_Kart"] = Relationship(back_populates="race")


class Workers_Race(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    worker_id: int = Field(foreign_key="workers.id")
    race_id: int = Field(foreign_key="races.id")

    # Relationships
    worker: Workers = Relationship(back_populates="workers_races")
    race: Races = Relationship(back_populates="workers_races")


class Race_Racer_Kart(RaceResultBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    race_id: int = Field(foreign_key="races.id")
    racer_id: int = Field(foreign_key="racers.id")
    kart_id: int = Field(foreign_key="karts.id")
    
    # Relationships
    race: Races = Relationship(back_populates="race_racer_karts")
    racer: Racers = Relationship(back_populates="race_racer_karts")
    kart: Karts = Relationship(back_populates="race_racer_karts")



from contextlib import asynccontextmanager
import time
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from database import Base, SessionLocal, engine, get_db
import models


class LaptopCreate(BaseModel):
    marca: str
    modelo: str
    ram_gb: int


class LaptopOut(BaseModel):
    id: int
    marca: str
    modelo: str
    ram_gb: int
    disponible: bool

    model_config = ConfigDict(from_attributes=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    intentos = 30
    while intentos > 0:
        try:
            Base.metadata.create_all(bind=engine)
            break
        except OperationalError:
            intentos -= 1
            if intentos == 0:
                raise
            time.sleep(2)

    db = SessionLocal()
    try:
        if db.query(models.Laptop).count() == 0:
            laptops_iniciales = [
                models.Laptop(marca="Dell", modelo="Latitude 5440", ram_gb=16, disponible=True),
                models.Laptop(marca="Lenovo", modelo="ThinkPad E14", ram_gb=8, disponible=False),
                models.Laptop(marca="HP", modelo="ProBook 450", ram_gb=16, disponible=True),
            ]
            db.add_all(laptops_iniciales)
            db.commit()
    finally:
        db.close()

    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def inicio():
    return {"mensaje": "API del laboratorio de cómputo"}


@app.get("/laptops", response_model=list[LaptopOut])
def obtener_laptops(db: Session = Depends(get_db)):
    return db.query(models.Laptop).order_by(models.Laptop.id.asc()).all()


@app.get("/laptops/disponibles", response_model=list[LaptopOut])
def obtener_laptops_disponibles(db: Session = Depends(get_db)):
    return db.query(models.Laptop).filter(models.Laptop.disponible == True).order_by(models.Laptop.id.asc()).all()


@app.get("/laptops/{laptop_id}", response_model=LaptopOut)
def obtener_laptop_por_id(laptop_id: int, db: Session = Depends(get_db)):
    laptop = db.query(models.Laptop).filter(models.Laptop.id == laptop_id).first()
    if not laptop:
        raise HTTPException(status_code=404, detail="Laptop no encontrada")
    return laptop


@app.post("/laptops", response_model=LaptopOut)
def crear_laptop(laptop: LaptopCreate, db: Session = Depends(get_db)):
    nueva_laptop = models.Laptop(
        marca=laptop.marca,
        modelo=laptop.modelo,
        ram_gb=laptop.ram_gb,
        disponible=True,
    )
    db.add(nueva_laptop)
    db.commit()
    db.refresh(nueva_laptop)
    return nueva_laptop

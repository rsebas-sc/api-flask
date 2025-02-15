from sqlmodel import SQLModel, Field
from typing import Optional
import bcrypt  # Importar bcrypt
from flask import json

class Usuario(SQLModel, table=True):
    __tablename__ = "usuarios"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, max_length=50)
    password: str = Field(max_length=60)  # Longitud para almacenar el hash bcrypt
    role: str = Field(default="user", max_length=20)
    email: Optional[str] = Field(default=None, unique=True)

    # Método para hashear la contraseña
    def set_password(self, password: str):
        # Generar un "salt" (valor aleatorio) y hashear la contraseña
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
        self.password = hashed_password.decode("utf-8")  # Guardar como string

    # Método para verificar contraseña
    def check_password(self, password: str) -> bool:
        # Comparar la contraseña ingresada con el hash almacenado
        return bcrypt.checkpw(
            password.encode("utf-8"),
            self.password.encode("utf-8")
        )
    
    def to_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "rol": self.role,
            "email": self.email
        }
    
class Cancha(SQLModel, table=True):
    __tablename__ = "canchas"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100)
    ubicacion: str
    tipo: str = Field(max_length=50)
    precio: float
    disponible: bool = Field(default=True)

from datetime import datetime

class Reserva(SQLModel, table=True):
    __tablename__ = "reservas"

    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuarios.id")
    cancha_id: int = Field(foreign_key="canchas.id")
    fecha_inicio: datetime
    fecha_fin: datetime
    estado: str = Field(default="pendiente", max_length=20)
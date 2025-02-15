from flask import Flask, request, jsonify
from config import engine

from .models import Usuario
from .schemas import UsuarioCreate, UsuarioLogin
from pydantic_core import ValidationError

from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token

def init_app(app: Flask):
    @app.get("/hello")
    def hello():
        return "Hola mundo"
    @app.post("/usuario")
    def crear_usuario():
        try:
            data = UsuarioCreate(**request.json)  # Validar con Pydantic
        except ValidationError as e:
            return jsonify({"mensaje": "Datos inválidos", "errores": e.errors()}), 400
        
        try:
            with Session(engine) as session:
                usuario_nuevo = Usuario(username=data.username, email=data.email)
                usuario_nuevo.set_password(data.password)
                session.add(usuario_nuevo)
                session.commit()
                return jsonify(usuario_nuevo.to_json())
        except IntegrityError:
            session.rollback()
            return jsonify({"mensaje": f"Ya existe el usuario o correo"})
    
    @app.post("/login")
    def login():
        try:
            data = UsuarioLogin(**request.json)  # Validar con Pydantic
        except ValidationError as e:
            return jsonify({"mensaje": "Datos inválidos", "errores": e.errors()}), 400
    
        with Session(engine) as session:
            results = session.exec(select(Usuario).where(Usuario.email == data.email)).first()
            if results is None:
                return jsonify({"mensaje": "Credenciales inválidas"}), 401  # 401 Unauthorized

            if results.check_password(data.password):
                token = create_access_token(identity=results.id, additional_claims={"id": results.id, "username": results.username})
                return jsonify({"mensaje": "Login exitoso", "token": token})
            else:
                return jsonify({"mensaje": "Credenciales inválidas"}), 401  # 401 Unauthorized
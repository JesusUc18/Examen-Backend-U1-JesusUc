from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# URL de conexión a la base de datos MySQL (el host es 'mysql' por el servicio de Docker Compose)
DATABASE_URL = "mysql+pymysql://laboratorio:laboratorio@mysql:3306/laboratorio"

# Configuración del motor de base de datos con verificación previa de conexión activa
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Creador de sesiones para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base declarativa para los modelos ORM
Base = declarative_base()

# Dependencia para inyectar y cerrar la sesión de base de datos en cada petición
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

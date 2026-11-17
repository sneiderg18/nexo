import enum
from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Enum,
    ForeignKey,
    Boolean,
)
from sqlalchemy.orm import relationship

from database import Base


# ---------- ENUMS ----------

class RolUsuario(str, enum.Enum):
    supervisor = "supervisor"
    soporte = "soporte"
    admin = "admin"


class Criticidad(str, enum.Enum):
    baja = "baja"
    media = "media"
    alta = "alta"


class Gravedad(str, enum.Enum):
    baja = "baja"
    media = "media"
    alta = "alta"
    critica = "critica"


class EstadoTicket(str, enum.Enum):
    nuevo = "nuevo"
    en_proceso = "en_proceso"
    resuelto = "resuelto"


# ---------- MODELOS ----------

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(150), unique=True, nullable=False, index=True)
    contrasena_hash = Column(String(255), nullable=False)
    rol = Column(Enum(RolUsuario), nullable=False, default=RolUsuario.supervisor)
    activo = Column(Boolean, default=True)
    creado_en = Column(DateTime, default=datetime.utcnow)

    tickets_reportados = relationship(
        "Ticket", back_populates="reportado_por", foreign_keys="Ticket.reportado_por_id"
    )


class Equipo(Base):
    __tablename__ = "equipos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    tipo = Column(String(50), nullable=False)  # PC, impresora, servidor, etc.
    area = Column(String(100), nullable=True)
    ip = Column(String(45), nullable=True)
    criticidad = Column(Enum(Criticidad), nullable=False, default=Criticidad.media)
    activo = Column(Boolean, default=True)
    creado_en = Column(DateTime, default=datetime.utcnow)

    tickets = relationship("Ticket", back_populates="equipo")


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(Text, nullable=False)

    equipo_id = Column(Integer, ForeignKey("equipos.id"), nullable=False)
    reportado_por_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    gravedad = Column(Enum(Gravedad), nullable=True)  # la asigna el sistema/IA
    justificacion_gravedad = Column(Text, nullable=True)  # explicación de la IA

    estado = Column(Enum(EstadoTicket), nullable=False, default=EstadoTicket.nuevo)

    creado_en = Column(DateTime, default=datetime.utcnow)
    actualizado_en = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resuelto_en = Column(DateTime, nullable=True)

    equipo = relationship("Equipo", back_populates="tickets")
    reportado_por = relationship(
        "Usuario", back_populates="tickets_reportados", foreign_keys=[reportado_por_id]
    )
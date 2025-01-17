from celery import shared_task
from sqlalchemy.orm import Session, sessionmaker
from db.config import engine
from models.event import EventModel, EventTicketModel
from models.location import CityModel
from models.category import CategoryModel
from models.user import UserModel

# Crear una sesión directamente usando el motor
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@shared_task
def process_ticket(event_id: int, user_id: int):
    db: Session = SessionLocal()  # Obtén la sesión de la base de datos
    try:
        # Obtén el evento y cuenta los tickets existentes
        event = db.query(EventModel).filter(EventModel.id == event_id).first()
        ticket_count = db.query(EventTicketModel).filter(EventTicketModel.event_id == event_id).count()

        if ticket_count < event.capacity:
            # Crear el ticket
            ticket = EventTicketModel(event_id=event_id, user_id=user_id)
            db.add(ticket)
            db.commit()
            db.refresh(ticket)
            return "Created ticket"
            # Enviar correo de confirmación
            # send_email(
            #     to_user_id=user_id,
            #     subject="Ticket confirmado",
            #     body=f"Tu ticket para el evento '{event.name}' ha sido confirmado.",
            # )
        
        return "Event sold out"
        # Enviar correo de cupo agotado
        # send_email(
        #     to_user_id=user_id,
        #     subject="Cupo agotado",
        #     body=f"Lo sentimos, no hay más cupos disponibles para el evento '{event.name}'.",
        # )
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

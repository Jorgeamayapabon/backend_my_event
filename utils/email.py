from smtplib import SMTP
from sqlalchemy.orm import Session
from db.config import get_db
from models.user import UserModel

def send_email(to_user_id: int, subject: str, body: str):
    # Implementa la lógica para enviar correos aquí
    # Ejemplo con SMTP (ajusta con tus credenciales y servidor SMTP)
    db: Session = get_db()
    user_email = db.query(UserModel).filter(UserModel.id == to_user_id).first().email
    with SMTP("smtp.example.com", 587) as server:
        server.starttls()
        server.login("your-email@example.com", "your-password")
        server.sendmail(
            from_addr="your-email@example.com",
            to_addrs=[user_email],
            msg=f"Subject: {subject}\n\n{body}",
        )

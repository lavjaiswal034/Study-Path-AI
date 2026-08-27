from getpass import getpass

from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.user import User


def main():
    db = SessionLocal()

    try:
        email = input("Admin email: ").strip()
        name = input("Admin name: ").strip()
        password = getpass("Admin password: ")

        existing_admin = (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

        if existing_admin:
            print("A user with this email already exists.")
            return

        admin = User(
            name=name,
            email=email,
            password_hash=hash_password(password),
            role="admin",
            approval_status="approved",
            is_active=True,
        )

        db.add(admin)
        db.commit()
        db.refresh(admin)

        print(f"Admin created successfully. ID: {admin.id}")

    finally:
        db.close()


if __name__ == "__main__":
    main()
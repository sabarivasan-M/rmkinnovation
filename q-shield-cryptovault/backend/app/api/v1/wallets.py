from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.wallet import Wallet

router = APIRouter()


@router.get("/wallets")
def list_wallets(db: Session = Depends(get_db)):
    return db.query(Wallet).all()

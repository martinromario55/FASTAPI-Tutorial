from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ..schemas import UserCreate, UserOut
from .. import models
from ..database import get_db
from ..utils import hash

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

# Create new User
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Hash password
    hashed_password = hash(user.password)
    user.password = hashed_password
    
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

# Get user by id
@router.get('/{id}', response_model=UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
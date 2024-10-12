from sqlmodel import Session

from app import crud
from app.models import Operation, OperationCreate


def create_random_operation(db: Session) -> Operation:
    expression = "5 3 + 2 *"
    result = 5
    item_in = OperationCreate(expression=expression, result=result)
    return crud.create_operation(session=db, operation_in=item_in)


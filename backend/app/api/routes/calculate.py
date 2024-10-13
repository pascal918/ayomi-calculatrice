
import csv

from typing import Any
from sqlmodel import select
from fastapi import APIRouter
from fastapi.responses import FileResponse

from app.api.deps import CurrentUser, SessionDep
from app.models import Operation

router = APIRouter()

def calculate_npi(expression):
    stack = []
    operators = {'+': lambda a, b: a + b,
                 '-': lambda a, b: a - b,
                 '*': lambda a, b: a * b,
                 '/': lambda a, b: a / b}
    for token in expression.split():
        if token not in operators:
            stack.append(float(token))
        else:
            b = stack.pop()
            a = stack.pop()
            result = operators[token](a, b)
            stack.append(result)
    return stack[0]

@router.post("/calculate", response_model=Operation)
def calculate_expression(expression: str,session: SessionDep):
    result = calculate_npi(expression)
    print('result : test kkkkkkkkkkkkkkkkkkkkkkkkkkk',result)

    new_operation = Operation(expression=expression, result=result)
    session.add(new_operation)
    session.commit()
    session.refresh(new_operation)
    return {"result": result}

@router.get("/export-csv")
async def export_csv(session: SessionDep, response_class=FileResponse) -> Any:
    statement = (
            select(Operation)
            .offset(1)
            .limit(1000)
        )
    operations = session.exec(statement).all()
    with open('operations.csv', 'w', newline='') as csvfile:
        fieldnames = ['id', 'expression', 'result']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for operation in operations:
            writer.writerow({'id': operation.id, 'expression': operation.expression, 'result': operation.result})
    #return {"message": "CSV file generated"}
        export_media_type = 'text/csv'
        export_headers = {
            "Content-Disposition": "attachment; filename={file_name}.csv".format(file_name="operations")
        }
    file_path = "operations.csv"
    response = FileResponse(file_path, media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=downloaded_file.csv"
    return response
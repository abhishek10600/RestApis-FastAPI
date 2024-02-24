from fastapi import APIRouter, HTTPException, status, BackgroundTasks
from ..validations.data_validations import Todo
from ..validations.response_validations import TodoResponse
from typing import Optional


router = APIRouter(tags=["Todos Routes"])

todos = []


async def send_email(todo: Todo):
    print(f"Email notification for Todo {todo.id} is sent")


@router.post("/todos/create", response_model=TodoResponse)
async def create_todo(todo: Todo, background_task: BackgroundTasks):
    todo.id = len(todos) + 1
    todos.append(todo)

    # background task are run on different thread. Use background task when it is a function that is independent of the other functoions.
    background_task.add_task(send_email, todo)
    return todo


@router.get("/todos/all")  # query
async def all_todos(completed: Optional[bool] = None):
    if completed is None:
        return todos
    else:
        return [todo for todo in todos if todo.is_complete == completed]


@router.get("/todos/{todo_id}")  # parameters
async def get_todo_by_id(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Todo not found.")


@router.put("/todos/update/{todo_id}")
async def update_todo(new_todo: Todo, todo_id: int):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            todos[index] = new_todo
            todos[index].id = todo_id
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Todo not found.")


@router.delete("/todos/delete/{todo_id}")
async def delete_todo(todo_id: int):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            del todos[index]
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Todo not found.")

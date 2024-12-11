from aiogram.fsm.state import StatesGroup,State


class UserState(StatesGroup):
    name = State()
    phone = State()

class EmployeesState(StatesGroup):
    employees = State()
    office = State()
    employee_location = State()
    start_work = State()
    report = State()
    status = State()

class DirectorsState(StatesGroup):
    directors = State()
    director_menu = State()
    branches = State()
    location = State()
    new_location = State()
    radius = State()
    branch_delete = State()
    delete = State()
    name = State()
    phone = State()
    new_branch = State()
    price=State()
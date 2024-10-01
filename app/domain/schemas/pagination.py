from pydantic import BaseModel

class Pagination(BaseModel):
    page_number: int
    per_page: int
    number_of_data: int
    number_of_page: int
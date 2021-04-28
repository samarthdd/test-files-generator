from pydantic import BaseModel
from polyglot_generator.Polyglot_Generator import Polyglot_Generator
from fastapi import APIRouter

router_params = { "prefix": "/polyglot-generator"  ,
                  "tags"  : ['Polyglot Generator'] }
router = APIRouter(**router_params)

class Polyglot_File_Details(BaseModel):
    file_type_1       : str
    file_type_2       : str
    num_of_files    : int

@router.post("/generate")
def file_generator(item: Polyglot_File_Details):

    pg = Polyglot_Generator()
    response = pg.populate_polyglot(item.file_type_1,item.file_type_2,item.num_of_files)

    if response == 0:
        return "File Type is not supported or Invalid File Type"

    elif response == -1:
        return "Number of files must be greater than 0"

    return f"{item.num_of_files} files of polyglot type \'{item.file_type_1} with {item.file_type_2}\' are generated"


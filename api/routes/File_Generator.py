from pydantic import BaseModel
from file_generator.File_Generator import File_Generator
from fastapi import APIRouter

router_params = { "prefix": "/file-generator"  ,
                  "tags"  : ['File Generator'] }
router = APIRouter(**router_params)

class File_Details(BaseModel):
    file_type       : str
    num_of_files    : int

@router.post("/generate")
def file_generator(item: File_Details):

    fg = File_Generator(num_of_files=item.num_of_files , file_type= item.file_type)
    response =  fg.populate()

    if response == 0:
        return "File Type is not supported or Invalid File Type"

    elif response == -1:
        return "Number of files must be greater than 0"

    return f"{item.num_of_files} files of type \'{item.file_type}\' are generated"


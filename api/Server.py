import logging

import uvicorn

from fastapi_offline import FastAPIOffline as FastAPI
from osbot_utils.utils.Misc import to_int

from api.routes.File_Generator import router as router_file_generator

class Server:

    def __init__(self, app, port="8881", reload=True):
        self.host       = "0.0.0.0"
        self.log_level  = "info"
        self.port       = to_int(port)
        self.app        = app
        self.reload     = reload

    def fix_logging_bug(self):
        # there were duplicated entries on logs
        #    - https://github.com/encode/uvicorn/issues/614
        #    - https://github.com/encode/uvicorn/issues/562
        logging.getLogger().handlers.clear()

    def setup(self):
        self.app.include_router(router_file_generator   )
        self.fix_logging_bug()
        return self

    def start(self):
        uvicorn.run("api.Server:app", host=self.host, port=self.port, log_level=self.log_level, reload=self.reload)

tags_metadata = [
    {"name": "File Generator", "description": "Supported_types : [ txt, pdf, docx, xlsx, jpg, jpeg, png, gif ]"},
]

# we need to do this here so that when unicorn reload is enabled the "cdr_plugin_folder_to_folder.api.Server:app" has an fully setup instance of the Server object
app     = FastAPI(openapi_tags=tags_metadata)
server  = Server(app)
server.setup()

def run_if_main():
    if __name__ == "__main__":
        server.start()

run_if_main()
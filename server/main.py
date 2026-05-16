from main_server import run

from controllers.sync.sync_controllers import sync_all
from db import init_db
from scheduler import start_scheduler

from lib.helpers import get_file_logger 
from configs.error_logs_files_name import SYNC_ERROR_FILE_NAME

logger = get_file_logger(SYNC_ERROR_FILE_NAME)

if __name__ == "__main__":
    init_db()

    # try:
    #  sync_all()
    # except:
    #  logger.exception("Initial sync failed")

    scheduler = start_scheduler()

    try:
        run("0.0.0.0", 8000)
    finally:
        scheduler.shutdown(wait=False)

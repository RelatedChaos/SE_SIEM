from rq import get_current_job
from app import db
from app.models import Task
import time
from rq import get_current_job
from app import create_app

app = create_app()
app.app_context().push()


def example(seconds):
    print("starting task")
    for i in range(seconds):
        print(i)
        time.sleep(1)
    print("task complete")
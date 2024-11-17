from celery import Celery, Task

from tasks.session import get_session

celery_app = Celery("tasks")
celery_app.config_from_object("tasks.celeryconfig")


class DbTask(Task):
    """An abstract Celery Task that ensures that the connection to the
    database is closed on task completion"""

    abstract = True

    def __init__(self):
        super(DbTask, self).__init__()
        self._session = None
        #email.create_connection()

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        self.session.remove()
        self._session = None

    @property
    def session(self):
        if self._session is None:
            self._session = get_session()
        return self._session

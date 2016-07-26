from app import ApplicationFactory


app = ApplicationFactory.create_application('development')
app.app_context().push()
from app import celery

from flask import current_app as app
from kombu import Queue, Exchange


class QueueConfig(object):
    default_name = 'default'
    system_name = 'system'

    def __call__(self):
        return {
            'CELERY_QUEUES': self.build_queues(),
            'CELERY_DEFAULT_QUEUE': self.default_name,
            'CELERY_ROUTES': (TaskRouter(), )
        }

    @classmethod
    def build_queues(cls):
        default_exchange = Exchange(cls.default_name, type='direct')

        queues = [
            Queue(cls.default_name, default_exchange, routing_key=cls.default_name),
            Queue(cls.system_name, default_exchange, routing_key=cls.system_name)
        ]
        return tuple(set(queues))


class TaskRouter(object):
    system_tasks = ()

    def route_for_task(self, task, args, kwargs):
        task_name = task.split('.')[-1]
        try:
            if task_name in self.system_tasks:
                return {'queue': QueueConfig.system_name, 'routing_key': QueueConfig.system_name}
            else:
                return {'queue': QueueConfig.default_name, 'routing_key': QueueConfig.default_name}
        except (IndexError, AttributeError):
            pass

        app.logger.info('No matching router rule for {}. Using default queue.'.format(task))


from flask_script import Option
from flask_script.commands import InvalidCommand
import atexit
import os
import psutil
import subprocess
import traceback
from signal import SIGTERM
from concurrent.futures import ThreadPoolExecutor
from lib.ext.command.base_command import BaseCommand


class GulpCommand(BaseCommand):
    gulp_command = 'gulp'
    option_list = (
        Option('--production', '-p', action="store_true", dest='prod'),
    )

    def __init__(self, *args, **kwargs):
        self.cleanup_closing = False
        self.gulp_process = None
        self.env = 'development'

        super(GulpCommand, self).__init__(*args, **kwargs)

    @staticmethod
    def gulp_exited_cb(future):
        if future.exception():
            print(traceback.format_exc())

            children = psutil.Process().children(recursive=True)

            for child in children:
                print('>>> Killing pid {}'.format(child.pid))

                child.send_signal(SIGTERM)

            print('>>> Exiting')

            # It would be nice to be able to raise a CommandError or use
            # sys.kill here but neither of those stop the runserver instance
            # since we're in a thread. This method is used in django as well.
            os._exit(1)

    def kill_gulp_process(self):
        if self.gulp_process.returncode is not None:
            return

        self.cleanup_closing = True
        self.stdout.write('>>> Closing gulp process')

        self.gulp_process.terminate()

    def start_gulp(self):
        self.stdout.write('>>> Starting gulp')

        if self.env == 'production':
            gulp_command = '{cmd} --production'.format(cmd=self.gulp_command)
        else:
            gulp_command = self.gulp_command
        self.gulp_process = subprocess.Popen(
            gulp_command,
            cwd=os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'assets')),
            shell=True,
            stdin=subprocess.PIPE,
            stdout=self.stdout,
            stderr=self.stderr)

        if self.gulp_process.poll() is not None:
            raise InvalidCommand('gulp failed to start')

        self.stdout.write('>>> gulp process on pid {0}'
                          .format(self.gulp_process.pid))

        atexit.register(self.kill_gulp_process)

        self.gulp_process.wait()

        if self.gulp_process.returncode != 0 and not self.cleanup_closing:
            raise InvalidCommand('gulp exited unexpectedly')

    def run(self, prod):
        """
        Run Command, Runs a gulp command.
        TODO: Handle KeyboardInterrupt in a nicer way!
        :param prod:
        :return:
        """
        self.env = 'production' if prod else 'development'
        pool = ThreadPoolExecutor(max_workers=1)

        gulp_thread = pool.submit(self.start_gulp)
        gulp_thread.add_done_callback(self.gulp_exited_cb)


class Watch(GulpCommand):
    """Runs gulp watch task"""
    gulp_command = 'gulp watch'


class Build(GulpCommand):
    """Runs gulp default task"""
    gulp_command = 'gulp'


class LintJS(GulpCommand):
    """Runs gulp javascript lint task"""
    gulp_command = 'gulp jshint'

from contextlib import contextmanager
import os
import sys
from threading import Thread, Event
import time

from typing import Iterator

class SpinnerThread(Thread):
    '''SpinnerThread class is a Thread subclass for printing a spinner to an
    output stream.  If the output stream is TTY, a spinner will be displayed, else
    the prefix will be displayed followed up the msg once the spinner is complete

    prefix: The prefixed message to print before the spinner
    msg: The message to print once the spinner is complete
    delay: The amount of time (in seconds) to wait between advancing the
        spinner one position.
    stream: The output stream to write the spinner.  Default: stdout
    '''
    __tokens__ = ['|', '/', '-', '\\']

    def __init__(self, prefix: str, msg: str, delay: float = .25,
            stream: object = sys.stdout) -> None:
        super().__init__()

        self.daemon = True # type: bool
        self.delay = delay
        self.evt_done = Event()
        self.msg = msg
        self.prefix = prefix
        self.stream = stream

    def run(self):
        if self.stream.isatty():
            self.run_thread_tty()
        else:
            self.run_thread()

    def join(self, timeout: float=None):
        try:
            self.evt_done.set()
        finally:
            return super().join(timeout)

    def run_thread(self):
        self.__print_msg(self.prefix)
        self.evt_done.wait()
        self.__print_msg(self.msg + '\n')

    def run_thread_tty(self):
        pos = 0
        tokens = __class__.__tokens__

        # Print the first token
        self.__print_msg(self.prefix + tokens[pos])

        # While the done event has not signaled
        while not self.evt_done.wait(self.delay):
            # Advance position by one
            pos = (pos + 1) % len(tokens)

            # Print just the token by overwritting the previous token
            self.__print_msg(('\b' * len(tokens[pos])) + tokens[pos])

        # Remove the last token and print the finish msg.
        self.__print_msg(('\b' * len(tokens[pos])) + self.msg + os.linesep)

    def __print_msg(self, msg):
        self.stream.write(msg)
        self.stream.flush()

@contextmanager
def spinner(prefix: str, msg: str, delay:float=0.25) -> Iterator[None]:
    spinner_thread = SpinnerThread(prefix=prefix, msg=msg, delay=delay)
    spinner_thread.start()

    try:
        yield
    finally:
        spinner_thread.join()

if __name__ == "__main__":
    with spinner("Waiting for sleep to complete... ", "done"):
        time.sleep(10)
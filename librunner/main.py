from .process import Process


def main(process: Process):
    if process.rank() == 0:
        print('Controller')
    else:
        print('Runner')

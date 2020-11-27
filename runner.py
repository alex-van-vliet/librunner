from librunner.process import Process

process = Process()

if process.rank() == 0:
    print('controller')
else:
    print('runner')

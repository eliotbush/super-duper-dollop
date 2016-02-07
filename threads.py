import threading
import queue
import time

def a():
    #thread worker function
    for i in range(60):
        print('a',end='')
        time.sleep(5)
    return

def console(q):
    while 1:
        cmd = input('> ')
        print(cmd)
        q.put(cmd)
        if cmd == 'quit':
            break

def action_foo():
    print('--> action foo')

def action_bar():
    print('--> action bar')

def invalid_input():
    print('', end='')

def main():
    cmd_actions = {'foo': action_foo, 'bar': action_bar}
    cmd_queue = queue.Queue()

    input_stream = threading.Thread(target=console, args=(cmd_queue,))
    update_timer = threading.Thread(target=a)
    input_stream.start()
    update_timer.start()

    while 1:
        cmd = cmd_queue.get()
        if cmd == 'quit':
            break
        action = cmd_actions.get(cmd, invalid_input)
        action()

main()
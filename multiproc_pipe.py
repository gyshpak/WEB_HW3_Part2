from multiprocessing import Pipe, Process, current_process, cpu_count
from time import sleep, time
import logging

logger = logging.getLogger()
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)

recipient1, sender1 = Pipe()

def factorize_synh(val):
    list_ = []
    sleep(1)
    for i in range(len(val)):
        for n in range(1, val[i]+1):
            if val[i] % n > 0:
                continue
            list_.append(n)
        logger.debug(f'Resault {val[i]} = {list_}')
        list_.clear
    # return list_

def factorize_pipe(pipe: Pipe):
    name = current_process().name
    logger.debug(f'{name} started...')
    val = pipe.recv()
    sleep(1)
    list_ = []
    for i in range(1, val+1):
        if val % i > 0:
            continue
        list_.append(i)
    logger.debug(f'Resault {name}, {val} = {list_}')
    # pipe.send(list_)


if __name__ == '__main__':
    list_digit = []
    while True:
        kay_int = True
        inp_str = input("please enter several numbers ")
        list_str = inp_str.split()
        for i in list_str:
            if i.isdigit() == False:
                logger.debug(f"{i} is not digit")
                kay_int = False
                list_digit.clear
                continue
            list_digit.append(int(i))
        if kay_int == False:
            continue
        break

    len_list_dig = len(list_digit)
    que_cpu = cpu_count()
    qua_iter = min(len_list_dig, que_cpu)
    
    name_proc = {}
    send_val = None

    time1 = time()
    factorize_synh(list_digit)
    time2 = time()
    logger.debug(f"time for synk proc = {time2 - time1}")

    time1 = time()
    for i in range(qua_iter):
        recipient, sender = Pipe()
        name_proc[i] = recipient, sender
    processes = []
    while True:
        qua_iter = min(len_list_dig, que_cpu)
        for i in range(qua_iter):
            process1 = Process(target=factorize_pipe, args=(name_proc[i][0], ))
            process1.start()
            processes.append(process1)
            
        for i in range(qua_iter):
            send_val = list_digit.pop(0)
            name_proc[i][1].send(send_val)
            
        # for i in range(qua_iter):
        #     logger.debug(f"Resault Process-{i+1} = {name_proc[i][1].recv()}")

        len_list_dig -= qua_iter

        if len_list_dig <= 0:
            break
    
    [el.join() for el in processes]

    time2 = time()
    logger.debug(f"time for multiproc = {time2 - time1}")

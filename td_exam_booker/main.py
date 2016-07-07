from .utils import loadConfig
from .attempt import Attempt
from multiprocessing import Process


def main():
    # Load clients from configs
    clients = None
    with open('./clients.json') as f:
        obj = loadConfig(f)
        clients = obj['clients']
        print(str(clients))

    #
    # Prepare the window
    #
    print("<Press Enter to start>")
    input()
    print("Preparing the Windows..")
    window = {}
    for client in clients:
        window[client["code"]] = Attempt(client)

    #
    # Process
    #
    p = {}
    print("<Press Enter to *GO*>")
    input()
    print("Process....")
    for client in clients:
        p[client["code"]] = Process(target=window[client["code"]].go)
        p[client["code"]].start()

    print("< Input 'q' to quit the program >")

    while True:
        if input().strip() == 'q':
            for client in clients:
                p[client["code"]].terminate()
                window[client["code"]].killAttempt()
            break

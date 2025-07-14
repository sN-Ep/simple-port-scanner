import socket
import time
import threading
import queue
from colors import colr 
import argparse
import sys

toscanned = queue.Queue()
SERVICE = "UNKNOWN SERVICE"

# To Use CLI Tool Like Hacker😀️
def from_cli():
     try:
        parser = argparse.ArgumentParser(description="My Cool Port Scanner")
        parser.add_argument('--host', required=True, help="Target host IP")
        parser.add_argument('--ports', default="22,80,443,1234,8080", help="Port range, e.g. 20,80")
        parser.add_argument('--threads', type=int, default=1, help="Number of threads")
        parser.add_argument('--verbose', action='store_true', help="show attempted ports")
        parser.add_argument('--no-banner', action='store_true', help='Banner Print or Not')

        args = parser.parse_args()
        mytarget = Target(host=args.host,port=args.ports,thread=args.threads,verbose=args.verbose)
        if not args.no_banner:
           Banner()
        mytarget.scan()
     except KeyboardInterrupt:
        print(f"\n{colr.RED}[!] Scan interrupted by user.{colr.END}")
        sys.exit(0) 


def timed(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        func(*args,**kwargs)
        endti = time.perf_counter()
        print(f"{colr.GREEN}[End time]:{colr.END}{endti-start:.2f}")
    return wrapper

def run(host,verbose):
    while not toscanned.empty():
        port = toscanned.get()
        if verbose:
          print(f"{colr.GREEN}[*]{colr.END}Attempt:{port}")
        soc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        #soc.settimeout(1)
        try:
               soc.connect((host,port))
               try:
                  service = socket.getservbyport(port)
               except OSError:
                  service = SERVICE
               print(f"{colr.BLUE}{host}{colr.END} | {colr.RED}{port}{colr.END} | {colr.BLUE}{service}{colr.END}")
        except ConnectionRefusedError:
                #print(f"tying..{port}")
                pass
        finally:
                soc.close()
class Banner:
    def __init__(self):
         print(f"{colr.BOLD}{colr.BLUE} _____           _       ______{colr.END}")
         print(f"{colr.BOLD}{colr.BLUE}|  __ \         | |     |___  /{colr.END}")
         print(f"{colr.BOLD}{colr.BLUE}| |__) |__  _ __| |_ ____  / / {colr.END}")
         print(f"{colr.BOLD}{colr.BLUE}|  ___/ _ \| '__| __|_  / / /  {colr.END}")
         print(f"{colr.BOLD}{colr.BLUE}| |  | (_) | |  | |_ / / / /__ {colr.END}")
         print(f"{colr.BOLD}{colr.BLUE}|_|   \___/|_|   \__/___/_____|{colr.END}")
         print(f"-------{colr.GREEN}Simple &{colr.END} {colr.RED}Powerful{colr.END}-------")
         print("")
         print(f"{colr.YELLOW}|__      __|{colr.END}---------------------------------------|")
         print(f"{colr.YELLOW}|\ \ /\ / /|{colr.END} This tool is for educational use only |")
         print(f"{colr.YELLOW}| \ V  V / |{colr.END}---------Tool By: {colr.BOLD}sNEp{colr.END}--------------|")
         print(f"{colr.YELLOW}|  \_/\_/  |{colr.END}---------------------------------------|\n\n")
          
class Target:
    def __init__(self,host="127.0.0.1",port=None,thread=1,verbose=False):
        self.host = host
        self.port = port
        self.thread = thread
        self.verbose = verbose
        if "-" in self.port:
          try:
            splited = self.port.split("-")
            for  x in range(int(splited[0]),int(splited[1])+1):
                  toscanned.put(x) 
          except ValueError:
            print(f"{colr.RED}[ValueError]:{colr.END} You Can Use Format Like This 1-80 ")
            sys.exit(1)
        elif "," in self.port:
          try:
            splited = self.port.split(",")
            for x in splited:
                  toscanned.put(int(x))
          except ValueError:
            print(f"{colr.RED}[ValueError]:{colr.END} You Can Use Format Like This 1,80,8080 ")
            sys.exit(1)
        else:
            for x in range(1,1000):
                  toscanned.put(x)
            
    @timed
    def scan(self):
        tl = []
        for _ in range(1,self.thread+1):
            th = threading.Thread(target=run,args=(self.host,self.verbose))
            tl.append(th)
            th.start()
        for t in tl:
            t.join()
if __name__ == "__main__":
    from_cli()

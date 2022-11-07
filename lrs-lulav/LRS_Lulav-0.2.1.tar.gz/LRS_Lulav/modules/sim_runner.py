import argparse
from subprocess import Popen
from multiprocessing.pool import ThreadPool
import os

class Runner():
    def __init__(self):
        pass

    def serial_run(self, command):
        # run = Popen(command, executable='/bin/bash',  text=True, shell=True)
        os.system(command)

def main(args):
    # command = f"docker run --rm -it --net=host {args.docker} ros2 launch launches/LRS.launch.py test_run_id:={args.test_run_id}"
    command = f"docker run --rm -it --net=host {args.docker} ros2 launch {args.launch} test_run_id:={args.test_run_id}"
    
    print(" ------ command:", command)
    number_of_runs = args.reruns
    number_of_thread = 4

    tp = ThreadPool(number_of_thread)
    runner = Runner()
    for i in range(number_of_runs):                
        tp.apply_async(runner.serial_run(command), (i,))
    tp.close()
    tp.join()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description="LRS runner")
    parser.add_argument('docker', type=str, help='user id', default='vovacooper/demo_lulav_elbit:latest')            
    parser.add_argument('launch', type=str, help='launch file path', default='launches/LRS.launch.py')
    parser.add_argument('test_run_id', type=str, help='test run id')
    # parser.add_argument('simulation_run_id', type=str, help='simulation run id')
    
    parser.add_argument('reruns', 
                        type=int, 
                        help='number of times to run the simulation',
                        default=10)
    args = parser.parse_args()
    try:
        main(args)
    except Exception as e:
        print(e)


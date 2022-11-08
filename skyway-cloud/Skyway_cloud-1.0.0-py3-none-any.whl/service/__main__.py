from . import *
import argparse

class RegistAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_strings=None):
        setattr(namespace, 'actioned', None)
        service_name = values
        
        if assert_run(service_name):
            raise Exception('Service [%s] has been registered already!' % (service_name))
        
        update_run(service_name, update=False)
    
class StartAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_strings=None):
        setattr(namespace, 'actioned', None)
        start_service(values)
            
class StopAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_strings=None):
        setattr(namespace, 'actioned', None)
        stop_service(values)
        
class RestartAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_strings=None):
        setattr(namespace, 'actioned', None)
        stop_service(values)
        start_service(values)

class StatusAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_strings=None):
        setattr(namespace, 'actioned', None)
        body = []
        
        for service_name in services:
            if assert_run(service_name):            
                pinfo = get_status(service_name)
                body.append([service_name, pinfo['status'], '-' if pinfo['pid']==0 else pinfo['pid'], pinfo['update']])
        
        print("")
        print(tabulate(body, headers=['Service', 'Status', 'PID', 'Last Update']))
        print("")
    

parser = argparse.ArgumentParser(description='Manage Skyway micro-services.')
group = parser.add_mutually_exclusive_group()
group.add_argument('--status', action=StatusAction, metavar='service', nargs='?', help='status of one or all services')
group.add_argument('--start', action=StartAction, metavar='service', type=str, default='', help='start a service')
group.add_argument('--stop', action=StopAction, metavar='service', type=str, default='', help='stop a service')
group.add_argument('--restart', action=RestartAction, metavar='service', type=str, default='', help='restart a service')
group.add_argument('--regist', action=RegistAction, metavar='service', type=str, default='', help='register a service')
args = parser.parse_args()

if not hasattr(args, 'actioned'):
    parser.print_help()





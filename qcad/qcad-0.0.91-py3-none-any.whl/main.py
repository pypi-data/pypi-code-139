import time
import pyhik.hikvision


class CAD:
    def __init__(self, host, login, password, logger, callback_func=None,
                 delay_time=0.5, ):
        #self.cam = Client(host, login, password, timeout=30)
        self.camera = pyhik.hikvision.HikCamera(
            host, port=80,
            usr=login,
            pwd=password)
        self.callback_func = callback_func
        self.delay_time = delay_time
        self.logger = logger

    def set_callback_func(self, func):
        self.callback_func = func

    '''
    def mainloop2(self):
        self.logger.info('CAD has started work')
        if not self.callback_func:
            return 'Set callback_function first!'
        while True:
            response = self.cam.Event.notification.alertStream(method='get',
                                                               type='stream')
            self.logger.debug(
                f"CAD got event "
                f"{response[0]['EventNotificationAlert']['eventType']}")
            if self.cam_response_operator(response):
                self.logger.debug("CAD calling back")
                self.callback_func(response)
            time.sleep(self.delay_time)
    '''

    def mainloop(self):
        self.camera.start_stream()
        while True:
            events = self.camera.current_event_states
            if events and events['Motion'][0][0]:
                self.logger.debug("CAD calling back")
                self.callback_func(None)
            time.sleep(1)

    def cam_response_operator(self, response):
        if response[0]['EventNotificationAlert']['eventType'] == 'VMD':
            return True

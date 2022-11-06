import fastapi, uvicorn, threading

from . import object_controller



class Server:
	# TODO implement some security maybe

	def __init__(self, port: int, namespace):
		"""
		Opens the Python namespace for remote control of objects and variables.
		Without port forwarding works only on internal network, which is probably for the best. \n
		NOTE: Currently not secure in the slightest -
		anyone on the same network can access it just by knowing the port.

		:param port: any unique port for your program (use the same one on client)
		:param namespace: The starting point from the client's POV.
						  Tip: you can use __import__(__name__) if you want the current module.
		"""
		self.port = port
		self.namespace = namespace
		self.fastapi = fastapi.FastAPI()

		@self.fastapi.get('/test')
		def hello():
			return "Hello!"

		@self.fastapi.exception_handler(Exception)
		async def validation_exception_handler(request, err: Exception):
			return fastapi.responses.JSONResponse(status_code=500,
												  content={'detail': f"{err.__class__.__name__}: {err}"})

		object_controller.generate_functions(self.fastapi, namespace)


	def start(self, log=False):
		if log:
			log_level = None
		else:
			log_level = 'warning'
		uvicorn.run(self.fastapi, host='0.0.0.0', port=self.port, log_level=log_level)

	def start_in_thread(self, log=False):
		threading.Thread(target=self.start, kwargs={'log': log}, daemon=True).start()

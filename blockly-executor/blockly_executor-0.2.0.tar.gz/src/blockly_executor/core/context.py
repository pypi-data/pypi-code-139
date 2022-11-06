from datetime import datetime

from blockly_executor import Helper, ArrayHelper
from blockly_executor.core.exceptions import LimitCommand


class Context:
    def __init__(self):
        self.data = {}
        # self.params = {}  # параметры операции передающиеся между вызовами
        # self.variables = {}  # значения переменных
        # self.block_context = {'__thread_vars': {}}  # контекст текущего блока, показывется при отладке
        # self.operation = {}  # контекст операции
        # self.deferred = []
        self.is_deferred = False
        self.deferred_result = None
        self.limit_commands = 25

    def _init_from_dict(self, data):
        self.variables = data.get('var', {})
        self.block_context = data.get('block_context', {'__thread_vars': {}})
        self.operation = data.get('operation', {})
        self.deferred = data.get('deferred', [])

    @classmethod
    def init(cls, *, data=None, params=None):
        # if not operation_id:
        #     operation_id = str(uuid4())
        self = cls()
        if not data:
            self.operation = dict(
                # globalBegin=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                commands=[],
                # comment='',
                status='run',
                # progress=-1,
                # stepByStep=executor.step_by_step
            )
        else:
            self._init_from_dict(data)

        self.params = params if params else {}

        self.operation['begin'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return self

    def init_deferred(self, block_context):
        _self = self.__class__()
        # _self.params = self.params
        _self.block_context = block_context['block_context']
        _self.is_deferred = True
        _self.variables = self.variables
        # _self.operation = self.operation
        _self.deferred = self.deferred
        return _self

    def init_nested(self, block_context):
        _self = self.__class__()
        # _self.params = self.params
        _self.block_context = block_context.get('_context_debug', {})
        _self.is_deferred = True
        _self.variables = block_context.get('_context_variables', {})
        # _self.operation = self.operation
        _self.deferred = self.deferred
        return _self

    @property
    def operation_id(self):
        return self.operation.get('operation_id')

    def to_parallel_dict(self):
        return dict(
            var=self.variables,
            debug=self.block_context,
            operation=self.operation,
        )

    def to_dict(self):
        return dict(
            var=self.variables,
            debug=self.block_context,
            operation=self.operation,
            deferred=self.deferred,
        )

    @staticmethod
    def get_child_context(block_context):
        try:
            child_context = block_context['__child']
        except KeyError:
            child_context = {}
            block_context['__child'] = child_context
        return child_context

    @staticmethod
    def clear_child_context(block_context, result=None, delete_children=True):
        if delete_children:
            block_context.pop('__child', None)

    def copy(self):
        _self = Context()
        # _self.params = self.params
        _self.operation = self.operation
        _self.deferred = self.deferred
        _self.block_context = Helper.copy_via_json(self.block_context)
        # _self._init_from_dict(copy_via_json(self.to_dict()))
        return _self

    def add_deferred(self, deferred_exception):

        _local_context = deferred_exception.args[2]
        _operation_context = deferred_exception.args[1]
        try:
            i = ArrayHelper.find_by_key(self.deferred, _local_context['__deferred'], key_field='__deferred')
        except KeyError:
            self.deferred.append({})
            i = len(self.deferred) - 1

        self.deferred[i] = {
            '__deferred': _local_context['__deferred'],
            'block_context': Helper.copy_via_json(_operation_context.block_context)
        }

        try:
            i = ArrayHelper.find_by_key(self.commands, _local_context['__path'], key_field=2)
        except KeyError:
            self.commands.append([])
            i = len(self.commands) - 1
        self.commands[i] = deferred_exception.to_command()

    def check_command_limit(self):
        if len(self.commands) >= self.limit_commands:
            raise LimitCommand()

    def set_command_limit(self, step_by_step=False):
        self.limit_commands = 1 if step_by_step else 25

    @property
    def variables(self):
        try:
            return self.data['var']
        except KeyError:
            self.data['var'] = {}
            return self.data['var']

    @variables.setter
    def variables(self, value):
        self.data['var'] = value

    @property
    def block_context(self):
        try:
            return self.data['block_context']
        except KeyError:
            self.data['block_context'] = {'__thread_vars': {}}
            return self.data['block_context']

    @block_context.setter
    def block_context(self, value):
        self.data['block_context'] = value

    @property
    def current_workspace(self):
        try:
            return self.data['current_workspace']
        except KeyError:
            self.data['current_workspace'] = ''
            return self.data['current_workspace']

    @current_workspace.setter
    def current_workspace(self, value):
        self.data['current_workspace'] = value

    # @property
    # def current_block_context(self):
    #     try:
    #         return self.data['current_block_context']
    #     except KeyError:
    #         self.data['current_block_context'] = {}
    #         return self.data['current_block_context']
    #
    # @current_block_context.setter
    # def current_block_context(self, value):
    #     self.data['current_block_context'] = value

    @property
    def current_variables(self):
        try:
            return self.data['current_variables']
        except KeyError:
            self.data['current_variables'] = ''
            return self.data['current_variables']

    @current_variables.setter
    def current_variables(self, value):
        self.data['current_variables'] = value

    @property
    def deferred(self):
        try:
            return self.data['deferred']
        except KeyError:
            self.data['deferred'] = []
            return self.data['deferred']

    @deferred.setter
    def deferred(self, value):
        self.data['deferred'] = value

    @property
    def status(self):
        try:
            return self.data['status']
        except KeyError:
            self.data['status'] = 'run'
            return self.data['status']

    @status.setter
    def status(self, value):
        self.data['status'] = value

    @property
    def result(self):
        try:
            return self.data['result']
        except KeyError:
            self.data['result'] = {}
            return self.data['result']

    @result.setter
    def result(self, value):
        self.data['result'] = value

    @property
    def commands(self):
        try:
            return self.data['commands']
        except KeyError:
            self.data['commands'] = []
            return self.data['commands']

    @commands.setter
    def commands(self, value):
        self.data['commands'] = value

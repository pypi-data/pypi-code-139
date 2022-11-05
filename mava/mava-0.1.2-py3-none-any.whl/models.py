# Copyright (c) 2022 warevil <jg@warevil.dev>

from .constants import UNSET
from .fields import Field, FieldId


def get_slots(dct: dict) -> set:
    return {
        attribute
        for attribute, var_type in dct.items()
        if (not attribute.startswith('_') or attribute == '_id')
        and not str(var_type).startswith(('<function '))
    }


class MetaModel(type):
    def __new__(cls, name, bases, dictionary):
        slots = get_slots(dictionary)
        for base in bases:
            slots = slots.union(get_slots(base.__dict__))  # Inherited slots

        dictionary['__slots__'] = slots
        dictionary['_dict'] = {}
        for slot in slots:
            if slot in dictionary:
                dictionary[f'__{slot}'] = dictionary.pop(slot)

        return type.__new__(cls, name, bases, dictionary)


class Model(metaclass=MetaModel):
    def __new__(cls, **fields):
        instance = super().__new__(cls)
        slots = instance.__slots__
        for field in fields.keys():
            if field not in slots:
                error_msg = f'{instance.__class__.__name__} does not have a "{field}" field'
                raise AttributeError(error_msg)

        for slot in slots:
            field = getattr(instance, f'__{slot}')

            # If not a Field, simply assumes the element is valid
            if not isinstance(field, Field):
                setattr(instance, slot, field)
                instance._dict[slot] = field
                continue

            value = fields.get(slot, None)
            value = field.validate(cls, slot, value)
            setattr(instance, slot, value)
            instance._dict[slot] = value

        return instance


class BaseSaveModel(Model):
    '''
    Base model for saving an object instance to a database.
    You can inherit from this class or directly inherit from Model.
    This should be taken mostly as a reference.
    '''

    _id = FieldId(default=UNSET)

    @classmethod
    def _add(cls, **attributes):
        '''
        Creates a new instance and calls the save method bypassing
        the attributes double-checking.
        '''
        model = cls(**attributes)
        model._save()
        return model

    @classmethod
    def _check_unique(cls, **attributes):
        '''
        Validates a field with a unique constraint.
        '''

    @classmethod
    def _get(cls, **attributes):
        '''
        Return an instance if all passed attributes match.
        You must override this method with your own implementation.
        '''

    def _save(self):
        '''
        Occurs at the end of a save operation, when all fields have been validated.
        You must override this method with your own implementation.
        '''

    def save(self):
        '''
        This operation validates values passed to Fields.
        If a non-Field is detected, it will accept any values passed, so be careful.
        You must override "_save" method with your own implementation.
        '''
        is_new = self._id == UNSET
        for slot in self.__slots__:
            value = getattr(self, slot)
            if self._dict[slot] == value:  # Already validated
                continue

            field = getattr(self, f'__{slot}')
            if not isinstance(field, Field):  # Cannot validate without a Field
                continue

            validate_method = field.validate_update
            if is_new:
                validate_method = field.validate

            value = validate_method(self, slot, value)
            setattr(self, slot, value)

        self._save()

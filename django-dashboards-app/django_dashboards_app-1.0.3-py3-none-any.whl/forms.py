from django import forms


# Custom Forms
BOOLEAN_NULL_CHOICES = [
    ('', '---------'),
    ('True', 'Si'),
    ('False', 'No')
]

NULL_CHOICE = ('', '---------')


class AbstractModelForm(forms.ModelForm):

    class Meta:
        fields = '__all__'

    def __init__(self, *args, **kwargs):

        self.action = kwargs.pop('action', None)
        self.app_name = kwargs.pop('app_name', None)

        super().__init__(*args, **kwargs)

        self.abstract_prepare()

    def abstract_prepare(self):
        print('abstract_prepare')
        
        #exclude_fields_name = f'{self._meta.model.__name__.upper()}_{self.action.upper()}_EXCLUDE_FIELDS'
        #exclude_fields = getattr(__import__(f'{ self.app_name }.configs', fromlist=[exclude_fields_name]), exclude_fields_name)

        #for field in exclude_fields:
        #    self.fields.pop(field, None)

        getattr(self, 'abstract_' + self.action)()

    def abstract_detail(self):
        print('abstract_detail')

        for field in self.fields:
            self.fields[field].widget.attrs['disabled'] = 'disabled'

    def abstract_create(self):
        print('abstract_create')

    def abstract_update(self):
        print('abstract_update')

    def abstract_duplicate(self):
        print('abstract_duplicate')

    def abstract_filter(self):
        print('abstract_filter')

        for field, type in self.fields.items():

            self.fields[field].required = False

            field_type_class_name = type.__class__.__name__

            if field_type_class_name == 'TypedChoiceField':

                self.fields[field].widget.choices.insert(0, NULL_CHOICE)
                self.fields[field].initial = ''

            elif field_type_class_name in ['DecimalField', 'FloatField', 'PositiveIntegerField', 'IntegerField']:

                # min and max
                extrems = self._meta.model.objects.aggregate(Min(field), Max(field))

                self.fields[field].widget = forms.TextInput()
                self.fields[field].widget.attrs['class'] = 'range'
                self.fields[field].widget.attrs['data_min'] = extrems[field + '__min']
                self.fields[field].widget.attrs['data_max'] = extrems[field + '__max']
                self.fields[field].widget.attrs['readonly'] = True
                self.fields[field].widget.attrs['style'] = "border:0;"
                self.fields[field].initial = ''

            elif field_type_class_name in ['DateField', 'TimeField', 'DateTimeField']:

                self.fields[field].widget.attrs['class'] = 'periodpicker'

            elif field_type_class_name in ['BooleanField']:

                self.fields[field].widget = forms.Select()
                self.fields[field].widget.choices = BOOLEAN_NULL_CHOICES
                self.fields[field].initial = ''


class AbstractConfirmationForm(forms.Form):

    ok = forms.IntegerField(widget=forms.HiddenInput(), initial=1, label='')
    next = forms.CharField(label='', widget=forms.HiddenInput(), required = False)
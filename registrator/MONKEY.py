

def apply_monkey():
    fuck = 'gAJjZGphbmdvLmRiLm1vZGVscy5maWVsZHMKTk9UX1BST1ZJREVECnEBLg=='

    from django.db.models.fields import Field, NOT_PROVIDED

    Field.__init_nomonkey__ = Field.__init__

    def field_monkey(self, *args, **kwargs):
        try:
            if fuck in kwargs.get('default', ''):
                kwargs['default'] = NOT_PROVIDED
        except:
            pass
        self.__init_nomonkey__(*args, **kwargs)

    Field.__init__ = field_monkey

    #

    from django.forms.fields import Field

    Field.__init_nomonkey__ = Field.__init__

    def field_monkey(self, *args, **kwargs):
        try:
            if fuck in kwargs.get('initial', ''):
                kwargs['initial'] = None
        except:
            pass
        self.__init_nomonkey__(*args, **kwargs)

    Field.__init__ = field_monkey

    '''
    from mutant.models import FieldDefinition

    FieldDefinition.__save_nomonkey__ = FieldDefinition.save

    def field_monkey(self, *args, **kwargs):
        try:
            if fuck in self.default:
                self.default = NOT_PROVIDED
        except:
            pass
        return self.__save_nomonkey__(*args, **kwargs)

    FieldDefinition.save = field_monkey
    '''

    from userlayers.api import TablesResource
    from picklefield.fields import dbsafe_decode

    TablesResource.__dehydrate_nomonkey__ = TablesResource.dehydrate

    def field_monkey(self, bundle):
        result = self.__dehydrate_nomonkey__(bundle)
        for f in result.data['fields']:
            if 'choices' in f.data:
                choices = []
                for choice in f.data['choices']:
                    try:
                        choice['value'] = dbsafe_decode(choice['value'])
                    except:
                        pass
                    choices.append(choice)
                f.data['choices'] = choices


        return result

    TablesResource.dehydrate = field_monkey

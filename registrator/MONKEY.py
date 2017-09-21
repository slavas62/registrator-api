def apply_monkey():
    from django.db.models import Field, NOT_PROVIDED

    Field.__init_nomonkey__ = Field.__init__

    def field_monkey(self, *args, **kwargs):
        try:
            if 'gAJjZGphbmdvLmRiLm1vZGVscy5maWVsZHMKTk9UX1BST1ZJREVECnEBLg==' in kwargs.get('default', ''):
                kwargs['default'] = NOT_PROVIDED
        except:
            pass
        self.__init_nomonkey__(*args, **kwargs)

    Field.__init__ = field_monkey

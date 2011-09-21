from django import forms

from mongotools.forms.fields import MongoFormFieldGenerator as MongotoolsGenerator

from documentoptions import AdminOptions

def init_document_options(document):
    if not hasattr(document, '_admin_opts') or not isinstance(document._admin_opts, AdminOptions):
        document._admin_opts = AdminOptions(document)
    if not isinstance(document._meta, AdminOptions):
        document._meta = document._admin_opts
    return document

def get_document_options(document):
    return AdminOptions(document)

class MongoFormFieldGenerator(MongotoolsGenerator):
    """This class generates Django form-fields for mongoengine-fields."""
    
    def generate(self, field_name, field):
        """Tries to lookup a matching formfield generator (lowercase 
        field-classname) and raises a NotImplementedError of no generator
        can be found.
        """
        try:
            return super(MongoFormFieldGenerator, self).generate(field_name, field)
        except NotImplementedError:
            # a normal charfield is always a good guess
            # for a widget.
            # TODO: Somehow add a warning
            kwargs = {'required': field.required}
            
            if hasattr(field, 'min_length'):
                kwargs['min_length'] = field.min_length
                
            if hasattr(field, 'max_length'):
                kwargs['max_length'] = field.max_length
            
            if hasattr(field, 'default'):
                kwargs['initial'] = field.default
            
            return forms.CharField(kwargs)


from __future__ import unicode_literals
import copy

from twilix.base.velement import VElement
from twilix.base.myelement import MyElement
from twilix.base.exceptions import ElementParseError
from twilix import fields as f

class ValidationError(Exception):
    pass

class FormField(f.NodeProp):
    def __init__(self, var, field_type, label=None, default=None, initial=None,
                 required=False, *args, **kwargs):
        self.var = var
        self.field_type = field_type
        self.initial = initial
        default = field_type(label=label, value=initial, var=var,
                             required=required, **kwargs)
        self.kwargs = kwargs
        super(FormField, self).__init__(field_type.elementName,
                                        listed=False, default=default,
                                        required=False)

    def __unicode__(self):
        return '%s %s FormField' % (self.var, self.field_type.fieldType)

    def get_from_el(self, el):
        r = [r for r in el.children if not isinstance(r, str) and \
                   r.attributes.get('var', None) == self.var and \
                   getattr(r, 'name', None) == self.xmlnode]
        if r:
            return r[0]

    def to_python(self, value):
        if value is None:
            pass
        elif isinstance(value, VElement):
            pass
        else:
            value = self.field_type.createFromElement(value, **self.kwargs)
        return value

class Form(VElement):
    elementName = 'x'
    elementUri = 'jabber:x:data'

    type_ = f.StringAttr('type')
    title = f.StringNode('title', required=False)
    instructions = f.StringNode('instructions', required=False)

    def clean_type_(self, value):
        if value not in ('form', 'submit', 'cancel', 'result'):
            raise ElementParseError
        return value

    def clean(self):
        if self.type_ != 'submit':
            return
        for fname in self.fields:
            field = getattr(self, fname)
            value = field.fclean(field.value)
            field.value = value

    @property
    def fields(self):
        fields = []
        for name, attr in list(self.nodesProps.items()):
            if isinstance(attr, FormField):
                fields.append(name)
        return fields

    def make_submit_form(self):
        assert self.type_ == 'form'
        sform = copy.deepcopy(self)
        fields = sform.fields
        for name in fields:
            field = getattr(sform, name)
            field.prepare_to_submit()
            setattr(sform, name, field)
        sform.type_ = 'submit'
        sform.title = None
        sform.instructions = None
        return sform

    def make_cancel_form(self):
        assert self.type_ == 'form'
        sform = copy.deepcopy(self)
        sform.children = []
        sform.type_ = 'cancel'
        return sform

# TODO: ReportedForm

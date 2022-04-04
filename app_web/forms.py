from django.forms import Form, FileField
from django.utils.translation import gettext_lazy as _

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class UploadQRCodeForm(Form):
    file = FileField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout.fields.append(
            FormActions(
                Submit('submit', _('Lookup')),
                # Button('cancel', _('Cancel')),
            ),
        )

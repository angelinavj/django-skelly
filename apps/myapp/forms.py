# -*- coding: utf-8 -*-
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
from django.utils.translation import ugettext_lazy as _
from registration.helpers import render_email
from django.core.mail import mail_managers
from django.core.urlresolvers import reverse

from getpaid.forms import PaymentMethodForm as _PaymentMethodForm


class PaymentMethodForm(_PaymentMethodForm):
    def __init__(self, order, *args, **kwargs):
        kwargs['initial'] = {'order': order}
        super(PaymentMethodForm, self).__init__(order.currency, *args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = reverse('getpaid-new-payment', kwargs={'currency': order.currency})
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            'order',
            'backend',
            FormActions(
                Submit('submit', _('Continue'), css_class="btn-primary"),
                Submit('cancel', _('Cancel')),
            )
        )

class ContactForm(forms.Form):
    email = forms.EmailField(label=_("E-mail"), required=True)
    message = forms.CharField(label=_("Message"), widget=forms.Textarea(), required=True)

    # Uni-form
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
        Field('email', css_class='input-xlarge'),
        Field('message', rows="10", css_class='input-xlarge'),

        FormActions(
            Submit('submit', _('Send'), css_class="btn-primary"),
            Submit('cancel', _('Cancel')),
        )
    )

    def __init__(self, email_template, *args, **kwargs):
        self.email_template = email_template

        super(ContactForm, self).__init__(*args, **kwargs)

    def render_email(self, data):
        return render_email(self.email_template, data)

    def send_email(self, email):
        return mail_managers(*email)

    def save(self):
        email = self.render_email(self.cleaned_data)

        return self.send_email(email)

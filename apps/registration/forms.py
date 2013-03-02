# -*- coding: utf-8 -*-
from django import forms

from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
from django.utils.translation import ugettext_lazy as _
from registration.models import RegistrationProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm as LoginForm, \
                                    PasswordResetForm as ResetForm, \
                                    SetPasswordForm as SetPassForm, \
                                    PasswordChangeForm as ChangeForm

def _registration_form_helper(*fields):
    register_fields = (
        Field('username', css_class='input-xlarge'),
        Field('email', rows="3", css_class='input-xlarge'),
        Field('password1', rows="3", css_class='input-xlarge'),
        Field('password2', rows="3", css_class='input-xlarge')
    )
    button_fields = (
        FormActions(
            Submit('save', _('Register'), css_class="btn-primary"),
            Submit('cancel', _('Cancel')),
        ),
    )

    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(*(register_fields + fields + button_fields))

    return helper

class SetPasswordForm(ChangeForm):
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
        Field('new_password1', css_class='input-xlarge'),
        Field('new_password2', css_class='input-xlarge'),
        FormActions(
            Submit('submit', _('Set password'), css_class="btn-primary"),
            Submit('cancel', _('Cancel')),
        ),
    )

class PasswordChangeForm(ChangeForm):
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
        Field('old_password', css_class='input-xlarge'),
        Field('new_password1', css_class='input-xlarge'),
        Field('new_password2', css_class='input-xlarge'),
        FormActions(
            Submit('submit', _('Change password'), css_class="btn-primary"),
            Submit('cancel', _('Cancel')),
        ),
    )

class PasswordResetForm(ResetForm):
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
        Field('email', css_class='input-xlarge'),
        FormActions(
            Submit('submit', _('Reset password'), css_class="btn-primary"),
            Submit('cancel', _('Cancel')),
        ),
    )

class AuthenticationForm(LoginForm):
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
        Field('username', css_class='input-xlarge'),
        Field('password', rows="3", css_class='input-xlarge'),
        FormActions(
            Submit('submit', _('Login'), css_class="btn-primary"),
            Submit('cancel', _('Cancel')),
        ),
    )

class RegistrationFormUniqueEmail(object):
    """ Subclass of ``RegistrationForm`` which enforces uniqueness of email addresses. """
    def clean_email(self):
        """ site. """
        email = self.cleaned_data['email']

        if User.objects.filter(email__iexact=email):
            error_msg = _("This email address is already in use. Please supply a different email address.")
            raise forms.ValidationError(error_msg)

        return email

class RegistrationForm(forms.Form):
    username = forms.RegexField(label=_("Username"), regex=r'^[\w.@+-]+$', max_length=30, required=True)
    email = forms.EmailField(max_length=75, label=_("E-mail"), required=True)
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label=_("Password (again)"), widget=forms.PasswordInput, required=True)

    def clean_username(self):
        """ Validate that the username is alphanumeric and is not already in use. """
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("A user with that username already exists."))

    def clean(self):
        """ Verifiy that the values entered into the two password fields match.
        Note that an error here will end up in  ``non_field_errors()``
        because it doesn't apply to a single field."""
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return self.cleaned_data

    # Uni-form
    helper = _registration_form_helper()

class RegistrationFormTermsOfService(RegistrationForm):
    """Subclass of ``RegistrationForm`` which adds a required checkbox
    for agreeing to a site's Terms of Service. """
    tos = forms.BooleanField(label=_(u'I have read and agree to the Terms of Service'),
                             error_messages={'required': _("You must agree to the terms to register")})

    helper = _registration_form_helper(Field('tos', rows="3"))

class RegistrationRestrictForm(RegistrationFormTermsOfService, RegistrationFormUniqueEmail):
    pass


class UserForm(forms.ModelForm, RegistrationFormUniqueEmail):
    username = forms.RegexField(label=_("Username"), regex=r'^[\w.@+-]+$', max_length=30, required=True)
    email = forms.EmailField(max_length=75, label=_("E-mail"), required=True)
    
    class Meta:
        model = User

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(label=_("First name"), max_length=30, required=True)
    last_name = forms.CharField(label=_("Last name"), max_length=30, required=True)

    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
        Field('first_name', rows="3", css_class='input-xlarge'),
        Field('last_name', rows="3", css_class='input-xlarge'),
        FormActions(
            Submit('submit', _('Save'), css_class="btn-primary"),
            Submit('cancel', _('Cancel')),
        ),
    )

    class Meta:
        model = RegistrationProfile
        fields = ('first_name', 'last_name')

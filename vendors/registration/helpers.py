from django.template.loader import render_to_string

def render_email(filename, args):
    message = render_to_string(filename, args).splitlines()
    subject = ''.join(message.pop(0).splitlines())
    message = "\n".join(message)
    return subject, message


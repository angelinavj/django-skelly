from django.views.generic.detail import DetailView
from django.template.response import TemplateResponse
from myapp.forms import ContactForm, PaymentMethodForm
from myapp.models import Order
from django.http import Http404

class OrderView(DetailView):
    model = Order
    template_name = 'myapp/payment.html'

    def get_object(self, queryset=None):
        obj = super(OrderView, self).get_object(queryset)
        if obj.user != self.request.user:
            raise Http404()
        return obj

    def get_context_data(self, **kwargs):
        context = super(OrderView, self).get_context_data(**kwargs)
        context['payment_form'] = PaymentMethodForm(self.object)
        return context

def index(request):
    return TemplateResponse(request, 'index.html')

def payment(request):
    order = Order(name='test', user=request.user)
    order.save()

    form = PaymentMethodForm(order)

    return TemplateResponse(request, 'myapp/payment.html', {'form': form})

def contact(request, email_template="myapp/contact_email.txt"):
    if request.method == 'POST':
        form = ContactForm(email_template, request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ContactForm(email_template)

    return TemplateResponse(request, 'myapp/contact.html', {'form': form})

    

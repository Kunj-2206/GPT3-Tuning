from django.shortcuts import render

# Create your views here.
def ChatbotView(request):
    return render(request=request, template_name="chatbotUI.html")



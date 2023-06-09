from django.shortcuts import render
from GPT3_Tuner.forms import TextInputForm, TempSlider, TokenSlider, TopSlider
from GPT3_Tuner.chatbot import generate_response
from GPT3_Tuner.GPT_Param_Pred import param_prediction, generate_model
import csv
# Create your views here.
def ChatbotView(request):
    GPT_response = ""
    user_prompt=""
    form = TextInputForm(my_widget_attr_value=user_prompt)
    tempSlider = TempSlider(my_widget_attr_value=0.1)
    tokenSlider = TokenSlider(my_widget_attr_value=1)
    topSlider = TopSlider(my_widget_attr_value=0.1)
    if request.method == 'POST':
        if(request.POST.get('respBtn')):
            user_prompt = request.POST.get('text_input')
            temperature = request.POST.get('temp_slider')
            max_tokens = request.POST.get('token_slider')
            top_p = request.POST.get('top_slider')
            GPT_response = generate_response(user_prompt, float(temperature), int(max_tokens), float(top_p))
            print(GPT_response)
            filename = "GPT3_Tuner/prompt_dataset.csv"
            with open(filename, 'a') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow([f"{user_prompt}", temperature, max_tokens, top_p])
                csvfile.close()
            return render(request=request, template_name="chatbotUI.html", context={'textForm': form, 'tempSlider':tempSlider, 'tokenSlider':tokenSlider, 'topSlider':topSlider, 'GPT_response':GPT_response, 'info':'Your current parameter settings is being saved to database and will use it further to make prediction of other prompt parameter. We are creating a personalized dataset of your prompt'})

        if(request.POST.get('modelBtn')):
            generate_model()
            return render(request=request, template_name="chatbotUI.html", context={'textForm': form, 'tempSlider':tempSlider, 'tokenSlider':tokenSlider, 'topSlider':topSlider, 'GPT_response':GPT_response, 'info':'Your model is trained'})


        if(request.POST.get('paramBtn')):
            user_prompt = request.POST.get('text_input')
            temperature, max_tokens, top_p = param_prediction(user_prompt)
            GPT_response = generate_response(user_prompt, float(temperature), int(max_tokens), float(top_p))
            tempSlider = TempSlider(my_widget_attr_value=temperature)
            tokenSlider = TokenSlider(my_widget_attr_value=max_tokens)
            topSlider = TopSlider(my_widget_attr_value=top_p)
            form = TextInputForm(my_widget_attr_value=user_prompt)
            return render(request=request, template_name="chatbotUI.html", context={'textForm': form, 'tempSlider':tempSlider, 'tokenSlider':tokenSlider, 'topSlider':topSlider, 'GPT_response':GPT_response, 'info':'This is ChatGPT3 Tuner.It has total 3 function first to generate response based on your parameter, third is to predict the parameter based on available data and second parameter for tune the machine learning model again.'})
    
    
    return render(request=request, template_name="chatbotUI.html", context={'textForm': form, 'tempSlider':tempSlider, 'tokenSlider':tokenSlider, 'topSlider':topSlider, 'GPT_response':GPT_response, 'info':'This is ChatGPT3 Tuner.It has total 3 function first to generate response based on your parameter, third is to predict the parameter based on available data and second parameter for tune the machine learning model again.'})



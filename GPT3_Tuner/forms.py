from django import forms

class TextInputForm(forms.Form):
    text_input = forms.CharField(required=False,max_length=10000, widget=forms.widgets.Textarea(attrs={"rows":12, "cols":25, "id":"textbox1", 'value':''}))
    
    def __init__(self, *args, **kwargs):
        my_widget_attr_value = kwargs.pop('my_widget_attr_value', {})
        super().__init__(*args, **kwargs)
        if my_widget_attr_value is not None:
            widget = self.fields['text_input'].widget
            widget.attrs['value'] = my_widget_attr_value
            self.fields['text_input'].widget = widget
            
class TempSlider(forms.Form):
    temp_slider = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'type': 'range', 'step': '0.01', 'min': '0.1', 'max': '1.0','value': '0.1', 'onChange': 'rangeSlide1(this.value)', 'onmousemove':'rangeSlide1(this.value)', 'onblur': 'rangeSlide1(this.value)'}))

    def __init__(self, *args, **kwargs):
        my_widget_attr_value = kwargs.pop('my_widget_attr_value', {})
        super().__init__(*args, **kwargs)
        if my_widget_attr_value is not None:
            widget = self.fields['temp_slider'].widget
            widget.attrs['value'] = my_widget_attr_value
            self.fields['temp_slider'].widget = widget
            
class TokenSlider(forms.Form):
    token_slider = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'type': 'range', 'step': '1', 'min': '1', 'max': '4000', 'value': '1','onChange': 'rangeSlide2(this.value)', 'onmousemove':'rangeSlide2(this.value)', 'onblur': 'rangeSlide2(this.value)'}))

    def __init__(self, *args, **kwargs):
        my_widget_attr_value = kwargs.pop('my_widget_attr_value', {})
        super().__init__(*args, **kwargs)
        if my_widget_attr_value is not None:
            widget = self.fields['token_slider'].widget
            widget.attrs['value'] = my_widget_attr_value
            self.fields['token_slider'].widget = widget
            
class TopSlider(forms.Form):
    top_slider = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'type': 'range', 'step': '0.01', 'min': '0.1', 'max': '1.0', 'value': '0.1', 'onChange': 'rangeSlide3(this.value)', 'onmousemove':'rangeSlide3(this.value)', 'onblur': 'rangeSlide3(this.value)'}))
    
    def __init__(self, *args, **kwargs):
        my_widget_attr_value = kwargs.pop('my_widget_attr_value', {})
        super().__init__(*args, **kwargs)
        if my_widget_attr_value is not None:
            widget = self.fields['top_slider'].widget
            widget.attrs['value'] = my_widget_attr_value
            self.fields['top_slider'].widget = widget
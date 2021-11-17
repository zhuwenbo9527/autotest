from django import forms
from . import models

class ApitestModelForm(forms.ModelForm):
    class Meta:
        model = models.Apitest
        fields = (
                  'Product',
                  'apitestfeature',
                  'apiteststory',
                  'apitestresult',
                  'apitester',)

ApistepModelFormSet = forms.inlineformset_factory(models.Apitest,
                                                  models.Apistep,
                                                  fields = ('waittime',
                                                            'title',
                                                            'url',
                                                            'apimethod',
                                                            'apiparamvalue',
                                                            'exceptresponse',
                                                            'actualresponse',
                                                            'result',
                                                            'apistatus',
                                                            'Apitest',
                                                            'headers'),
                                                  extra=1,
                                                  )
from django import forms
from . import models


class ApitestModelForm(forms.ModelForm):
    class Meta:
        model = models.Apitest
        fields = ('id',
                  'Product',
                  'apitestfeature',
                  'apiteststory',
                  'apitestresult',
                  'apitester',)


class ApistepModelForm(forms.ModelForm):
    class Meta:
        model = models.Apistep
        fields = ('id',
                  'waittime',
                  'title',
                  'url',
                  'headers',
                  'apimethod',
                  'apiparamvalue',
                  'exceptresponse',
                  'result',
                  'apistatus')


ApistepModelFormSet = forms.inlineformset_factory(parent_model=models.Apitest,
                                                  model=models.Apistep,
                                                  fields=('id',
                                                  'waittime',
                                                  'title',
                                                  'url',
                                                  'headers',
                                                  'apimethod',
                                                  'apiparamvalue',
                                                  'exceptresponse',
                                                  'result',
                                                  'apistatus'),
                                                  extra=1,
                                                  can_delete=True,
                                                  )
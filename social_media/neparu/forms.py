from django import forms
from django.forms import ModelForm
from neparu.models import User,Post, Notification, Rental
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import DateInput





class UploadPost(forms.ModelForm):
    class Meta:
        model = Post
        fields =('title',)


class UploadProfile(forms.ModelForm):
    class Meta:
        model = User
        fields =('photo',)



class Blood(forms.ModelForm):
    class Meta:
        model = Notification
        fields =('content','description','blood_group')


class Notification(forms.ModelForm):
    class Meta:
        model = Notification
        fields =('description',)
        widgets = {
                'description': forms.TextInput(attrs={'required':'required'}),
            }


class Rental(forms.ModelForm):
    class Meta:
        model = Rental
        fields = ('title','price','space_no','description','location')

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        unique_together = ('email',)
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2' )


class SignUpFormUpdate(forms.ModelForm):
    op = (
        ('private','Private'),
        ('public','Public')
        )

    account_type = forms.ChoiceField(required=True, choices=op)

    # email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name','email','blood_group','bio','account_type' )
        widgets = {
                'username': forms.TextInput(attrs={'readonly':'readonly'}),
                'email': forms.TextInput(attrs={'readonly':'readonly'}),
            }
        


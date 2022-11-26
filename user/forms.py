
from django import forms
from .models import User




class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    

    class Meta:
        model = User
        fields = ('name', 'email', 'password1', 'password2')


    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['name'].widget.attrs['placeholder'] = 'Name'

        

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
    
    def clean_email(self): 
        user_email = self.cleaned_data.get('email')
        if user_email:
            user_query_set = User.objects.filter(email=user_email)
            if user_query_set:
                self.add_error('email', 'Email is already exist try different one ')        

    
    
    

    # def save(self, commit=True):
    #     # Save the provided password in hashed format
    #     user = super().save(commit=False)
    #     print(self.cleaned_data["password1"], '************')
    #     user.set_password(self.cleaned_data["password1"])
    #     if commit:
    #         user.save()
    #     return user

     


class UserLogin(forms.Form):
    email  = forms.EmailField()
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    

    def __init__(self, *args, **kwargs):
        super(UserLogin, self).__init__(*args, **kwargs)
        
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'


    def clean(self):
        cleaned_data = super().clean()
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2: 
            if password1 != password2:
                # raise forms.ValidationError('Password Not Matched')
                self.add_error('password2', "passwords do not match !")


class UserProfile(forms.ModelForm):

    class Meta:
        model = User 
        fields = ('pic', 'email', 'name', 'mobile_number', 'address', )
        
        
    def clean_email(self): 
        user_email = self.cleaned_data.get('email')
        if user_email:
            user_query_set = User.objects.filter(email=user_email)
            if user_query_set:
                self.add_error('email', 'Email is already exist try different one ')        

         

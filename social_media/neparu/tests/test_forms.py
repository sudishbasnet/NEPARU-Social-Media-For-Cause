from django.test import TestCase
from neparu import forms,models

class TestSignupForm(TestCase):
    def test_signup_form1(self):
        dat = {
            "username": "user",
            "first_name": "user",
            "last_name" : "seventy",
            "email":"user@test.com",
            "password1": "blabit2539",
            "password2": "blabit2539"
            }

        self.form(dat)  

    def test_signup_form2(self):
        dat = {
            "username": "user",
            "first_name": "",
            "last_name" : "seventy",
            "email":"user@test.com",
            "password1": "blabit2539",
            "password2": "blabit2539"
        }
        self.form(dat) 

    def test_signup_form3(Self):
        dat = {
            "username": "user",
            "first_name": "sudish",
            "last_name" : "",
            "email":"user@test.com",
            "password1": "blabit2539",
            "password2": "blabit2539"
        }
        self.form(dat)  

    def test_signup_form4(Self):
        dat = {
            "username": "user",
            "first_name": "user",
            "last_name" : "seventy",
            "email":"",
            "password1": "blabit2539",
            "password2": "blabit2539"
        }

        self.form(dat)

    def test_signup_form5(Self):
        dat = {
            "username": "user",
            "first_name": "user",
            "last_name" : "seventy",
            "email":"user@test.com",
            "password1": "",
            "password2": "blabit2539"
        }
         
        self.form(dat)


    def test_signup_form6(Self):
        dat = {
            "username": "user",
            "first_name": "user",
            "last_name" : "seventy",
            "email":"user@test.com",
            "password1": "blabit2539",
            "password2": ""
        }
        
        self.form(dat) 


        
        
    def form(self,dat):
        form = forms.SignUpForm(data=dat)
        form.is_valid()
        self.assertFalse(form.errors) 
           




class TestRentalForm(TestCase):
    def test_rental_form(self):
        dat = {
            "title" : "House",
            "price" : 2222,
            "space_no": 22,
            "description" : "very beautiful house",
            "location" : "sankhamul",
        }
        self.form(dat)
    
    def test_rental_form1(self):
        dat = {
            "title" : "House",
            "price" :'' ,
            "space_no": 22,
            "description" : "very beautiful house",
            "location" : "sankhamul",
        }
        self.form(dat)

    def test_rental_form2(self):
        dat = {
            "title" : "House",
            "price" : 2222,
            "space_no":'' ,
            "description" : "very beautiful house",
            "location" : "sankhamul",
        }
        self.form(dat)

    def test_rental_form3(self):
        dat = {
            "title" : "House",
            "price" : 2222,
            "space_no": 22,
            "description" : "",
            "location" : "sankhamul",
        }
        self.form(dat)


    def test_rental_form4(self):
        dat = {
            "title" : "House",
            "price" : 2222,
            "space_no": 22,
            "description" : "very beautiful house",
            "location" : "",
        }
        self.form(dat)



    def form(self,dat):
        form = forms.Rental(data=dat)
        form.is_valid()
        self.assertFalse(form.errors)




class TestSigupUpdate(TestCase):
    def test_Signupupate(self):
        dat = {
            'username':'sudish',
            'first_name' : 'sudish',
            'last_name' : 'basnet',
            'email' : 'sudishbasnet@gmail.com',
            'blood_group' : '',
            'bio': '',
            'account_type' :'private'
        }
        self.form(dat)


    def test_Signupupate1(self):
        dat = {
            'username':'',
            'first_name' : 'sudish',
            'last_name' : 'basnet',
            'email' : 'sudishbasnet@gmail.com',
            'blood_group' : '',
            'bio': '',
            'account_type' :'private'
        }
        self.form(dat)

    def test_Signupupate2(self):
        dat = {
            'username':'sudish',
            'first_name' : '',
            'last_name' : 'basnet',
            'email' : 'sudishbasnet@gmail.com',
            'blood_group' : '',
            'bio': '',
            'account_type' :'private'
        }
        self.form(dat)

    
    def test_Signupupate3(self):
        dat = {
            'username':'sudish',
            'first_name' : 'sudish',
            'last_name' : '',
            'email' : 'sudishbasnet@gmail.com',
            'blood_group' : '',
            'bio': '',
            'account_type' :'private'
        }
        self.form(dat)

    def test_Signupupate4(self):
        dat = {
            'username':'sudish',
            'first_name' : 'sudish',
            'last_name' : 'basnet',
            'email' : '',
            'blood_group' : '',
            'bio': '',
            'account_type' :'private'
        }
        self.form(dat)

    

    def form(self,dat):
        form = forms.SignUpFormUpdate(data=dat)
        form.is_valid()
        self.assertFalse(form.errors)






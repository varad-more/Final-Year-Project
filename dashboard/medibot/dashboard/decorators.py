from django.shortcuts import render, redirect
""" 
The decorator for checking if user or admin is signed in.
If user is not logged in is redirected to signin

"""

def doctor_logged_in(f):
        def wrap(request, *args, **kwargs):
                #this check the session if userid key exist, if not it will redirect to login page
                if 'user_role' not in request.session.keys():
                    request.session['error'] = "You are not authorized to view the page. Sign In to view."
                    return redirect("signin")
                
                elif request.session['user_role'] == 'doctor' :
                    return f(request, *args, **kwargs)
        wrap.__doc__=f.__doc__
        wrap.__name__=f.__name__
        return wrap

def receptionist_logged_in(f):
        def wrap(request, *args, **kwargs):
                #this check the session if userid key exist, if not it will redirect to login page
                if 'user_role' not in request.session.keys():
                    request.session['error'] = "You are not authorized to view the page. Sign In as Receptionist to view."
                    return redirect("signin")
                
                elif request.session['user_role'] == 'receptionist' :
                    return f(request, *args, **kwargs)
        wrap.__doc__=f.__doc__
        wrap.__name__=f.__name__
        return wrap


def admin_logged_in(f):
        def wrap(request, *args, **kwargs):
                #this check the session if userid key exist, if not it will redirect to login page
                if 'user_role' not in request.session.keys():
                    return redirect("signin")
                
                elif request.session['user_role'] == 'admin' :
                    return f(request, *args, **kwargs)
        wrap.__doc__=f.__doc__
        wrap.__name__=f.__name__
        return wrap


def hash_password (password):
    import hashlib
    import os

    # salt = os.urandom(32) # Remember this
    salt = b'varad'
    # key = b'\x07\x0fV=<\xe7r\xa7\x85\xe5\xe44H>\\\x13\xad\x18l\xba~\xe4\xb1\x99\x96cz\xb4\x92\x94\x829'
    # print ('salt', salt)
    # password = 'password123'

    key = hashlib.pbkdf2_hmac(
        'sha256', # The hash digest algorithm for HMAC
        password.encode('utf-8'), # Convert the password to bytes
        salt, # Provide the salt
        100000 # It is recommended to use at least 100,000 iterations of SHA-256 
    )

    return key
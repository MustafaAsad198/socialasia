***Some features cannot be implemented on the deployed website for now because it uses advanced python libraries for ML or graph plotting (like sklearn,numpy,networkx,matplotplib,Tensorflow,Keras) and shitty Python Anywhere does not provide enough space to install all these packages (They all work fine on localserver). Sorry for the inconvenience caused***

# Socialasia

### Tech-Stack used:
* Python
* Django Rest Framework
* HTML, CSS, JavaScript, and Bootstrap
* Tensorflow, Keras (for image classification)
* sklearn's Decision tree machine learning algorithm
* matplotlib

### clone the repository

```
git clone https://github.com/MustafaAsad198/socialasia
```

### install requirements

```
pip install requirements.txt
```

### run migration to register models in admin
```
python manage.py makemigrations
python manage.py migrate
```

### create a super user for admin panel
```
python manage.py createsuperuser
```

### to run django server on your localhost
```
python manage.py runserver
```

You can open the local server and try implenting the APIs through given URL patterns in dashboard/urls.py.

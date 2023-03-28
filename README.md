# FFRM API
Football Field Reservation Management API

<hr>

## `Clone repository`
```bash
git clone https://github.com/voidnowhere/FFRM_API.git
```

<hr>

## `Set up environment`
### Install `virtualenv`
```bash
pip install virtualenv
```
### Change current directory to `FFRM_API`
```bash
cd FFRM_API
```
### Create python `virtual environment`
```bash
python -m venv venv
```
### Activate it
- `Command Prompt`
```bash
venv\Scripts\activate.bat
```
- `Linux` or `PowerShell`
```bash
source venv/Scripts/activate
```
- `PowerShell`
no scripts like the activate script are allowed to be executed so you need to run PowerShell as `admin` and change `ExecutionPolicy` to `AllSigned` then type `A` to `Always run` `the command is under` in the end use `the command above` to activate virtual environment
```bash
Set-ExecutionPolicy AllSigned
```
### Install `virtualenv requirements`
```bash
pip install -r requirements.txt
```
### Make `migrations`
```bash
python manage.py makemigrations
```
### Apply `migrations`
```bash
python manage.py migrate
```
### Create your `superuser` for `django admin site`
```bash
python manage.py createsuperuser
```
### Run server
```bash
python manage.py runserver
```

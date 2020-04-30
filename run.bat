@echo Download Support Library
workon cdc
pip install -r requirements.txt

@echo reload cdc_python
@python manage.py runserver 8080
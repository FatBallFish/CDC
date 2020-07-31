@echo Download Support Library
pip install -r requirements.txt

@echo reload cdc_python
@start python manage.py runserver 0.0.0.0:8848
@exit
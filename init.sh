ite
pip install -r requirements.txt
chmod +x manage.py
./manage.py migrate
./manage.py loaddata sites

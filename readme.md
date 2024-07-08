<h1>Announcemates - An announcement center</h1>

<h3>Start project</h3>
<p><b>install requirements</b> pip install -r requirements.txt</p>
<p><b>migrate</b> python manage.py migrate</p>
<p><b>run</b>python manage.py runserver</p>
<br>
<br>

<h3>Run redis</h3>
<p><b>In docker</b>docker run -p 6379:6379 --name some-redis -d redis</p>
<p> install redis if docker is not installed</p>

<h3>Run celery</h3>
<p>To send emails<p>
<p>celery -A src worker --loglevel=info<p>
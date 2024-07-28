<h1>Announcemates - An announcement center</h1>

<h3>Start project</h3>
<pre><b>install requirements</b>    pip install -r requirements.txt</pre>
<pre><b>migrate</b>     python manage.py migrate</pre>
<pre><b>run</b>     python manage.py runserver</pre>
<br>
<br>

<h3>Run redis</h3>
<pre><b>In docker:</b>  docker run -p 6379:6379 --name some-redis -d redis</pre>
<p> install redis if docker is not installed</p>

<h3>Run celery</h3>
<p>To send emails<p>
<p>celery -A src worker --loglevel=info<p>
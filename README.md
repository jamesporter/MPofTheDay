# MPofTheDay

Learn about a new UK MP every day and take action.

## Installing the app locally

```
# Set up a virtualenv
virtualenv env

# activate it
source env/bin/activate

# install requirements
pip install -r requirements.txt
```

Then to run the app, it’s:

```
gunicorn app:app
```

## Fetching data

You’ll need a [TWFY API key](http://www.theyworkforyou.com/api/key). Once you
have that, make a local copy of constants.py from the stub.

```
cp constants.py.in-git constants.py
```

…and update constants.py with your key.

For the summary stuff, you’ll need NLTK English corpus.

At a python prompt, run:

```python
nltk.download()
```

Then to gather the data, it’s:

```
python cron.py
```

And wait for 650 dots (one per MP) to appear.


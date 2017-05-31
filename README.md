# smtp-file-updater
Grabs remote files over SFTP if they're newer than the local copy.

## Installing
Built for Python 3. Run `pip install -r requirements.txt`, ideally within
a virtualenv.


## Running
1. Copy `config_example.yml` to `config.yml`. Put in your connection information and configure
   the files you wish to copy.
2. Run `python grab.py`
3. To run frequently, add it to cron or to Windows scheduler.

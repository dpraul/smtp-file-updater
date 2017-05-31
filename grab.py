import os
import logging
import logging.config

import yaml
import subprocess
import pysftp


with open('config.yml') as config_file:
    config = yaml.load(config_file)

logging.config.fileConfig('logging.conf')

logger = logging.getLogger('grab-remote-files')


def main():
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None  # disable checking hostkeys

    any_updated = False

    with pysftp.Connection(config['hostname'], username=config['username'],
                           password=config['password'], cnopts=cnopts) as sftp:
        for remote, local in config['files'].items():
            try:
                remote_stats = sftp.stat(remote)
            except FileNotFoundError:
                logger.error('Remote file %s does not exist - quitting' % remote)
                return
            if not os.path.isfile(local) or os.path.getmtime(local) < remote_stats.st_mtime:
                any_updated = True
                sftp.get(remote, local, preserve_mtime=True)
                logger.info('Updated %s' % local)
            else:
                logger.info('Did not update %s' % local)

    if any_updated:
        logger.info('Updated files, running post_script')
        subprocess.check_call(config['post_script'], shell=True)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.error('Hit an unexpected error: %s' % e)

import os
import configparser
import tempfile
from datetime import datetime, timedelta
from time import mktime
import feedparser
import urllib.request
import zipfile


def main():
    configfile = 'settings.cfg'
    config = configparser.ConfigParser()
    if os.path.isfile(configfile):
        # read the config
        config.sections()
        config.read(configfile)
        InstallPath = config['DEFAULT']['InstallPath']
        print('install path is ', InstallPath)
        UpdatedDate = datetime(int(config['DEFAULT']['UpdateYear']),
                               int(config['DEFAULT']['UpdateMonth']),
                               int(config['DEFAULT']['UpdateDay']),
                               0, 0, 0)
        print('sysinternals last updated on ', UpdatedDate)
    else:
        print("file does not exist")
#        create the file
        InstallPath = input('It looks like you ' +
                            'haven''t run this program before. ' +
                            'Where would you like to save your ' +
                            'sysinternals programs? ')
        UpdatedDate = datetime(1937, 1, 1, 0, 0, 0)
        config['DEFAULT'] = {'InstallPath': InstallPath, 'UpdateYear': '1937', 'UpdateMonth': '01', 'UpdateDay': '01'}
        with open(configfile, 'w') as theConfig:
            config.write(theConfig)

#    try to read the current version from the rss feed
    sifeed = feedparser.parse('http://blogs.technet.com/b/sysinternals/rss.aspx')
    latestDate = sifeed.entries[0]['published_parsed']
    print('latest sysinternals release: ', datetime.fromtimestamp(mktime(latestDate)))

#    if current version is newer than installed
    if datetime.fromtimestamp(mktime(latestDate)) - UpdatedDate >= timedelta(days=1):
        print('latest is newer than installed, need to update.')
        temp = tempfile.gettempdir()
        zipname = temp + '\\sysinternals.zip'
        print('temp is: ', temp)
        try:
#            download latest
            urllib.request.urlretrieve('https://download.sysinternals.com/files/SysinternalsSuite.zip', zipname)
            print('latest downloaded')

#            unzip to install path
            if not os.path.exists(InstallPath):
                os.makedirs(InstallPath)
            sizip = zipfile.ZipFile(zipname)
            print('extracting files from zip')
            sizip.extractall(InstallPath)
            sizip.close()
#            delete zip archive
            os.remove(zipname)

#            update config last updated date values
            config.set('DEFAULT', 'UpdateYear', str(latestDate[0]))
            config.set('DEFAULT', 'UpdateMonth', str(latestDate[1]))
            config.set('DEFAULT', 'UpdateDay', str(latestDate[2]))
            with open(configfile, 'w') as theConfig:
                config.write(theConfig)

        except:
            print('something went wrong with the download')
            raise

    else:
        print('Sysinterals is already up to date.')

if __name__ == "__main__":
    main()

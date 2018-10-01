#/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Daniel Godoy 01/10/2018

from __future__ import division
import argparse,requests,urlparse,sys

class bcolors:
    BLUE = '\033[94m'
    RED = '\033[91m'
    GREEN = '\033[32m'
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    YELLOW = "\033[93m"
    MAGENTA = "\033[95m"
    GREY = "\033[90m"
    DEFAULT = "\033[0m"

def banner():
    print bcolors.GREY+""
    print "                                              ##          ## "
    print "                                                ##      ##    "    
    print "                                              ############## "
    print "                                            ####  ######  #### "
    print "                                          ###################### "
    print "                                          ##  ##############  ##     "
    print "                                          ##  ##          ##  ## "
    print "                                                ####  ####"
    print ""
 
def details():
    print bcolors.WHITE+"                              =[" + bcolors.YELLOW + "CRX Analyzer v0.0.0 "
    print ""


class ChromeCRXDownloader():
    CRX_URL = "https://clients2.google.com/service/update2/crx?" \
              "response=redirect&prodversion=38.0&x=id%3D~~~~%26installsource%3Dondemand%26uc"
    USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36"
    global headers
    headers = {
        "User-Agent": USER_AGENT,
        "Referer": "https://chrome.google.com",
    }

    def __init__(self):
        pass

    def download(self, _download_url_, _file_name_):
        try:
            r = requests.get(url=_download_url_, headers=headers, stream=True)
            redirects = r.history
            if len(redirects) > 0:
                redirect_header = redirects[-1].headers
                if "location" in redirect_header:
                    loc = redirect_header["location"]
                    uparse = urlparse.urlparse(loc)
                    splits = uparse.path.split("/")
                    _fname_ = splits[-1]

            if _fname_:
                _file_name_ = _fname_.replace("extension", _file_name_)
            else:
                _file_name_ += ".crx"
            r_headers = r.headers
            content_length = None
            if "content-length" in r_headers:
                content_length = int(r_headers["content-length"])

            if content_length:
                print bcolors.OKGREEN+"Bajando %s. \nTamaño del Archivo %s "  % (_file_name_, self.convert_bytes(content_length))
                print "\n"
                print "hola mundo"
            else:
                print bcolors.OKGREEN+"Bajando %s \n"  % _file_name_
                print "\n"

            chunk_size = 16 * 1024
            dowloaded_bytes = 0
            with open(_file_name_, 'wb') as fd:
                for chunk in r.iter_content(chunk_size):
                    fd.write(chunk)
                    dowloaded_bytes += len(chunk)
                    sys.stdout.write("\r" + self.convert_bytes(dowloaded_bytes))
                    sys.stdout.flush()
                    print "3"
        except Exception, e:
            raise ValueError(bcolors.WARNING+"Error en Descarga %s " % _download_url_, e)

    def parse(self, chrome_store_url):
        try:
            uparse = urlparse.urlparse(chrome_store_url)
            if uparse.netloc != "chrome.google.com":
                raise ValueError("URL Invalida %s" % chrome_store_url)
            splits = uparse.path.split("/")
            if not (len(splits) == 4 and uparse.path.startswith("/webstore/detail/")):
                raise ValueError("URL Invalida%s" % chrome_store_url)
        except Exception, e:
            pass

        return splits[-1], splits[-2]

    def convert_bytes(self, len_in_byte):
        in_kb = len_in_byte / 1024
        in_mb = in_kb / 1024
        in_gb = in_mb / 1024
        if in_kb < 1024:
            return "%.2f KB" % in_kb

        if in_mb < 1024:
            return "%.2f MB" % in_mb

        if in_gb > 1:
            return "%.2f GB" % in_gb


if __name__ == '__main__':
    banner()
    details()
    url_parse = raw_input('URL de la Extension: ')
    downloader = ChromeCRXDownloader()
    try:
        file_name = None
        chrome_app_id, file_name = downloader.parse(chrome_store_url=url_parse)
        if chrome_app_id:
            download_url = downloader.CRX_URL.replace("~~~~", chrome_app_id)
            downloader.download(download_url, file_name)
    except Exception, e:
        print e
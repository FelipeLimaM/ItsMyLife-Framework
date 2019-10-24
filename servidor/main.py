import webapp2
import jinja2
from cryptography.fernet import Fernet
from paste.urlparser import StaticURLParser
from paste.cascade import Cascade
import os, json
import api_list_file as firebase
import export_csv
import export_reduced
import zipfile as zf
import pandas as pd
import machine_learning.pre_processing as pre
from machine_learning.clustering import Clustering
from battery import ExportBattery, BatteryGraphic as BG
from sensorhub import ExportSensorHub, SensorHubGraphic as SHG
from bluetooth import ExportBluetooth, BluetoothGraphic
from wifi import ExportWifi, WifiGraphic
import utils
from threading import Thread
import codes
# from machine_learning import MachineLearning


KEY_IML = Fernet.generate_key()
KEY_IML = 'G5uBexn4SniCdeYwGYB0dht9v9Rq0tAUYGqae0Q5pF0=' #DEBUG



JINJA_ENVIRONMENT = jinja2.Environment(autoescape=True,
loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'views')))


# Class that defines the web enviroment
class Template(webapp2.RequestHandler):
  def render_template(self, view_filename, params={}):
      template = JINJA_ENVIRONMENT.get_template(view_filename)
      self.response.write(template.render(params))

class GetFiles(Template):
    def get(self):
        json_dict = firebase.init()
        print json_dict
        params = { 'json' : json_dict}
        self.render_template('firebase.html', params)

class ComputeEngine(Template):
    def get(self):
        filename = self.request.get("filename")
        params = {'filename' : filename}
        self.render_template('modal.html', params)

    def post(self):
        params = {'KEY_IML':KEY_IML}
        try:
            params['email'] = self.request.get("email")
            params['filename'] = self.request.get("filename")
            params['optimzation_sensor_hub'] = True if self.request.get("optimzation_sensor_hub") else False
            params['bluetooth'] = True if self.request.get("bluetooth") else False
            params['wifi'] = True if self.request.get("wifi") else False
            params['number'] = self.request.get("number")
        except Exception as e:
            raise

        thread = Thread(target = codes.exec_ML, args = ((params),))
        thread.start()

        self.render_template('thanks.html', {})


class DownloadDatabase(Template):

    def post(self):
        params = {
            'filename':self.request.get("filename"),
            'email':self.request.get("email"),
            'KEY_IML': KEY_IML
        }

        thread = Thread(target = codes.download_database, args = ((params),))
        thread.start()

        self.render_template('thanks.html', {})

class BatteryGraphic(Template):

    def post(self):
        params = {
            'filename':self.request.get("filename"),
            'email':self.request.get("email"),
            'KEY_IML': KEY_IML
        }
        thread = Thread(target = codes.simple_battery, args = ((params),))
        thread.start()
        self.render_template('thanks.html', {})


class SensorHubGraphic(Template):

    def post(self):
        params = {
            'filename':self.request.get("filename"),
            'email':self.request.get("email"),
            'KEY_IML': KEY_IML
        }
        thread = Thread(target = codes.simple_sensorHub, args = ((params),))
        thread.start()
        self.render_template('thanks.html', {})


class BLEGraphic(Template):

    def post(self):
        params = {
            'filename':self.request.get("filename"),
            'email':self.request.get("email"),
            'KEY_IML': KEY_IML
        }
        thread = Thread(target = codes.simple_bluetooth, args = ((params),))
        thread.start()
        self.render_template('thanks.html', {})


class WIFIGraphic(Template):

    def post(self):
        params = {
            'filename':self.request.get("filename"),
            'email':self.request.get("email"),
            'KEY_IML': KEY_IML
        }
        thread = Thread(target = codes.simple_wifi, args = ((params),))
        thread.start()
        self.render_template('thanks.html', {})

class FilterGraphic(Template):
    def get(self):
        filename = self.request.get("filename")
        mlistble, mlistwifi = utils.get_list(filename)
        params = {'filename' : filename, 'mlistwifi':mlistwifi, 'mlistble':mlistble}
        self.render_template('especialgraphic.html', params)


class BluetoothSpecificGraphic(Template):
    def post(self):
        params = {
            'filename':self.request.get("filename"),
            'email':self.request.get("email"),
            'ble_list': self.request.get_all("ble_list"),
            'is_blacklist': False if self.request.get("blacklist") else True,
            'KEY_IML': KEY_IML,
        }
        thread = Thread(target = codes.filter_simple_bluetooth, args = ((params),))
        thread.start()
        self.render_template('thanks.html', {})


class WifiSpecificGraphic(Template):
    def post(self):
        params = {
            'filename':self.request.get("filename"),
            'email':self.request.get("email"),
            'wifi_list': self.request.get_all("ble_list"),
            'is_blacklist': False if self.request.get("blacklist") else True,
            'KEY_IML': KEY_IML,
        }
        thread = Thread(target = codes.filter_simple_wifi, args = ((params),))
        thread.start()
        self.render_template('thanks.html', {})


class PermalinkDownload(Template):
    def get(self):
        crypto_path_real = self.request.get("filename")
        crypto_path_graphic = self.request.get("config")
        cipher_suite = Fernet(KEY_IML)
        path_real = cipher_suite.decrypt(bytes(crypto_path_real))
        path_graphic = cipher_suite.decrypt(bytes(crypto_path_graphic))

        crypto_level = self.request.get("key")
        if crypto_level:
            level = cipher_suite.decrypt(bytes(crypto_level))
            crypto_old_params = self.request.get("extra")
            old_params = cipher_suite.decrypt(bytes(crypto_old_params))
            params = {
                'level_html' : int(level),
                'filename': crypto_path_real,
                'config': crypto_path_graphic,
                'url': utils.create_link(KEY_IML,path_real,path_graphic),
                'params': old_params,
            }
            self.render_template('download_file.html', params)
        else:
            utils.response_download_file(self,path_real,path_graphic)

class ContinueML(Template):
    def post(self):
        try:
            params = {
                'path_real':self.request.get("filename"),
                'email':self.request.get("email"),
                'filename':self.request.get("config"),
                'level_html':int(self.request.get("level_html")),
                'number':self.request.get("number"),
                'params':self.request.get("params"),
                'KEY_IML': KEY_IML,
            }
        except Exception as e:
            raise

        cipher_suite = Fernet(KEY_IML)
        params['path_real'] = cipher_suite.decrypt(bytes(params['path_real']))
        params['filename'] = cipher_suite.decrypt(bytes(params['filename']))
        params.update(json.loads(params['params']))

        print params

        thread = Thread(target = codes.continue_ML, args = ((params),))
        thread.start()
        self.render_template('thanks.html', {})


class AdvancedOptionsMachineLearning(Template):
    def get(self):
        filename = self.request.get("filename")
        int_time, finish_time = utils.get_period(filename)
        mlistble, mlistwifi = utils.get_list(filename)
        params = {'filename' : filename, 'mlistwifi':mlistwifi, 'mlistble':mlistble, 'int_time':int_time , 'finish_time':finish_time}
        self.render_template('machineLearningAdvanced.html', params)

    def post(self):
        try:
            params = {
                'filename':self.request.get("filename"),
                'email':self.request.get("email"),
                'optimzation_sensor_hub':True if self.request.get("optimzation_sensor_hub") else False,
                'bluetooth':True if self.request.get("bluetooth") else False,
                'wifi':True if self.request.get("wifi") else False,
                'number':self.request.get("number"),
                'KEY_IML': KEY_IML,
                'period':self.request.get("period"),
                'set_period':True if self.request.get("set_period") else False,
            }
            if params['set_period']:
                params['init_time'] ,params['finish_time'] = utils.parsePeriod(params['period'])
            if params['bluetooth']:
                params['ble_list'] = self.request.get_all("ble_list")
                params['is_blacklist_ble'] = False if self.request.get("blacklist_ble") else True
                params['is_only_hardcode'] = True if self.request.get("bluetooth_hardcode") else False

            if params['wifi']:
                params['wifi_list'] = self.request.get_all("wifi_list")
                params['is_blacklist_wifi'] = False if self.request.get("blacklist_wifi") else True
        except Exception as e:
            raise

        thread = Thread(target = codes.exec_ML, args = ((params),))
        thread.start()
        self.render_template('thanks.html', {})



def main():
    from paste import httpserver
    httpserver.serve(app, host='0.0.0.0', port='8081')


static_app = StaticURLParser("static/")

web_app = webapp2.WSGIApplication([
    ('/', GetFiles),
    ('/computeEngine', ComputeEngine),
    ('/downloaddatabase', DownloadDatabase),
    ('/batterygraphic', BatteryGraphic),
    ('/sensorhubgraphic', SensorHubGraphic),
    ('/blegraphic', BLEGraphic),
    ('/wifigraphic', WIFIGraphic),
    ('/bluetoothspecificgraphic',BluetoothSpecificGraphic),
    ('/wifispecificgraphic',WifiSpecificGraphic),
    ('/advancedoptions', AdvancedOptionsMachineLearning),
    ('/permalink', PermalinkDownload),
    ('/specificgraphic',FilterGraphic),
    ('/continueML',ContinueML)


], debug=True)
# Create a cascade that looks for static files first, then tries the webapp
app = Cascade([static_app, web_app])


if __name__ == '__main__':
    main()

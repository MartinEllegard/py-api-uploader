import json
from os.path import isfile
import requests
import os
import glob
from dataclasses import dataclass, field

@dataclass
class Settings:
    baseurl: str = ""
    useSSl: bool = False
    methods: list[str] = field(default_factory=list)

    def fromJson(self, jsonObject):
        self.baseurl = jsonObject.baseurl
        self.useSSl = jsonObject.useSSl
        for method in jsonObject.methods:
            self.methods.append(method)

def main():
    # Static vars
    inputPath = 'test-input/'
    outputPath = 'test-output/'

    settingsFilename = 'settings.json'
    settings = Settings()
    
    if not os.path.exists(settingsFilename):
        print("Let's create a settings file :)")
        settings.baseurl = input('type down the base url to the api you will be testing: ')
        settings.useSSl = input('do you want to verify ssl?(y/n)') == 'y'
        methods = input('Add the methods you want to be able to post to seperated by , : ').split(',')
        for method in methods:
            settings.methods.append(method)

        with open(settingsFilename, encoding='utf-8', mode='w') as settingsFile:
            settingsFile.write(json.dumps(settings.__dict__))
        print('Settings file created!')
        
    else:
        with open(settingsFilename, encoding='utf-8', mode='r') as settingsFile:
            settings.fromJson(json.load(settingsFile))

    # apiUrl = ""
    # if input('Do you want to convert test data to polygons?(y/n) ') == 'y':
    #     apiUrl = "https://localhost:7099/Ais/PostAisWithConversion"
    # else:
    #     apiUrl = '"https://localhost:7099/Ais/PostAis"'

    # for filename in glob.glob(os.path.join(inputPath, '*.geojson')):
    #     baseFilename = filename.split('/')[1]

    #     with open(filename, encoding='utf-8', mode='r') as jsonFile:
    #         jsondata = json.load(jsonFile)

    #         result = requests.post(apiUrl, json=jsondata, verify=False)

    #         if result.ok:
    #             jsonResult = result.json()
    #             with open(os.path.join(outputPath, baseFilename), encoding='utf-8', mode='w') as outputFile:
    #                 outputFile.write(json.dumps(jsonResult))

    # print('success')


if __name__ == "__main__":
    main()

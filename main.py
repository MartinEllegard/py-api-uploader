import json
import requests
import os
import glob
from dataclasses import dataclass, field

@dataclass
class Settings:
    settingsFilename: str = "settings.json"
    baseurl: str = ""
    useSSl: bool = False
    endpoints: list[str] = field(default_factory=list)

    def settingsExist(self):
        if os.path.exists(self.settingsFilename):
            return True
        else:
            return False

    def loadSettings(self):
        with open(self.settingsFilename, encoding='utf-8', mode='r') as settingsFile:
            self.fromJson(json.load(settingsFile))

    def createSettings(self):
        self.baseurl = input('type down the base url to the api you will be testing: ')
        self.useSSl = input('do you want to verify ssl?(y/n)') == 'y'
        endpoints_input = input('Add the endpoints you want to be able to post to seperated by , : ').split(',')
        for endpoint in endpoints_input:
            self.endpoints.append(endpoint)

        with open(self.settingsFilename, encoding='utf-8', mode='w') as settingsFile:
            settingsFile.write(json.dumps(self.__dict__))

        print('Settings file created!')

    def fromJson(self, jsonObject):
        print(jsonObject)
        self.baseurl = jsonObject["baseurl"]
        self.useSSl = jsonObject["useSSl"]
        for endpoint in jsonObject["endpoints"]:
            self.endpoints.append(endpoint)
    def selectEndpoint(self):
        endpointsString = ""
        for index, endpoint in enumerate(self.endpoints):
            endpointsString += f"{index + 1}: {endpoint}, /n"

        print(endpointsString)

        selectedEndpointString = input("What endpoint do you want to use?")
        selectedEndpoint = 0
        try:
            selectedEndpoint = int(selectedEndpointString)
        except ValueError:
            print("Didn't type a number setting  method to 1")

        selectedEndpoint = selectedEndpoint - 1

        if len(self.endpoints) >= selectedEndpoint:
            return self.endpoints[selectedEndpoint]
        else:
            return self.endpoints[0]

def main():
    # Static vars
    inputPath = 'test-input/'
    outputPath = 'test-output/'

    setup = Settings()

    if setup.settingsExist():
        setup.loadSettings()
    else:
        setup.createSettings()

    endpoint = setup.selectEndpoint()

    for filename in glob.glob(os.path.join(inputPath, '*.geojson')):
        baseFilename = filename.split('/')[1]

        with open(filename, encoding='utf-8', mode='r') as jsonFile:
            jsondata = json.load(jsonFile)

            result = requests.post(setup.baseurl + endpoint, json=jsondata, verify=False)

            if result.ok:
                jsonResult = result.json()
                with open(os.path.join(outputPath, baseFilename), encoding='utf-8', mode='w') as outputFile:
                    outputFile.write(json.dumps(jsonResult))

    print('success')


if __name__ == "__main__":
    main()

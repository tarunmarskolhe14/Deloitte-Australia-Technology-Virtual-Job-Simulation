import os
import json
import unittest
import datetime


# Get current directory of this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Load JSON files safely
with open(os.path.join(BASE_DIR, "data-1.json"), "r", encoding="utf-8") as f:
    jsonData1 = json.load(f)

with open(os.path.join(BASE_DIR, "data-2.json"), "r", encoding="utf-8") as f:
    jsonData2 = json.load(f)

with open(os.path.join(BASE_DIR, "data-result.json"), "r", encoding="utf-8") as f:
    jsonExpectedResult = json.load(f)


# Convert Format 1 to unified format
def convertFromFormat1(jsonObject):
    loc_parts = jsonObject["location"].split("/")
    if len(loc_parts) != 5:
        raise ValueError("Invalid location format in Format 1")

    location = {
        "country": loc_parts[0],
        "city": loc_parts[1],
        "area": loc_parts[2],
        "factory": loc_parts[3],
        "section": loc_parts[4]
    }

    return {
        "deviceID": jsonObject["deviceID"],
        "deviceType": jsonObject["deviceType"],
        "timestamp": jsonObject["timestamp"],
        "location": location,
        "data": {
            "status": jsonObject["operationStatus"],
            "temperature": jsonObject["temp"]
        }
    }


# Convert Format 2 to unified format
def convertFromFormat2(jsonObject):
    dt = datetime.datetime.fromisoformat(jsonObject["timestamp"].replace("Z", "+00:00"))
    millis = int(dt.timestamp() * 1000)

    return {
        "deviceID": jsonObject["device"]["id"],
        "deviceType": jsonObject["device"]["type"],
        "timestamp": millis,
        "location": {
            "country": jsonObject["country"],
            "city": jsonObject["city"],
            "area": jsonObject["area"],
            "factory": jsonObject["factory"],
            "section": jsonObject["section"]
        },
        "data": {
            "status": jsonObject["data"]["status"],
            "temperature": jsonObject["data"]["temperature"]
        }
    }


# Dispatcher function
def main(jsonObject):
    if "device" in jsonObject:
        return convertFromFormat2(jsonObject)
    else:
        return convertFromFormat1(jsonObject)


# Unit tests
class TestSolution(unittest.TestCase):

    def test_sanity(self):
        result = json.loads(json.dumps(jsonExpectedResult))
        self.assertEqual(
            result,
            jsonExpectedResult
        )

    def test_dataType1(self):
        result = main(jsonData1)
        self.assertEqual(
            result,
            jsonExpectedResult,
            'Converting from Type 1 failed'
        )

    def test_dataType2(self):
        result = main(jsonData2)
        self.assertEqual(
            result,
            jsonExpectedResult,
            'Converting from Type 2 failed'
        )


# Run tests
if __name__ == '__main__':
    unittest.main(verbosity=2)

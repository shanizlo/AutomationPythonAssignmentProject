from web_client import WebClient
from json_parser import JsonParser
from json_viewer_page import JsonViewPage

TEST_URL = "http://a360ci.s3.amazonaws.com/Jmx/einat_world_bank.json"
TEST_FILE = TEST_URL.split("/")[-1]  # einat_world_bank.json
TEST_VALUE = "090224b0817be218_1_0"
TEST_ERROR_TEXT = "Invalid JSON variable"

"""
1.
    Implement in Python a function that downloads the following .json file from a storage server (s3) to your local 
    machine. Save it to your machine as 'einat_world_bank.json'
"""
def part_1():
    print("Downloading {}".format(TEST_FILE))
    client = WebClient()
    client.download(TEST_URL, TEST_FILE)


"""
2.
    Implement in Python a function that reads the einat_world_bank.json file from your local machine
    and check/validate that the file contain the following value: 090224b0817be218_1_0
"""
def part_2():
    print("Verifying {} exists in {}".format(TEST_VALUE, TEST_FILE))
    with open("einat_world_bank.json", "rb") as json_file:
        for line in json_file.readlines():
            json = JsonParser(line)
            if json.has_value(TEST_VALUE):
                return
        raise Exception("Can't find '{}' in JSON".format(TEST_VALUE))


"""
3. 
    A. Open a web browser (any web browser type - Chrome/Firefox you choice) 
    B. go to url: http://jsonviewer.stack.hu/
    C. add into the main text field all the text from the 'einat_world_bank.json' file.
    D. Click on the 'Format' button on the upper toolbar.
    E. validate that the web browser contains the value '090224b0817be218_1_0'
    F. Click on the 'viewer' button(tab)
    G. clicking on the viewer button should cause to an error message with the following text 'Invalid JSON variable'.
    Your task is that the script will check that the system raised this error message (it is the expected behaviour)
"""
def part_3():
    print("Navigating to the JSON test web page")
    json_view = JsonViewPage()
    print("Loading JSON from URL {}".format(TEST_URL))
    json_view.load_json_from_url(TEST_URL)  # alternatively, I could copy+paste the downloaded file content.
    print("Formatting JSON")
    json_view.format_json()
    print("Validating JSON content")
    text = json_view.get_json_text()
    if TEST_VALUE not in text:
        raise Exception("Can't find {} in the JSON text area".format(TEST_VALUE))
    print("Switching to viewer")
    json_view.switch_to_viewer()
    print("Validating error dialog")
    error = json_view.get_error_message()
    if not error:
        raise Exception("Expected an error message but didn't get one")
    if TEST_ERROR_TEXT not in error:
        raise Exception("Expected '{}' error message but got {} instead".format(TEST_ERROR_TEXT, text))
    print("Done")

"""
Entry method
"""
def main():
    part_1()
    part_2()
    part_3()


if __name__ == '__main__':
    main()

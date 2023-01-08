# swagger-test-automation

## Pet Swagger Flask based Framework

### Installing Virtualenv & Python dependencies.
1. Go to root folder of repo on Terminal.
2. `cd bin/`
3. `pip install -r requirements.txt`

### Downloading Pycharm IDE on your system:
Download/Install Pycharm from [here](https://www.jetbrains.com/pycharm/download/download-thanks.html?platform=mac&code=PCC)

### Selecting the python Interpreter on your machine.
If you are setting up Pycharm for first time on your machine, then you need to specify the project interpreter(we have just created).
1. Open Pycharm IDE. --> Preferences.
2. Open Project Interpreter
3. Click on Settings icon --> Click Add.
4. On Add Python Interpreter Page, Click on Existing environment --> Click on ellipsis (...) button.
5. Navigate to `<Repo_Local_Path>/bin/virtualenv/swagger-test-automation/bin/python` and click on OK.
6. Click on Apply, OK to save settings.

### Upgrading your code base
1. Please repeat [these steps](#installing-virtualenv--python-dependencies) to install a new virtual environment for python3.
2. Set up the recently created virtual env `venv` using the steps mentioned [here](#selecting-the-python-interpreter-on-your-machine).
**Important:** It is very important to select `venv` as mentioned in Step 5 to [Select Python interpreter](#selecting-the-python-interpreter-on-your-machine).
3. Restart pycharm to update the IDE to detect anomalies w.r.t to python3.
4. Happy Coding!

### Opening project in Pycharm
1. Open Pycharm IDE. --> File --> Open.
2. Navigate to the root path of aquila.
3. Click on OK.

### For running the tests locally
1. `python -m swagger`
2.  Hit APIs from Postman or Curl as we are using Flask request/response model
    Since, server will be up at 5010, so use the following to hit the requests.
    URL: POST `http://localhost:5010/swagger/run_tests`
    Payload: `{
    "swagger": {
        "api_key": "special-key",
        "url": "https://petstore.swagger.io/v2"
    },
    "tags_list": ["pet"]
}`
3. tags_list is a list containing which test cases to run, which maps with tag_list in file `testData/tests.py`
4. For generating a very basic PDF report of the final result and test cases executed, use the ID received in `run_tests` API response like:
    URL: GET `http://localhost:5010/download/report/{id}`
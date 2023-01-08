def validate_response(actual, response):
    exclusions = []
    for i in actual.keys():
        if i not in exclusions and (
            i not in response.keys() or str(actual[i]) != str(response[i])
        ):
            return False

    return True

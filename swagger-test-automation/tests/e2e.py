from petstore import Pet, User
from petstore.pet_service.pet_service import PetService
from petstore.user_service.user_service import UserService
from testData.mappings import service_key_mappings
from utils.logger import Log, Logger

logger = Logger().get_logger()


def setup_swagger(
    payload: dict,
    unique_id: str,
) -> object:
    """
    Function initialises the instances of all services and returns them

    :param payload: Swagger pets' payload
    :param cache: The cache object
    :param unique_id: The logger execution id
    :return: instance of conversion service
    """

    log = Log(execution_id=unique_id)
    if "swagger" in list(payload.keys()):
        swagger_instance = Pet(
            base_url=payload.get("swagger").get("url"),
            api_key=payload.get("swagger").get("api_key"),
            log=log,
        )
        pet_service_instance = PetService(swagger_instance)
        swagger_instance = User(
            base_url=payload.get("swagger").get("url"),
            api_key=payload.get("swagger").get("api_key"),
            log=log,
        )
        user_service_instance = UserService(swagger_instance)
    return (
        pet_service_instance,
        user_service_instance,
    )


def test_cases_parser(case):
    # TODO optimize
    methods = {}
    for method in case:
        for service in service_key_mappings:
            if method in service_key_mappings[service]:
                methods.update({f"{method}": f"{service}_instance.{method}"})
                break
    return methods


def test_e2e(
    payload: dict,
    test_cases: list,
    unique_id: str,
) -> str:
    # TODO get data from test cases and pass it respective functions
    """
    Running test-cases
    :param payload: Swagger Payload
    :param test_cases: The test cases to be executed
    :param unique_id: The logger execution id
    """
    if "swagger" in list(payload.keys()):
        (pet_service_instance, user_service_instance,) = setup_swagger(
            payload,
            unique_id,
        )

    final_result = ""
    for each_case in test_cases:
        all_methods = []
        passed = 0
        case = each_case["case"]
        method_mappings = test_cases_parser(case)
        for method in case:
            for parameters in case[method]:
                if type(parameters) == dict:
                    name = parameters.get("name", "test")
                else:
                    name = method
                try:
                    case_result = eval(method_mappings[method] + f"({parameters})")
                except Exception as e:
                    case_result = {
                        method: "Exception caught in automation framework, Reason: "
                        + str(e)
                    }
                    logger.error(case_result[method])
                if (
                    case_result.get(
                        method, "Something went wrong with automation framework"
                    )
                    != "Test Case Passed"
                ):
                    passed = 1
                    all_methods.append(
                        {
                            str(name): str(method)
                            + ";        Reason:     "
                            + str(
                                case_result.get(
                                    method, "Something went wrong with IT framework"
                                )
                            )
                        }
                    )
                else:
                    all_methods.append({str(name): str(method) + ", Test case passed"})
        if passed == 0:
            status = "Passed"
        else:
            status = "Failed"
        final_result = (
            final_result
            + str(each_case.get("unique_id"))
            + "           "
            + str(each_case.get("description"))
            + "           "
            + status
            + "\n"
        )
        for i in range(len(all_methods)):
            key_list = list(all_methods[i])
            key = key_list[0]
            final_result = (
                final_result
                + str(key)
                + "           "
                + str(all_methods[i].get(key))
                + "\n"
            )
    return final_result

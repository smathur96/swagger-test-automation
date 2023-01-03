def get_final_verdict(test_report: str) -> str:
    """
    :param test_report: The test_report in the string format
    :return: The body in string format
    """
    msg = "Unique_id\t\t\tDescription\t\t\tStatus\t\t\t\n"
    for each_line in test_report.split("\n"):
        line_array = each_line.split("           ")
        if len(line_array) == 3:
            msg = (
                msg
                + str(line_array[0])
                + "\t\t\t"
                + str(line_array[1])
                + "\t\t\t"
                + str(line_array[2])
                + "\t\t\t"
            )
    return msg

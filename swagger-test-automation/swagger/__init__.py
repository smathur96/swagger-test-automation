import uuid
import pymysql
from fpdf import FPDF

from flask import (
    Flask,
    Response,
    json,
    jsonify,
    make_response,
    render_template,
    request,
)
from testData.tests import test_cases
from tests import e2e
from utils.logger import Logger
from utils.result_formatter import get_final_verdict

logger = Logger().get_logger()


def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.debug = True
    res = {}
    
    @app.route('/')
    def upload_form():
        return render_template('download.html')
    
    @app.route('/download/report/<id>')
    def return_report(id) -> Response:
        return res[id]
    
    def download_report(result, id=None) -> None:
        try:
            pdf = FPDF()
            pdf.add_page()
            
            page_width = pdf.w - 2 * pdf.l_margin
            
            pdf.set_font('Times', 'B', 14)
            pdf.cell(page_width, 0.0, 'Test Results', align='C')
            pdf.ln(10)
            
            pdf.set_font('Courier', '', 12)
            
            col_width = page_width / 6
            
            pdf.ln(1)
            
            th = pdf.font_size
            
            # for row in result:
            pdf.cell(col_width, th, result[0], border=1)
            pdf.cell(col_width, th, result[2], border=1)
            pdf.multi_cell(col_width, th, result[1], border=1)
            pdf.ln(th)
            
            pdf.ln(10)
            
            pdf.set_font('Times', '', 10)
            pdf.cell(page_width, 0.0, '- end of report -', align='C')
            res.update({id: Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf',
                                     headers={'Content-Disposition': 'attachment;filename=swagger_report.pdf'})})
        except Exception as e:
            print(e)
    
    @app.route("/swagger/run_tests", methods=["POST"])
    def run_tests() -> Response:
        """
        function to run test cases
        :return:
        """
        params = request.data
        params = json.loads(params)
        tags_list = params.get("tags_list")
        unique_id = str(uuid.uuid4())
        
        validate_testcases(test_cases)
        
        response = make_response(
            jsonify({"id": unique_id, "info": "You can check logs for any issues."}),
            200,
        )
        
        @response.call_on_close
        def background_task() -> None:
            """
            :return:
            """
            with app.app_context():
                test_report = response_call_on_close(params, unique_id, tags_list)
                result = get_final_verdict(test_report)
                logger.info(result)
                download_report(result, unique_id)
        
        return response
    
    return app


def validate_testcases(test_cases: list) -> None:
    """
    Function to validate test cases. will fail if any one of the condition fails
    :param test_cases: list of test cases
    :return:
    """
    for test_case in test_cases:
        assert (
                test_case.get("unique_id") is not None
        ), "Please provide a unique id for the testcase"
        assert (
                test_case.get("description") is not None
        ), "Please provide description for the testcase"
        assert (
                test_case.get("tag_list") is not None
        ), "Please provide a tag for the testcase"
        assert (
                test_case.get("case") is not None
        ), "Please provide a cases list for the testcase"
        assert (
                len(test_case.get("case")) > 0
        ), "Please provide at least 1 test case to run"


def response_call_on_close(payload: dict, unique_id: str, tags: list) -> str:
    """
    It will be called when swagger/run_tests will be completed
    :param payload: The Swagger payload
    :param unique_id: unique_id generated for API call
    :param tags: tag name in list format
    :return: tuple which has test_report and time_taken
    """
    test_cases_with_tag = []
    for tag_param in tags:
        test_case_data = test_cases
        for case in test_case_data:
            tag_list = case.get("tag_list")
            for tag_index in range(len(tag_list)):
                if tag_list[tag_index] == tag_param:
                    test_cases_with_tag.append(case)
    test_report = e2e.test_e2e(
        payload,
        test_cases_with_tag,
        unique_id,
    )
    
    data = {"id": unique_id} if unique_id is not None else {}
    data["status"] = "completed"
    data["data"] = test_report
    return test_report

from flask import Blueprint
from werkzeug.exceptions import BadRequest, NotFound
from flask import jsonify, make_response, request, Response
from database import Summary, Text
from summary import summarize


api_bp = Blueprint('api', __name__)


DATABASE_NAME = 'squirro-app.db'


@api_bp.route('/text/<text_id>', methods=['GET'])
def get_text(text_id: str) -> Response:
    text = Text()
    text.connect(DATABASE_NAME)
    content = text.get(where={'id': text_id})

    if content is None or len(content) == 0:
        raise NotFound(f'Not found text with id: {text_id}')

    response = make_response(
        jsonify({
            'text_id':  content[0][0],
            'text': content[0][1],
        }),
        200,
    )

    response.headers["Content-Type"] = "application/json"
    return response


@api_bp.route('/text', methods=['POST'])
def store_text() -> Response:
    header = request.headers.get('Content-Type')
    if header is None or "application/json" not in header:
        raise BadRequest('content type must be "application/json"')

    content = request.json.get('text')

    if content is None:
        raise BadRequest('Request data missing {text}')

    if content is '':
        raise BadRequest('Request data is empty')

    db_text = Text()
    db_text.connect(DATABASE_NAME)
    # TODO: compress text before storing
    text_id = db_text.put(values=[content])

    db_sum = Summary()
    db_sum.connect(DATABASE_NAME)
    # TODO: compress summary before storing
    sumamry = summarize(content)
    sum_id = db_sum.put(values=[str(text_id), sumamry])


    response = make_response(
        jsonify({
            'text_id': text_id,
        }),
        201,
    )

    response.headers["Content-Type"] = "application/json"
    return response


@api_bp.route('/summary/<text_id>')
def get_summary(text_id: str) -> Response:
    summary = Summary()
    summary.connect(DATABASE_NAME)
    content = summary.get(where = {'text_id': text_id})

    if content is None or len(content) == 0:
        raise NotFound(f'Not found Summary corelated with text with id {text_id}')

    response = make_response(
        jsonify({
            "id":  content[0][0],
            "text_id": content[0][1],
            "summary": content[0][2],
        }),
        200,
    )


    response.headers["Content-Type"] = "application/json"
    return response


def make_error_response(code: int, err: str) -> Response:
    response = make_response(
        jsonify({
            'message': err,
        }),
        code,
    )
    response.headers["Content-Type"] = "application/json"
    return response


@api_bp.errorhandler(NotFound)
def handle_not_found_request(e) -> Response:
    return make_error_response(404, str(e))


@api_bp.errorhandler(BadRequest)
def handle_bad_request(e) -> Response:
    return make_error_response(400, str(e))

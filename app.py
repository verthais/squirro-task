import uuid
from flask import Flask, jsonify, make_response, request
from tests.test_database import DATABASE_NAME
from werkzeug.exceptions import BadRequest, NotFound

from database import Summary, Text


DATABASE_NAME = 'squirro-app.db'


def create_app(name: str) -> Flask:
    # TODO: init db if non existing
    return Flask(name)


app = create_app('squirro-app')


@app.route('/text/<text_id>', methods=['GET'])
def get_text(text_id: str):
    text = Text()
    text.connect('squirro.db')
    content = text.get(where={'id': text_id})

    if content is None:
        raise NotFound(f'Not found text with id: {text_id}')

    response = make_response(
        jsonify({
            'text': content[0][1],
        }),
        200,
    )

    response.headers["Content-Type"] = "application/json"
    return response


@app.route('/text', methods=['POST'])
def store_text():
    header = request.headers.get('Content-Type')
    if header is None or "application/json" not in header:
        raise BadRequest('content type must be "application/json"')

    content = request.json.get('text')

    if content is None:
        raise BadRequest('Request data missing {text}')

    db_text = Text()
    db_text.connect(DATABASE_NAME)
    # TODO: compress text before storing
    text_id = db_text.put(values=[content])

    db_sum = Summary()
    db_sum.connect(DATABASE_NAME)
    # TODO: compress summary before storing
    # TODO: generate summary
    sumamry = ''
    sum_id = db_sum.put(values=[text_id, sumamry])


    response = make_response(
        jsonify({
            'text_id': text_id,
        }),
        201,
    )

    response.headers["Content-Type"] = "application/json"
    return response


@app.route('/summary/<text_id>')
def get_summary(text_id: str):
    summary = Summary()
    summary.connect('squirro.db')
    content = summary.get(where = {'text_id': text_id})

    if content is None:
        raise NotFound(f'Not found Summary corelated with text with id {text_id}')

    response = make_response(
        jsonify({
            "document_id": "example_id",
            "summary": f"This is the summary of text {text_id}",
        }),
        200,
    )


    response.headers["Content-Type"] = "application/json"
    return response


def make_error_response(code: int, err: str):
    response = make_response(
        jsonify({
            'message': err,
        }),
        code,
    )
    response.headers["Content-Type"] = "application/json"
    return response


@app.errorhandler(NotFound)
def handle_not_found_request(e):
    return make_error_response(404, str(e))


@app.errorhandler(BadRequest)
def handle_bad_request(e):
    return make_error_response(400, str(e))


def main():
    app.run(port=50000)


if __name__ == '__main__':
    main()
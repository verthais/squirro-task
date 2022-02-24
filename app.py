import uuid
from flask import Flask, jsonify, make_response, request
from werkzeug.exceptions import BadRequest, NotFound

from database import Summary, Text, Schema

def create_app(name: str) -> Flask:
    return Flask(name)

app = create_app('squirro-app')


@app.route('/text/<text_id>', methods=['GET'])
def get_text(text_id: str):
    text = Text()
    content = text.get({'where':{'id': text_id}})

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
    print(header)
    if header is None or "application/json" not in header:
        raise BadRequest('content type must be "application/json"')

    text_id = uuid.uuid4()

    response = make_response(
        jsonify({
            'text_id': text_id,
        }),
        201,
    )

    # TODO: store the text in <??>
    # TODO: store the summarty in <??>

    response.headers["Content-Type"] = "application/json"
    return response


@app.route('/summary/<text_id>')
def get_summary(text_id: str):
    summary = Summary()
    content = summary.get({'where': {'text_id': text_id}})

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
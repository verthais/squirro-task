import uuid
from flask import Flask, jsonify, make_response, request
from werkzeug.exceptions import BadRequest


def create_app(name: str) -> Flask:
    return Flask(name)

app = create_app('squirro-app')


@app.route('/text/<text_id>', methods=['GET'])
def get_text(text_id: str):
    response = make_response(
        jsonify({
            'text': f'text with id {text_id}',
        }),
        200,
    )

    # TODO: retrieve the text from <??>

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
    response = make_response(
        jsonify({
            "document_id": "example_id",
            "summary": f"This is the summary of text {text_id}",
        }),
        200,
    )

    # TODO: retrieve the corresponding summary from <??>

    response.headers["Content-Type"] = "application/json"
    return response


@app.errorhandler(BadRequest)
def handle_bad_request(e):
    response = make_response(
        jsonify({
            'message': str(e),
        }),
        400,
    )
    response.headers["Content-Type"] = "application/json"
    return response


def main():
    app.run(port=50000)


if __name__ == '__main__':
    main()
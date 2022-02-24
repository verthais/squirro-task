from flask import Flask

def create_app(name: str) -> Flask:
    return Flask(name)

app = create_app('squirro-app')

@app.route('/')
def hello_world():
    return 'Hello world!'


def main():
    app.run(port=50000)


if __name__ == '__main__':
    main()
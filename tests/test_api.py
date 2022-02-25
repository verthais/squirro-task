import pytest
from uuid import uuid4
from app import create_app

@pytest.fixture()
def app():
    app = create_app("test-squirro-app")
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture()
def gen_id():
    return str(uuid4())

def test_edit_user(client):
    content = (
        "The Florida House of Representatives on Thursday approved legislation that would ban certain discussions of gender identity and sexual orientation in schools."
        "I believe in the idea that creating boundaries at an early age of what is appropriate in our schools — when we are funding our schools — is not hate,” the bill’s sponsor, state Rep. Joe Harding (R), said during the vote."
        "It's actually providing boundaries, and it's fair to our teachers and our school districts to know what we expect."
        "But those against Harding’s bill called it a hateful and needless attack on the state’s young LGBTQ+ population, which already faces greater risk of mental illness, self-harm and suicide."
        "Despite overwhelming public outrage, polling data underscoring immense unpopularity with voters, and hours of testimony from LGBTQ families, Republican legislators voted to pass the ‘Don’t Say Gay’ bill and ‘Stop WOKE’ Act in the Florida House. If signed into law, these bills will have disastrous impacts on classrooms and workplaces,” the LGBTQ+ advocacy group Equality Florida said in a statement immediately following the vote. “They will turn Florida into a surveillance state and give the government broad license to censor conversations about American history, the origins of racism and injustice, and the existence of LGBTQ people."
    )
    response = client.post(
        "/text",
        json={
            "text": (content),
        }
    )
    assert response.status_code == 201

    text_id = response.json.get('text_id')

    get_text_response = client.get(
        f'/text/{text_id}'
    )

    assert get_text_response.status_code == 200

    get_sum_response = client.get(
        f'/summary/{text_id}'
    )

    assert get_sum_response.status_code == 200


def test_negative_text(client, gen_id):
    response = client.post(
        '/text'
    )

    assert response.status_code == 400

    text_id = gen_id

    response = client.get(
        f'/text/{text_id}'
    )

    assert response.status_code == 404

def test_negative_summary(client, gen_id):
    text_id = gen_id

    response = client.get(
        f'/summary/{text_id}'
    )

    assert response.status_code == 404

from database import Text, Summary, migrate


DATABASE_NAME = 'test.db'


def setup_module(_):
    import os
    cwd = os.getcwd()
    db_file = f'{cwd}/{DATABASE_NAME}'
    if os.path.exists(db_file):
        os.remove(db_file)

    migrate(DATABASE_NAME)


def test_text_query():
    text = Text()
    text.connect(DATABASE_NAME)
    query = text.get(
        dry_run = True,
        where = {'id': '12345'},
    )

    assert 'SELECT id,content FROM texts WHERE id = "12345"' == query


def test_summary_query():
    summary = Summary()
    summary.connect(DATABASE_NAME)
    query = summary.get(
        dry_run = True,
        where = {'id': '12345'},
    )

    assert 'SELECT id,text_id,summary FROM summaries WHERE id = "12345"' == query


def test_text_put():
    text = Text()
    text.connect(DATABASE_NAME)
    query = text.put(
        dry_run = True,
        values = ['orginal text to store'],
    )

    assert 'INSERT INTO texts VALUES ("' in query
    assert '","orginal text to store")' in query


def test_summary_put():
    summary = Summary()
    summary.connect(DATABASE_NAME)
    query = summary.put(
        dry_run = True,
        values = ['text_id','summary text to store'],
    )

    assert 'INSERT INTO summaries VALUES ("' in query
    assert '","text_id","summary text to store")' in query


def test_db_integration():
    text = Text()
    text.connect(DATABASE_NAME)

    text_text = 'orginal text to store'
    text_id = text.put(values=[text_text])

    summary = Summary()
    summary.connect(DATABASE_NAME)
    summary_text = [f'{text_id}','summary text']
    summary_id = summary.put(values=summary_text)

    ret_text = text.get(where={'id': text_id})[0]

    assert ret_text[0] == str(text_id)
    assert ret_text[1] == text_text

    ret_summary = summary.get(where={'id': summary_id})[0]

    assert ret_summary[0] == str(summary_id)
    assert ret_summary[1] == str(text_id)
    assert ret_summary[2] == summary_text[1]

    sum_for_txt = summary.get(where={'text_id': text_id})[0]

    assert sum_for_txt[0] == str(summary_id)
    assert sum_for_txt[1] == str(text_id)
    assert sum_for_txt[2] == summary_text[1]
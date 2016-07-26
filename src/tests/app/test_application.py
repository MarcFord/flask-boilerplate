def test_application_env(app):
    assert app.env == 'testing', 'Application is not in testing env'

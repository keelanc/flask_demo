from src_api.demo import api, run_command


class TestAPI:
    """Test the API"""
    def setup_class(self):
        """Setup class"""
        self._client = api.test_client()

    def test_index(self):
        """Test index"""
        resp = self._client.get('/')
        assert resp.status_code == 200
        assert b'See API documentation: TBD' in resp.data

    def test_post(self):
        """Should get a 405 METHOD NOT ALLOWED error when using POST"""
        resp = self._client.post('/command', headers={'Content-Type': 'application/json'}, json={})
        assert resp.status_code == 405

    def test_no_command_key(self):
        """Should get a 400 BAD REQUEST error if no command key is in the request body"""
        resp = self._client.put('/command', headers={'Content-Type': 'application/json'}, json={})
        assert resp.status_code == 400

    def test_command_simple(self):
        """Test a simple echo command"""
        resp = self._client.put('/command', headers={'Content-Type': 'application/json'},
                                json={"command": "echo foo"})
        assert resp.status_code == 200
        assert b'"status":0' in resp.data
        assert b'"stdout":"foo\\n"' in resp.data
        assert b'"stderr":""' in resp.data

    def test_command_pipe(self):
        """Test the run_command function. Ensure it handles piping."""
        # count number of new lines in requirements.txt
        status, out, err = run_command("cat $(ls | grep req) | wc -l")
        assert status == 0
        assert out == "2\n"
        assert err == ""

    def test_command_error(self):
        """Should return 'status': -1 if the command is received but cannot be executed"""
        resp = self._client.put('/command', headers={'Content-Type': 'application/json'},
                                json={"command": "fakecommand"})
        assert resp.status_code == 200
        assert b'"status":-1' in resp.data
        assert b'"stdout":""' in resp.data
        assert b'"stderr":"/bin/sh: fakecommand: not found\\n"' in resp.data

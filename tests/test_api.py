from unittest import mock
from unittest.mock import Mock
from api import lambda_handler, queue


def test_lambda_handler_success(mocker):
    mocker.patch.object(queue, "send_message")
    event = {
        "body": '{"update_id": 813352806,"message": {"message_id": 186,"from": {"id": 182552976,"is_bot": false,"first_name": "Test","last_name": "Test","language_code": "uk"},"chat": {"id": 182552976,"first_name": "Test","last_name": "Test","type": "private"},"date": 1708367401,"text": "/hello"}}'
    }
    context = Mock()
    response = lambda_handler(event, context)
    assert response["statusCode"] == 200
    assert response["body"] == "Success"


def test_lambda_handler_failure(mocker):
    event = {"body": "test"}
    context = Mock()
    with mock.patch("api.queue.send_message") as mock_send_message:
        mock_send_message.side_effect = Exception("Test exception")
        response = lambda_handler(event, context)
    assert response["statusCode"] == 500
    assert response["body"] == "Failure"

import unittest
import os
import sys
if os.name == 'nt':
    pddl_path = "C:\\Users\\giulio17\\Documents\\Camelot_work\\EV_PDDL"
else:
    pddl_path = "/Users/giuliomori/Documents/GitHub/EV_PDDL/"

sys.path.insert(0, pddl_path)
from unittest.mock import patch
import responses

class TestPlatformCommunication(unittest.TestCase):

    def setUp(self):
        self.protocol_messages = {
            "PHASE_1" : 
            {
                "message_1" : "start of communication. name:",
                "message_2" : "inizialization completed. wait preparation environment."
            },
            "PHASE_2" : 
            {
                "message_3" : "start of communication. name:",
                "message_4" : "inizialization completed. Request for initial state of environment."
            },
            "PHASE_3" : 
            {
                "message_5" : "request domain and problem",
                "message_6" : "domain and problem",
                "message_7" : "domain and problem"
            },
            "PHASE_4" : 
            {
                "message_8" : "received domain and problem. request links for communication",
                "message_9" : "receved. start communication on links",
                "message_10" : "links"
            }
        }

    @responses.activate
    def test_send_message(self):
        message = {'message': 'message'}
        responses.add(responses.GET, 'http://127.0.0.1:8080/get_protocol_messages', json=self.protocol_messages)
        responses.add(responses.POST, 'http://127.0.0.1:8080/inizialization_em', json=message, status=200)
        from camelot_communicator.platform_IO_communication import PlatformIOCommunication
        with patch.object(PlatformIOCommunication.__wrapped__ , '_is_platform_online') as mock_is_platform_online:
            mock_is_platform_online.return_value = True
            platform_communication = PlatformIOCommunication()
            reply = platform_communication.send_message("test", inizialization=True)
        self.assertEqual(reply, message)
        self.assertEqual(len(responses.calls) , 2 )
        self.assertEqual(responses.calls[1].request.url , 'http://127.0.0.1:8080/inizialization_em')
        self.assertEqual(responses.calls[1].request.body , b'{"text": "test"}')
        self.assertEqual(responses.calls[1].response.text , '{"message": "message"}' )
    
    @responses.activate
    def test_phase1(self):
        message = {'message': 'message'}
        responses.add(responses.GET, 'http://127.0.0.1:8080/get_protocol_messages', json=self.protocol_messages)
        responses.add(responses.POST, 'http://127.0.0.1:8080/inizialization_em', json=self.protocol_messages['PHASE_2']['message_4'], status=200)
        from camelot_communicator.game_controller import GameController
        from camelot_communicator.platform_IO_communication import PlatformIOCommunication
        with patch.object(PlatformIOCommunication.__wrapped__ , '_is_platform_online') as mock_is_platform_online:
            with patch('camelot_communicator.camelot_input_multiplexer.CamelotInputMultiplexer.__wrapped__', autospec=True) as mock_camelot_communication:
                mock_camelot_communication.start = True
                mock_is_platform_online.return_value = True
                gc = GameController(GUI=False)
                result = gc.start_platform_communication()
        self.assertEqual(len(responses.calls) , 2 )
        self.assertEqual(responses.calls[1].request.url , 'http://127.0.0.1:8080/inizialization_em')
        self.assertEqual(responses.calls[1].request.body , b'{"text": "start of communication. name:Camelot"}')
        self.assertTrue(result)
    
    @responses.activate
    def test_phase3_4(self):
        message = {'message': 'message'}
        responses.add(responses.GET, 'http://127.0.0.1:8080/get_protocol_messages', json=self.protocol_messages)
        response_message = {
            'text' : self.protocol_messages['PHASE_4']['message_9'],
            'add_message_url' : 'url',
            'get_message_url' : 'url'
        }
        responses.add(responses.POST, 'http://127.0.0.1:8080/inizialization_em', json=response_message, status=200)
        from camelot_communicator.game_controller import GameController
        from camelot_communicator.platform_IO_communication import PlatformIOCommunication
        with patch.object(PlatformIOCommunication.__wrapped__ , '_is_platform_online') as mock_is_platform_online:
            with patch('camelot_communicator.camelot_input_multiplexer.CamelotInputMultiplexer.__wrapped__', autospec=True) as mock_camelot_communication:
                mock_camelot_communication.start = True
                mock_is_platform_online.return_value = True
                with patch('camelot_communicator.camelot_action.CamelotAction.__wrapped__', autospec=True) as mock_camelot_action:
                    mock_camelot_action.return_value.action.return_value = True
                    gc = GameController(GUI=False)
                    gc.start_game(game_loop=False)

        self.assertEqual(len(responses.calls) , 2 )
        self.assertEqual(responses.calls[1].request.url , 'http://127.0.0.1:8080/inizialization_em')



if __name__ == '__main__':
    unittest.main()
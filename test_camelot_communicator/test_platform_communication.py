import unittest
import os
import sys
if os.name == 'nt':
    pddl_path = "C:\\Users\\giulio17\\Documents\\Camelot_work\\EV_PDDL"
else:
    pddl_path = "/Users/giuliomori/Documents/GitHub/EV_PDDL/"

sys.path.insert(0, pddl_path)
from unittest.mock import patch
from camelot_communicator.platform_IO_communication import PlatformIOCommunication
from camelot_communicator.game_controller import GameController
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
    @patch.object(PlatformIOCommunication.__wrapped__, '_is_platform_online')
    def test_send_message(self, mock_is_platform_online):
        message = {'message': 'message'}
        responses.add(responses.GET, 'http://127.0.0.1:8080/get_protocol_messages', json=self.protocol_messages)
        responses.add(responses.POST, 'http://127.0.0.1:8080/inizialization_em', json=message, status=200)
        mock_is_platform_online.return_value = True
        platform_communication = PlatformIOCommunication()
        reply = platform_communication.send_message("test", inizialization=True)
        self.assertEqual(reply, message)
    
    @responses.activate
    @patch.object(PlatformIOCommunication.__wrapped__, '_is_platform_online')
    def test_phase1(self, mock_is_platform_online):
        message = {'message': 'message'}
        responses.add(responses.GET, 'http://127.0.0.1:8080/get_protocol_messages', json=self.protocol_messages)
        responses.add(responses.POST, 'http://127.0.0.1:8080/inizialization_em', json=message, status=200)
        mock_is_platform_online.return_value = True
        gc = GameController(GUI=False)


if __name__ == '__main__':
    unittest.main()
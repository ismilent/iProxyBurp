# coding:utf-8

from frida_tools import tracer

import json
import requests

BURP_HOST = 'localhost'
BURP_PORT = 26080


def frida_process_message(self, message, data, ui):
    handled = False

    if message['type'] == 'input':
        handled = True

    elif message['type'] == 'send':
        stanza = message['payload']

        if stanza['from'] == '/request':
            req_data = stanza['payload'].encode('utf-8')

            orig_json_data = json.loads(req_data)

            orig_request_url = orig_json_data.pop(u'orig_request_url')

            req = requests.request('FRIDA', 'http://%s:%d/' % (BURP_HOST, BURP_PORT),
                                   headers={'content-type':'text/plain', 'ORIG_REQUEST_URI': orig_request_url},
                                   data=json.dumps(orig_json_data))
            self._script.post({'type':'input', 'payload': req.content})
            handled = True

        elif stanza['from'] == '/response':
            req_data = stanza['payload'].encode('utf-8')

            req = requests.request('RESPF', 'http://%s:%d/' % (BURP_HOST, BURP_PORT),
                                   headers={'content-type': 'text/plain'},
                                   data=json.dumps(req_data))
            self._script.post({'type': 'output', 'payload': req.content})
            handled = True

    if not handled:
        self.__process_message(message, data, ui)

tracer.Tracer.__process_message = tracer.Tracer._process_message
tracer.Tracer._process_message = frida_process_message

if __name__ == '__main__':
    tracer.main()
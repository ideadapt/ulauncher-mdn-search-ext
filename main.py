import json
import urllib.request
import urllib.parse
import logging
from time import sleep
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction

logger = logging.getLogger(__name__)
key = 'AIzaSyCr6xs0NlPg2hIynXQJWY3o230n6iQyDl0'
cx = '017146964052550031681:wnjobi1fzcm'

# debug via /usr/bin/ulauncher -v | grep -A 5 "mdn"
class MdnSearchExtension(Extension):

    def __init__(self):
        super(MdnSearchExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):

    # inspired by https://github.com/ChaitanyaPramod/mdn-search/blob/master/mdn_search.js
    # actually reusing his google custom search project
    # example request https://www.googleapis.com/customsearch/v1?key=AIzaSyCr6xs0NlPg2hIynXQJWY3o230n6iQyDl0&cx=017146964052550031681:wnjobi1fzcm&q=flex-direction
    def on_event(self, event, extension):
        logger.info('preferences %s', json.dumps(extension.preferences))
        query = event.get_argument()
        url = 'https://www.googleapis.com/customsearch/v1?key={0}&cx={1}&q={2}'.format(key, cx, query)
        url_stream = urllib.request.urlopen(url)
        response = url_stream.read().decode('utf-8')
        json_string = json.loads(response)
        items = []
        items.append(ExtensionResultItem(icon='images/icon.png',
                                        name=json_string['items'][0]['title'],
                                        description=json_string['items'][0]['snippet'],
                                        on_enter=OpenUrlAction(json_string['items'][0]['formattedUrl'])))

        return RenderResultListAction(items)


if __name__ == '__main__':
    MdnSearchExtension().run()

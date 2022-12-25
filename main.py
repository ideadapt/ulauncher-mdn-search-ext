import json
import urllib.request
import urllib.parse
import logging

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
        if query.strip() == '':
            return []
        url = 'https://www.googleapis.com/customsearch/v1?key={0}&cx={1}&q={2}'.format(key, cx, urllib.parse.quote(query))
        logger.debug('search mdn via google at %s', url)
        url_stream = urllib.request.urlopen(url)
        response = url_stream.read().decode('utf-8')
        json_string = json.loads(response)
        items = []
        json_items = json_string['items']
        for item in json_items:
            items.append(ExtensionResultItem(
                icon='images/mdn.png',
                name=item['title'],
                description=item['snippet'],
                # could filter by og:locale
                on_enter=OpenUrlAction(item['pagemap']['metatags'][0]['og:url'])))

        return RenderResultListAction(items)


if __name__ == '__main__':
    MdnSearchExtension().run()

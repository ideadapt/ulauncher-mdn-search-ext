import json
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
        url = 'https://www.googleapis.com/customsearch/v1?key=AIzaSyCr6xs0NlPg2hIynXQJWY3o230n6iQyDl0&cx=017146964052550031681:wnjobi1fzcm&q=flex-direction'
        f = urllib.request.urlopen(url)
        s = f.read().decode('utf-8')
        j = json.loads(s)
        logger.info(j)
        items = []
        logger.info('preferences %s' % json.dumps(extension.preferences))
        items.append(ExtensionResultItem(icon='images/icon.png',
                                        name='MDN Entry 1',
                                        description='Description of Entry 1',
                                        on_enter=OpenUrlAction('https://www.blick.ch')))

        return RenderResultListAction(items)


if __name__ == '__main__':
    MdnSearchExtension().run()

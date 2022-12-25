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

logger = logging.getLogger(__name__)


class MdnSearchExtension(Extension):

    def __init__(self):
        super(MdnSearchExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        #self.subscribe(ItemEnterEvent, ItemEnterEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        items = []
        logger.info('preferences %s' % json.dumps(extension.preferences))
        # TODO send request to https://www.googleapis.com/customsearch/v1?key=AIzaSyCr6xs0NlPg2hIynXQJWY3o230n6iQyDl0&cx=017146964052550031681:wnjobi1fzcm&q=flex-direction
        items.append(ExtensionResultItem(icon='images/icon.png',
                                        name='MDN Entry 1',
                                        description='Description of Entry 1',
                                        on_enter=OpenUrlAction('https://www.blick.ch')))

        return RenderResultListAction(items)


class ItemEnterEventListener(EventListener):

    def on_event(self, event, extension):
        data = event.get_data()
        # TODO open website from event data
        return RenderResultListAction([ExtensionResultItem(icon='images/icon.png',
                                                           name=data['new_name'],
                                                           on_enter=OpenUrlAction('https://www.blick.ch'))])


if __name__ == '__main__':
    MdnSearchExtension().run()

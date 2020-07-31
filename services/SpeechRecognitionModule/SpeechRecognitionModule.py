import speech_recognition as sr

from common import ScModule
from keynodes import Keynodes

from sc import *


def recognise_file(file, lang='de'):
    if lang == 'de':
        lang = 'de-DE'
    elif lang == 'en':
        lang = 'en-EN'
    elif lang == 'ru':
        lang = 'ru-RU'

    r = sr.Recognizer()

    with sr.AudioFile(file) as source:
        audio_text = r.listen(source)
        try:
            text = r.recognize_google(audio_text, language=lang)
            print('Converting audio transcripts into text ...')
            print(text)
            return text
        except:
            print('Sorry.. run again...')


def recognise_mic(lang='de'):
    if lang == 'de':
        lang = 'de-DE'
    elif lang == 'en':
        lang = 'en-EN'
    elif lang == 'ru':
        lang = 'ru-RU'

    r = sr.Recognizer()

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Talk")
        audio_text = r.listen(source)
        print("Time over, thanks")

        try:
            text = r.recognize_google(audio_text, language=lang)
            print("Text: "+text)
            return text
        except:
            print("Sorry, I did not get that")


def gen_template(ctx, text):
    if text is not None:
        nrel_sc_text_translation_addr = ctx.HelperResolveSystemIdtf(
            'nrel_sc_text_translation', ScType.NodeConstNoRole)
        concept_message_addr = ctx.HelperResolveSystemIdtf(
            'concept_message', ScType.NodeConstClass)
        nrel_authors_addr = ctx.HelperResolveSystemIdtf(
            'nrel_authors', ScType.NodeConstNoRole)

        templ = ScTemplate()
        templ.TripleWithRelation(
            ScType.NodeVar >> '_message_name',
            ScType.EdgeDCommonVar,
            ScType.NodeVar >> '_message_author',
            ScType.EdgeAccessVarPosPerm,
            nrel_authors_addr
        )
        templ.TripleWithRelation(
            ScType.NodeVar >> '_temp',
            ScType.EdgeDCommonVar,
            '_message_name',
            ScType.EdgeAccessVarPosPerm,
            nrel_sc_text_translation_addr
        )
        templ.Triple(
            '_temp',
            ScType.EdgeAccessVarPosPerm,
            ScType.LinkVar >> '_text'
        )
        templ.Triple(
            concept_message_addr,
            ScType.EdgeAccessVarPosPerm,
            '_message_name'
        )

        params = ScTemplateParams()

        new_message_node_addr = ctx.CreateNode(ScType.NodeConst)
        ctx.HelperSetSystemIdtf(
            'recognised_message', new_message_node_addr)
        params.Add('_message_name', new_message_node_addr)

        message_author_node_addr = ctx.CreateNode(ScType.NodeConst)
        ctx.HelperSetSystemIdtf(
            'speech_recognition_module', message_author_node_addr)
        params.Add('_message_author', message_author_node_addr)

        link_addr = ctx.CreateLink()
        ctx.SetLinkContent(link_addr, text)
        params.Add('_text', link_addr)

        result = ctx.HelperGenTemplate(templ, params)
    else:
        print("The message couldn't be recognized")


class SpeechRecognitionModule(ScModule):
    def __init__(self):
        ScModule.__init__(
            self,
            ctx=__ctx__,
            cpp_bridge=__cpp_bridge__,
            keynodes=[
            ],
        )

    def OnInitialize(self, params):
        print('Initialize Recogn Module')
        gen_template(self.ctx, recognise_mic(lang='ru'))

    def OnShutdown(self):
        print('Shutting down Recogn module')


module = SpeechRecognitionModule()
module.Run()

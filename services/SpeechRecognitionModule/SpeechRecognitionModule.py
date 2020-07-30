from speech2text import recognise_mic

from common import ScModule
from keynodes import Keynodes

from sc import *


def gen_template(ctx, text):
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

        text = recognise_mic(lang='ru')

        if text is not None:
            gen_template(self.ctx, text)
        else:
            print("The message couldn't be recognized")

    def OnShutdown(self):
        print('Shutting down Recogn module')

module = SpeechRecognitionModule()
module.Run()

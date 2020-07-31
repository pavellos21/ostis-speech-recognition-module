from SpeechRecognitionModule.SpeechRecognitionModule import gen_template, recognise_file
from os import path
from unittest import defaultTestLoader, TestLoader, TestCase, TextTestRunner

from common import *
from sc import *

AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "english.wav")


class TestSpeech2Text(TestCase):
    def test_audio_file(self):
        self.assertEqual(recognise_file(AUDIO_FILE, lang='en'), '123')


class TestTemplateGen(TestCase):
    def test_template_generation(self):
        ctx = TestTemplateGen.MemoryCtx()

        text = recognise_file(AUDIO_FILE, lang='en')

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
            ScType.NodeVar,
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
            ScType.LinkVar
        )
        templ.Triple(
            concept_message_addr,
            ScType.EdgeAccessVarPosPerm,
            '_message_name'
        )
        
        gen_template(ctx, None)
        self.assertEqual(ctx.HelperSearchTemplate(templ).Size(), 0)

        gen_template(ctx, text)
        self.assertNotEqual(ctx.HelperSearchTemplate(templ).Size(), 0)

        templ = ScTemplate()

        templ.TripleWithRelation(
            ScType.NodeVar >> '_temp',
            ScType.EdgeDCommonVar,
            ScType.NodeVar >> '_message',
            ScType.EdgeAccessVarPosPerm,
            nrel_sc_text_translation_addr
        )

        templ.Triple(
            '_temp',
            ScType.EdgeAccessVarPosPerm,
            ScType.LinkVar >> '_link'
        )

        templ.Triple(
            concept_message_addr,
            ScType.EdgeAccessVarPosPerm,
            '_message'
        )

        search_result = ctx.HelperSearchTemplate(templ)
        link_index = search_result.Aliases()['_link']
        search_item = search_result[0]

        self.assertEqual(ctx.GetLinkContent(search_item[link_index]).AsString(), text)


def MemoryCtx() -> ScMemoryContext:
    return __ctx__


def RunTests():
    global TestLoader, TextTestRunner

    tests = [
        TestSpeech2Text,
        TestTemplateGen,
    ]

    for testItem in tests:
        testItem.MemoryCtx = MemoryCtx
        suite = defaultTestLoader.loadTestsFromTestCase(testItem)
        res = TextTestRunner(verbosity=2).run(suite)
        if not res.wasSuccessful():
            raise Exception("Unit test failed")


class TestModule(ScModule):
    def __init__(self):
        ScModule.__init__(self,
                          ctx=__ctx__,
                          cpp_bridge=__cpp_bridge__,
                          keynodes=[
                          ])

    def DoTests(self):
        try:
            RunTests()
        except Exception as ex:
            raise ex
        except:
            print("Unexpected error")
        finally:
            module.Stop()

    def OnInitialize(self, params):
        self.DoTests()

    def OnShutdown(self):
        pass


module = TestModule()
module.Run()

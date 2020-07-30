/*
* This source file is part of an OSTIS project. For the latest info, see http://ostis.net
* Distributed under the MIT License
* (See accompanying file COPYING.MIT or copy at http://opensource.org/licenses/MIT)
*/

#include "SpeechRecognitionModule.hpp"

SC_IMPLEMENT_MODULE(SpeechRecognitionModule)

sc_result SpeechRecognitionModule::InitializeImpl()
{
  m_SpeechRecognitionService.reset(new SpeechRecognitionPythonService("SpeechRecognitionModule/SpeechRecognitionModule.py"));
  m_SpeechRecognitionService->Run();
  return SC_RESULT_OK;
}

sc_result SpeechRecognitionModule::ShutdownImpl()
{
  m_SpeechRecognitionService->Stop();
  m_SpeechRecognitionService.reset();
  return SC_RESULT_OK;
}

/*
* This source file is part of an OSTIS project. For the latest info, see http://ostis.net
* Distributed under the MIT License
* (See accompanying file COPYING.MIT or copy at http://opensource.org/licenses/MIT)
*/

#include "SRMTest.hpp"

SC_IMPLEMENT_MODULE(SRMTest)

sc_result SRMTest::InitializeImpl()
{
  m_SRMTestService.reset(new SRMTestPythonService("SpeechRecognitionModule/test/test.py"));
  m_SRMTestService->Run();
  return SC_RESULT_OK;
}

sc_result SRMTest::ShutdownImpl()
{
  m_SRMTestService->Stop();
  m_SRMTestService.reset();
  return SC_RESULT_OK;
}

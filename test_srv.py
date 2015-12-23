#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
from omniORB import CORBA, PortableServer, sslTP
import CosNaming, Example, Example__POA
class Echo_i (Example__POA.Echo):
    def echoString(self, mesg):
        print "echoString() called with message:", mesg
        return mesg


#os.environ['ORBtraceLevel'] = '25'

sslTP.certificate_authority_file("private-key.crt")
sslTP.key_file("private-key.key")
sslTP.key_file_password("test")


# ORBの生成と初期化
#sys.argv.extend(["-ORBtraceLevel", "25"])
sys.argv.extend(["-ORBInitRef", "NameService=corbaloc:iiop:1.0@localhost:2809/NameService"])
sys.argv.extend(["-ORBendPoint","giop:ssl::"])
sys.argv.extend(["-ORBsslVerifyMode","none"])
#sys.argv.extend(["-ORBendPoint","giop:tcp::"])
orb = CORBA.ORB_init(sys.argv, CORBA.ORB_ID)

poa = orb.resolve_initial_references("RootPOA")
ei = Echo_i()
eo = ei._this()
# RootPOA(ツリー構造のルート)への参照を取得
obj         = orb.resolve_initial_references("NameService")
#ルートコンテキストを取得
rootContext = obj._narrow(CosNaming.NamingContext)
if rootContext is None:
    print "Failed to narrow the root naming context"
    sys.exit(1)
name = [CosNaming.NameComponent("test", "my_context")]
try:
    #ネーミングコンテキストの作成
    testContext = rootContext.bind_new_context(name)
    print "New test context bound"
    
except CosNaming.NamingContext.AlreadyBound, ex:
    print "Test context already exists"
    obj = rootContext.resolve(name)
    testContext = obj._narrow(CosNaming.NamingContext)
    if testContext is None:
        print "test.mycontext exists but is not a NamingContext"
        sys.exit(1)
name = [CosNaming.NameComponent("ExampleEcho", "Object")]
try:
   #オブジェクトを登録
    testContext.bind(name, eo)
    print "New ExampleEcho object bound"
except CosNaming.NamingContext.AlreadyBound:
    testContext.rebind(name, eo)
    print "ExampleEcho binding already existed -- rebound"
#POAManagerオブジェクトの取得とアクティブ状態への遷移
poaManager = poa._get_the_POAManager()
poaManager.activate()
#eo.echoString("test")
#ORBの破棄
orb.run()
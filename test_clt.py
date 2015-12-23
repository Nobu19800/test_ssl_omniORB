#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
from omniORB import CORBA,sslTP
import CosNaming, Example

sslTP.certificate_authority_file("certs.crt")
sslTP.key_file("private-key.key")
sslTP.key_file_password("test")

#os.environ['ORBtraceLevel'] = '25'

# ORBの生成と初期化
#sys.argv.extend(["-ORBtraceLevel", "25"])
sys.argv.extend(["-ORBInitRef", "NameService=corbaloc:iiop:1.0@localhost:2809/NameService"])
sys.argv.extend(["-ORBendPoint","giop:ssl::"])
sys.argv.extend(["-ORBsslVerifyMode","none"])
#sys.argv.extend(["-ORBendPoint","giop:tcp::"])
orb = CORBA.ORB_init(sys.argv, CORBA.ORB_ID)

# RootPOA(ツリー構造のルート)への参照を取得
obj         = orb.resolve_initial_references("NameService")

#ルートコンテキストを取得
rootContext = obj._narrow(CosNaming.NamingContext)
if rootContext is None:
    print "Failed to narrow the root naming context"
    sys.exit(1)
name = [CosNaming.NameComponent("test", "my_context"),
        CosNaming.NameComponent("ExampleEcho", "Object")]
try:
   #指定した名前のオブジェクトリファレンスを取得
    obj = rootContext.resolve(name)
except CosNaming.NamingContext.NotFound, ex:
    print "Name not found"
    sys.exit(1)
#サーバントのオブジェクトリファレンス取得
eo = obj._narrow(Example.Echo)
if (eo is None):
    print "Object reference is not an Example::Echo"
    sys.exit(1)
message = "Hello from Python"
print eo
#サーバーに処理を要求
result  = eo.echoString(message)
print "I said '%s'. The object said '%s'." % (message,result)

raw_input()
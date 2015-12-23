rem C:\Python27\omniidl -bpython example_echo.idl
rem python example_echo_srv.py -ORBInitRef NameService=corbaloc:iiop:1.0@localhost:2809/NameService -ORBendPoint giop:ssl:: -ORBendPoint giop:tcp::
rem -ORBendPoint giop:tcp::
python test_srv.py
pause
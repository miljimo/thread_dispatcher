from threading import Event;
"""
  The dispatcher operation wrapper
  this class provided a way we can use to invoke the original function and
  return the result back.
"""
class DispatcherOperation(object):

    def __init__(self, method,*args, **kwargs):
        if(callable(method) != True):
            raise TypeError("@Method: expecting a callable object but {0} given".format(type(method)));
        if(kwargs != None):
            if ((type(kwargs) != list)  and
                (type(kwargs) != tuple) and
                (type(kwargs) !=dict)):
                raise TypeError("@Pareneter 2 : must be either variadic argument of list,tuple or dict");
        self.__method  = method;
        self.__kwargs    = kwargs;
        self.__args      = args;
        self.__Result    = None;
        self.__WaitEvent  =  None;

    
    def Wait(self):
        if(self.__WaitEvent == None):
            self.__WaitEvent =  Event();
            self.__WaitEvent.clear();
        self.__WaitEvent.wait();
        self.__WaitEvent  =  None;

    @property
    def Result(self):
        return self.__Result;
        

    def Invoke(self):
        try:
            if(callable(self.__method)):
               self.__Result  = self.__method(*self.__args, **self.__kwargs);
        except Exception as err:
            #Do some handling here.
            raise;
        finally:
            if(self.__WaitEvent != None):
                self.__WaitEvent.set();
       
        

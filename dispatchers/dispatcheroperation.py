
"""

"""
from datetime import datetime, timedelta;
from threading import Event;


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
        self.__EnqueueTime     = datetime.now();
        self.__WaitTime        =  None;
        self.__ElapseTime      =  None;

    @property
    def EnqueueTime(self):
        return self.__EnqueueTime;

    @EnqueueTime.setter
    def EnqueueTime(self, dtime: datetime):
        if(isinstance(dtime , datetime) is not True):
            raise TypeError("@EnqueueTime: expecting a datetime");
        self.__EnqueueTime  =  dtime;
    
    
    @property
    def WaitTime(self):
        return self.__WaitTime;

    @WaitTime.setter
    def WaitTime(self, value: timedelta):
        if(isinstance(value, timedelta) is not True):
            raise TypeError("@WaitTime : expecting a dateime  but {0} given".format(type(value)));
        self.__WaitTime  =  value;


    @property
    def ElapseTime(self):
        return self.__ElapseTime;

    @ElapseTime.setter
    def ElapseTime(self, value: timedelta):
        if(isinstance(value, timedelta) is not True):
            raise TypeError("@ElapseTime : Expecting a timedelta but {0} was given".format(type(value)));
        self.__ElapseTime  =  value;  
  
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
           pass;
       
        

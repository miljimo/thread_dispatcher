
import threading;
import time;
from datetime import datetime;
from dispatchers.dispatcheroperation import DispatcherOperation
from dispatchers.dispatcherqueue     import DispatcherQueue;        


class Dispatcher:

    __dispatchers  = list();
    @staticmethod
    def CreateInstance():
        thread   = threading.current_thread();
        result   =  None;
        for dispatcher in Dispatcher.__dispatchers:
            if(dispatcher.Thread  == thread):
                result  =  dispatcher;
                break;
        if(result is None):
            result  =  Dispatcher.__Dispatcher();
            Dispatcher.__dispatchers.append(result);
        return result;
        
        @staticmethod
        def Count():
            return len(Dispatcher.__dispatchers);

    def __init__(self):
        raise NotImplementedError("@Dispatcher does not have a constructor");


    """
    """
     
    class __Dispatcher(object):
        

        def __init__(self):
            self.__currentThread     =   threading.current_thread();
            self.__DispatcherQueue   =   DispatcherQueue();
            self.__Freezed  = False;
           
        def Invoke(self, method, *args , **kwargs):
            operation = None;
            #when the reaches 5millions it automatically start to get crashed prevent it.
            if(self.Count >= 100000):
                self.__Freezed = True;
                pass;
            else:
                if(self.__Freezed is not True):
                    operation  =  DispatcherOperation(method,*args, **kwargs)
                    operation.EnqueueTime = datetime.now();
                    self.__DispatcherQueue.Enqueue(operation);
                else:
                    if(self.Count <= 0):
                        self.__Freezed  = False;
            return operation;
        
        @property
        def Count(self):
            return self.__DispatcherQueue.Count;
             
        def Run(self):
            operation = None;
            if(self.CheckAccess() != True):
                raise ValueError("@Run Method : must be called on the same thread that create the dispatcher instance");
           
            try:
                if(self.__DispatcherQueue.IsEmpty is not True):
                    operation  =  self.__DispatcherQueue.Dequeue();
                    
                    if(operation != None):
                        #Calculate the wait time
                        currentTime         = datetime.now();
                        operation.WaitTime  =  currentTime  -  operation.EnqueueTime;
                        operation.Invoke();
                        #calculate the elapseTime;
                        operation.ElapseTime  = datetime.now() - currentTime ;
                    else:
                        # Idle dothing here.
                        # Dont know how to tell the system to suspend the thread until there
                        # is a value in the queue yet.
                        pass;
            except Exception as err:
                raise err;
          
            return operation;

        def CheckAccess(self):
            return (threading.current_thread().ident == self.Thread.ident);

        @property
        def Thread(self):
            return self.__currentThread;

    
       

if(__name__ =="__main__"):
    dispatcher   =  Dispatcher.CreateInstance();
    

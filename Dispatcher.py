
import threading;
import time;
from DispatcherOperation import DispatcherOperation
from DispatcherQueue     import DispatcherQueue;        


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
     
    class __Dispatcher(object):

        

        def __init__(self):
            self.__currentThread     =   threading.current_thread();
            self.__DispatcherQueue   =   DispatcherQueue();
            self.__IsRunning         =   False;

        def Invoke(self, method, *args , **kwargs):
            operation  =  DispatcherOperation(method,*args, **kwargs)
            self.__DispatcherQueue.Enqueue(operation);
            return operation;
             
        def Run(self):
            if(self.CheckAccess() != True):
                raise ValueError("@Run Method : must be called on the same thread that create the dispatcher instance");
           
            if(self.__IsRunning == True):
                return;
            self.__IsRunning = True;
            try:
                while(self.__IsRunning is True):
                    if(self.__DispatcherQueue.IsEmpty is not True):
                        operation  =  self.__DispatcherQueue.Dequeue();
                        if(operation != None):
                            operation.Invoke();
                    else:
                        time.sleep(1);
            except:
                raise ;
            finally:
                self.__IsRunning = False;

        def CheckAccess(self):
            return (threading.current_thread().ident == self.Thread.ident);

        @property
        def Thread(self):
            return self.__currentThread;

    
       

if(__name__ =="__main__"):
    def Task1():
        print("Task Running");

    def Task2(a , b):
        result  = (a + b);
        print("Thread Id = {0} , result ={1} \n".format(threading.current_thread().ident, result ));
        return result;


    def ExternalRun(dispatcher):
        a  = 1
        while(True):
            print("Invoked {0}".format(threading.current_thread().ident));
            dispatcher.Invoke(Task2, a ,  10);
            a =  a + 1;

          
    dispatcher  =  Dispatcher.CreateInstance();
 
    dispatcher.Invoke(Task1);
    dispatcher.Invoke(Task2, 5, 6);
    print(dispatcher.Thread);
    for i in range(1, 20):
        t  =  threading.Thread(target=ExternalRun, args=(dispatcher,));
        t.daemon = True;
        t.start();
    dispatcher.Run();
    


import threading;
import time;
from DispatcherOperation import DispatcherOperation
from DispatcherQueue    import DispatcherQueue;        


        
class Dispatcher(object):

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
        return (threading.current_thread() == self.Thread);

    @property
    def Thread(self):
        return self.__currentThread;


class DispatcherObject(object):


    def __init__(self):
        self.__Dispatcher   = None;

    @property
    def Dispatcher(self):
        return self.__Dispatcher;

    def CheckAccess(self):
        status  =  False;
        if(self.Dispatcher != None):
            status  =  sellf.Dispatcher.CheckAccess();
        return status;
    
       

if(__name__ =="__main__"):
    def Task1():
        print("Task Running");

    def Task2(a , b):
        result  = (a + b);
        print("Task 2 Thread Id = {0} \n".format(threading.current_thread().name));
        return result;


    def ExternalRun(dispatcher):
        a  = 1
        while(True):
            print("Thread Id = {0} \n".format(threading.current_thread().name));
            operation =  dispatcher.Invoke(Task2, a ,  6);
            #operation.Wait();
            print("Result for wait  =  {0}".format(operation.Result));
            
            a =  a + 1;

          
    dispatcher  =  Dispatcher();
    dispatcher.Invoke(Task1);
    dispatcher.Invoke(Task2, 5, 6);
    print(dispatcher.Thread);
    t  =  threading.Thread(target=ExternalRun, args=(dispatcher,));
    t.daemon = True;
    t.start();
    dispatcher.Run();
    

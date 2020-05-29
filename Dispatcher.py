
import threading;
import time;
        
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

    def Invoke(self):
        try:
            if(callable(self.__method)):
                self.__method(*self.__args, **self.__kwargs);
        except Exception as err:
            #Do some handling here.
            raise;
        
class DispatcherQueue(object):

    def __init__(self):
        self.__queue = list();
        self.__queueLocker  =  threading.Lock();
        
    @property
    def IsEmpty(self):
        self.__queueLocker.acquire();
        status  = False;
        if(len(self.__queue) <= 0):
            status  =  True;
        self.__queueLocker.release(); 
        return status;

    @property
    def Count(self):
        return len(self.__queue);
    

    def Enqueue(self, operation: DispatcherOperation):
        self.__queueLocker.acquire();
        if(isinstance(operation, DispatcherOperation) != True):
            raise TypeError("@Enqueue: expecting a DispatcherOperation but {0} was given".format(type(operation)));
        index  =  len(self.__queue);
        self.__queue.append(operation);
        self.__queueLocker.release();
        return index;


    def Dequeue(self):
        self.__queueLocker.acquire();
        operation  =  None;
        if(self.Count > 0):
            operation =  self.__queue[0];
            del self.__queue[0];
        self.__queueLocker.release();
        return operation;
        

class Dispatcher(object):

    def __init__(self):
        self.__currentThread     =  threading.current_thread();
        self.__DispatcherQueue   = DispatcherQueue();
        self.__IsRunning         = False;


    def Invoke(self, method, *args , **kwargs):
         operation  =  DispatcherOperation(method,*args, **kwargs);
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


        

if(__name__ =="__main__"):
    def Task1():
        print("Task Running");

    def Task2(a , b):
        print(a + b);
        print("Task 2 Thread Id = {0} \n".format(threading.current_thread().name));


    def ExternalRun(dispatcher):
        a  = 1
        while(True):
            print("Thread Id = {0} \n".format(threading.current_thread().name));
            dispatcher.Invoke(Task2, a ,  6);
            a =  a + 1;
            time.sleep(1);
            


    dispatcher  =  Dispatcher();
    dispatcher.Invoke(Task1);
    dispatcher.Invoke(Task2, 5, 6);
    print(dispatcher.Thread);
    t  =  threading.Thread(target=ExternalRun, args=(dispatcher,));
    t.daemon = True;
    t.start();
    dispatcher.Run();
    

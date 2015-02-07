# -*- coding: utf-8 -*-

'''
Created on 18 Sep, 2014

PyMatrix implementation based on pure python oop charisma

Description:

@author: WANG LEI / YI, Research Associate @ NTU

@emial: L.WANG@ntu.edu.sg, Nanyang Technologcial University

@licence: licence
'''
from time import time

DEBUG_TIME_ELAPSE = False
DEBUG_GET_SET     = False 
DEBUG_LOG_LEVEL   = 'warning'
# this function for elapse time measurement
def timmer(func):
    
    def wrapper(*args, **keywords):
        # start time
        start  = time()
        # original call
        result = func(*args, **keywords)
        # end   time
        elapse = time() - start
        
        if  DEBUG_TIME_ELAPSE:
            print(func.__name__, ':\n\tconsumed ', '{0:<2.4f}'.format(elapse), ' seconds')
        return result
    
    return wrapper
#===========================================================================
# n-d matrix size discrptors: when it is 2-d or 1-d, it reduces to {row, col} form
#===========================================================================
class Size(object):
    
    def __init__(self, data=[]):        
        self.data = data
    
    def __iter__(self):
        return   self.data.__iter__() 
    
    def __get__( self, caller, callerType,):
        if  caller == None:#caller == None:
            return  self.__get__(caller, callerType)
        else:
            return Size( caller._get_shape_array() )
    
    def __getitem__(self, key,):
        try:
            return  self.data[key]
        except:
            return 0
    
    def __getattribute__(self, name,):
        try:
            return object.__getattribute__(self, name)
        except:
            if  name == 'row':
                try:
                    return self.data['row']
                except:  
                    try:
                        return self.data[0]
                    except:
                        return 0
                    
            if  name == 'col':
                try:
                    return self.data['col']
                except:
                    try:
                        return self.data[1]
                    except:
                        return 0
    def __len__(self):
        if  not    self.data:
            return 0
        return len(self.data)
    
    def __str__(self):
        return str( len(self.data) ) + ':' + str(self.data) + '\n'         


class Formatter(object):
    
    def __init__(self,   data = {'width':2, 'float':2}, ftemplate= ['{0:<{width}.{float}f} ', '{0:<{width}s} '], doc = 'formatter'):
        self.data      = data
        self.ftemplate = ftemplate
        
        self.__doc__   = doc

    def __iter__(self):
        pass

    def __get__(self, caller, callerType):
        if  caller == None:
            return self
        else:
            data = caller._init_matrix_formatter(width=2, float=2)
            ftemplate = caller.Init_matrix_options['ftemplate']
            return Formatter(data, ftemplate)
        
    def __getitem__(self, key):
            return self.ftemplate[key]
    
    def __getattribute__(self, name):
        try:
            return object.__getattribute__(self, name)
        except:
            if  name == 'float':
                return self.data['float']
            if  name == 'width':
                return self.data['width']
    

def checkKey(name, default, dict):
    try:
        value = dict[name]
    except KeyError as e:
        return default
    
    return value

class matrixArrayLists(list):
    '''
    Created on 17 Nov, 2014
    
    @author: wang yi/Lei, Researcher Associate @ EIRAN, Nanyang Technological University
    
    @email: L.WANG@ntu.edu.sg
    
    @copyright: 2014 www.yiak.co. All rights reserved.
    
    @license: license
    
    @decription: N-Matrix container for objects of any type. It then could be 2 or demensions numeric matrix for computation
    
    @param:
    '''
    # discriptors initialzation
    size                = Size()
    formatter           = Formatter()
    
    # options, configuration context
    Init_hint_options   = { 'r': None, 'c': None, 'debug'    : False, 'modifed_to_row_col': False         , 'ori_mem': None, }
    Init_matrix_options = { 'width':2, 'float':2, 'ftemplate':['{0:<{width}.{float}f} ', '{0:<{width}s} '],                  } 
    
    def __init__(self, *args, **hint):
        # initialization fo hint data    
        r = c = ori_mem = debug = None
        
        self._init_hint(hint)
      
        numberOfargs = len(args)
        
        # no inputting arguments
        if   numberOfargs == 0:
            if   hint == {}: pass
                # no hints              
            elif hint != {}:
                # set up empty matrix
                super(self.__class__, self).__init__([])
            
        elif numberOfargs == 1:
            # create a square null matrix. 2-D version
            if   isinstance(args[0], int):
                super(self.__class__, self).__init__()
                # specify n * n null matrix, done
                self.nil(args[0], args[0], self.Null())
            
            # create a matrix based on one inputting list    
            elif isinstance(args[0], list):
                # copy or convert
                super(self.__class__, self).__init__()
                # this works for matrix
                self.setUp( args[0],  self.r, self.c, self.ori_mem )    
                 
        elif numberOfargs == 2:
                # two integers are specified
            if   isinstance(args[0], int) and isinstance(args[1], int ):
                super(self.__class__, self).__init__()    
                # specify m * n null matrix
                self.nil(args[0], args[1], self.Null())
                 
                # combination of integer and list inputtings 
            elif isinstance(args[0], int) and isinstance(args[1], list):
                super(self.__class__, self).__init__()
                # To do: specify m * n null matrix
                self.nil(args[0], args[0], self.Null())
                
                self.setUp( args[1], args[0], c, ori_mem) 
                              
        elif numberOfargs  > 2:
            for i in range( 0, len(args) ):
                if not isinstance(args[i], int):
                    break
 
            if  i == 0 and isinstance(args[ 0 ], list):
                # To do: matrix cantenation
                super(self.__class__, list).__init__()
                
                # To do: union
                                  
            if  i != 0 and isinstance(args[ i ], list):
                # To do: specify, filling missing data by other iteratables
                super(self.__class__, list).__init__()
                
                # otherwise:
                # To do: args[0:i]
                # fillup
                self.fillUp(args[i+1:])
  
        # self._init_matrix_formmater()
   
    def _init_hint(self, hint):
        for name, default in self.Init_hint_options.items():
            # set local variables
            exec("self.%s = %s" % (name, checkKey(name, default, hint)))
   
    def _init_matrix_formatter(self, float=None, width=None, formatter=None):
        for name, default in self.Init_matrix_options.items():
            # set local variables
            exec("self.%s = %s" % (name, default))
         
        size = self.size
        
        n = 0
        m = []
        l = self.get_runtime_list()
        
        for j in range(size[1]):      
            n = 0
            for i in range(size[0]):
                try:
                    if  n < len(str(l[i][j])):
                        n = len(str(l[i][j])); 
                except Exception:
                    pass
            m.append(n + width)    
               
        return {'float':float, 'width':m}
    # matrix STL iterators
    class matrixIterator(object):
        def __init__(self, Mat):
            self.matrixArray = Mat
            self.counter = self.__counter__()
            
        def __iter__(self):
            return self

        ## ! just for two dimensions for the moment
        def __counter__(self):
            # stop index generation
            _STOP = True
            # opposite
            _CONT = False
            # commment the following lines when debug, other wise comment out
            # when apply matrix 2 list this will be call            
            size = self.matrixArray._get_shape_array()

            # initialization
            tier = len(size)
            
            # iteration indice
            iter = tier * [0]
            
            while True:
                yield iter
                
                def routine(iter, size, curr):
                    # add value at current position
                    try:
                        iter[curr] += 1
                    except Exception:
                        pass
                    # check whether it is flow out         
                    if  iter[curr] >= size[curr]:
                        # last positon
                        if  curr == 0:
                            return _STOP
                        else:
                            # clear the current bit
                            iter[curr] = 0
                            # go into higher bit
                            return routine(iter, size, curr - 1)              
                    
                    return  _CONT
                     
                signal = routine(iter, size, tier - 1)
        
                if  signal:
                    break
     
        def __next__(self):
            try:
                index = next(self.counter)
                return self.matrixArray[tuple(index)]
            except StopIteration as e:
                raise StopIteration()   
    
        def nextIndex(self):
            try:
                index = next(self.counter)
                return index
            except StopIteration as e:
                raise StopIteration()
            
        def __str__(self):

            if  isinstance(self.data, list):
                if  len(self.data)  > 2:
                    return "super matrix, shape: {0}".format( str(self.data) )
                if  len(self.data) == 2:
                    return "matrix, shape: row:{0}, col:{1}".format(self.data[0], self.data[1])
                if  len(self.data) == 1:
                    return "vector, shape: length: {0}".format(self.data[0])
 
    class Null():
        
        def __init__(self):
            pass
        
        def __len__(self):
            return 1
        
        def __str__(self):
            return 'null'
        
        def __repr__(self):
            return 'nullObect'
    
    def setIndice(self, l):
        pass
    
    def setHeader(self, l):
        self.insert( 0, list(l) )    
        
    def json2list(self, json):
        l = [[record[key] for key in json[0].keys()] for record in json]
        
        self.setUp(l)
        # set header
        self.setHeader( json[0].keys() )
        # set indice
        self.setIndice(range(0, len(l)))
        
    #===========================================================================
    # n-d matrix helper functions
    #===========================================================================           
    def name(self):
        return "matrixArrayLists:"
    
    #===========================================================================
    # elementary setup funciton from a iterable
    #===========================================================================
    def _toRow(self, r, c, l):
        # row vector
        if  not c and (r and r == 1):
            L = []
            for i in l:
                if  isinstance(i, list):
                    L.append(i)
                else:
                    L.append([i])
            self.extend(L)
            return

         
        if  c and c != 1 and (r and r == 1):
            # col vector:[[0,1,2...]]
            self.append([i for i in l])
            return
            
        if  c and c != 1 and not r:
            L = []
            for i in l:
                if  isinstance(i, list):
                    L.append(i)
                else:
                    L.append([i])
            self.extend(L)
            return 
    
    def _toCol(self, r, c, l):
        # col vector processing, simple mode
        if  r and r != 1 and not c:
            for i in l:
                if  isinstance(  i,  list ):
                    self.append( i )
                else:
                    self.append([i])
            return
        
        # col vector processing, simple mode
        if  r and r != 1 and (c and c == 1):
            # row vector:[[0],[1],[2],,,]
            for i in l:
                self.append([i])
            return
        # col vector
        if not r and (c and c == 1):
            for i in l:
                if  isinstance(i, list):
                    self.append(i)
                else:
                    self.append([i])
            return
    
    @timmer
    def setUp(self, l=None, r=None, c=None, o=None):
        # clearn up
        self.clear()
        self.modifed_to_row_col = False
        # set up container values
        if  str(type(l)) == "<class 'list'>":
            # calling from inside
            if  o == 'ori':
                self.extend(l)
                return
            
            # for default situation, from outside
            if  r == None and c == None:
                flag = True
                
                for i in l:
                    if  isinstance(i, list):
                        pass
                    else:
                        flag = False
                        break
                    
                if  flag:
                    self.extend(l)
                    return
                else:
                    c = 1    
            #===================================================================
            # col - vector processing
            #===================================================================            
            # col vector processing, simple mode
            if  r and r != 1 and not c:
                for i in l:
                    if  isinstance(  i,  list ):
                        self.append( i )
                    else:
                        self.append([i])
                        self.modifed_to_row_col = True
                return

            # col vector processing, simple mode
            if  r and r != 1 and (c and c == 1):
                # row vector:[[0],[1],[2],,,]
                self.append([i] for i in l)
                self.modifed_to_row_col         = True
                return
            # col vector
            if not r and (c and c == 1):
                for i in l:
                    if  isinstance(i, list):
                        self.append(i)
                    else:
                        self.append([i])
                        self.modifed_to_row_col = True
                return  

            #===================================================================
            # row vector processing
            #===================================================================
            # row vector
            if  not c and (r and r == 1):
                L = []
                for i in l:
                    if  isinstance(i, list):
                        L.append(i)
                    else:
                        L.append([i])
                        self.modifed_to_row_col = True
                self.extend(L)
                return

             
            if  c and c != 1 and (r and r == 1):
                # col vector:[[0,1,2...]]
                self.append([i for i in l])
                self.modifed_to_row_col         = True
                return
                
            if  c and c != 1 and not r:
                L = []
                for i in l:
                    if  isinstance(i, list):
                        L.append(i)
                    else:
                        L.append([i])
                        self.modifed_to_row_col = True
                self.extend(L)
                return 
            #===================================================================
            # special situation
            #===================================================================
            if  r and r == 1 and c and c == 1:
                self.append([i for i in l])
                self.modifed_to_row_col         = True
                return
            
            # by default
            self.extend(l)       
        else:
            
            it_index = l.__iter__()
            it_value = l.__iter__()
            while True:
                try:
                    index = it_index.nextIndex()
                    value = it_value.__next__()
                    # use redefined method
                    self[index] = value
                except StopIteration as e:
                    break

        # modify shape accordingly
    #===============================================================================
    # basic matrix filling function, m = matrixArray(list1, list2, list3 ...)
    #===============================================================================
    def fillUp(self, *iterators):
        obj = self
        
        for itx in iterators:
            itl, itr     =  (obj.__iter__(), itx.__iter__())
            while True:
                try:
                    p, q = (itl.nextIndex(), itr.__next__())
                    # use redefined method
                    obj[p] = q                  
                except StopIteration as e:
                    break 
        
        return self
    
    # this help funciton is exclusively for 2-demension case. I consider it seriously. 
    def nil(self, r, c, value=None):
        super(self.__class__, self).clear() 
        # set size 
        self.size.data = [r,c]        
#       self.head = [None] * self.row
        if   r > 1:
            from copy import deepcopy
            
            row = [value] * c
            
            for r in range(0, r):
#               self.head[r] = deepcopy(row)
                super(self.__class__, self).append(deepcopy(row))
        elif r == 1:
            for i in range(0, c):
                self.append(value) 
    
    # further extension form nil funciton            
    def Zeors(self, r, c=None):
        if  c == None:
            self.nil(r, r, 0)
        else:
            self.nil(r, c, 0) 
            
            
    def __call__(self, key=None, value=None, json=None, callback=None):
        if   key == None:
            if   json == None:
                pass
            elif json != None:
                pass
        elif key != None:
        
            if   value == None:
                return super(self.__class__, self).__getitem__(key)
            elif value != None:
                super(self.__class__, self).__setitem__(key, value)
                return self
    @timmer    
    def matrix2list(self):
        l = self.get_runtime_list()
        
        if len(l) == 1:
            if isinstance(l[0], list):
                l = l[0] 
        else:
            for i, v in enumerate(l):
                if isinstance(v, list):
                    if len(v) == 1:
                        l[i] = v[0]
        
        return l
    
    
    def get_runtime_list(self):
        return self( slice(0, len(self)) )
        
        
    def __setattr__(self, name, value):
        if   isinstance(name, tuple):
            pass
        elif True:
            self.__dict__[name] = value   
    
    def __iter__(self):
        return self.matrixIterator(self)

    def index_value(self, key):
        if  isinstance(key, int):
            return ([key],)
        if  isinstance(key, list):
            return ( key ,)
        if  isinstance(key, slice):
            start, stop, step = key.indices(len(self))
            return (list(range(start, stop, step)),) 
        if  isinstance(key, tuple):
            return tuple([self.index_value(i)[0] for i in key])         
    
    @timmer      
    def setitem(self,    key, value):
        if  isinstance(value, self.__class__):
            
            value = value.matrix2list()
        # currently set method doesn't support selector     
        if    isinstance(key, int):
            while True:
                try:
                    # old method
                    self(key, value)
                    break  
                except Exception as inst:
                    if  self.debug == True:
                        print(key, inst, 'set')
                    self.append(self.Null())
                
        elif isinstance(key, tuple):
            if   len(key) == 1:
                self.setitem(key[0], value)
            elif len(key) == 2: 
                
                while True:
                    try:
                        # old method
                        t = self(key[0])
                        break
                    except IndexError as e:
                        if  self.debug == True:
                            print(key[0], e, 'set')
                        self.append( self.Null() )
                
                # test codes for vector cases
                if  not isinstance(t, self.__class__) and not isinstance(t, list):
                    t = [t]
                    self(key[0], t)
                
                while True:
                    try:
                        t[key[1]] = value
                        break
                    except Exception as inst:
                        if  self.debug == True:
                            print(key[1], inst, 'set')
                        t.append(self.Null())
#               self[key[0]][key[1]] = value              
            elif len(key) >= 3:
                l = len(key) 
                # iteration part
                i = 0
                
                r = self.get_runtime_list() # global
                t = s = r                   # pre, succ
                
                while i < l - 1:
                    while True:
                        try:
                            t = s[key[i]]
                            break
                        except IndexError as e:
                            if  self.debug == True:
                                print(key[i],e,'set')
                            s.append(self.Null())
                        
                    if  not isinstance(t, self.__class__) and not isinstance(t, list):
                        t = [t]
                        s[key[i]] = t
                        s = t
                    
                    i += 1
                
                self.setUp(r)
                # get list
                while True:
                    try:
                        t[key[l-1]] = value
                        # do not need to process error
                        break
                    except Exception as inst:
                        if  self.debug == True:
                            print(inst)
                        t.append(self.Null())
#               self[key[:l-1]][key[l-1]] = value
#               print(self)

        elif True:
            raise TypeError("index must be int or slice")
    
    @timmer
    def setitem_multi(self, key, value):
        
        if   isinstance( key, int  ):
            self.setitem(key, value)
            
        elif isinstance( key, list ):
            for i in key:
                self.setitem(i, value[i])
                
        elif isinstance( key, slice):
            start, stop, step = key.indices(len(self))
            for i in range(start, stop, step):
                self.setitem(i, value[i])
            
        elif isinstance( key, tuple):
            
            def routines(curr, key, index):
                
                if  curr == depth:
                    for i in   key[curr - 1]:
                        try:
                            index[curr  - 1] = i
                        except Exception:
                            index.append(i)
                        # use settiem   
                        try: 
                            self.setitem(tuple(index), itv.__next__())
                        except StopIteration:
                            return 
                else:
                    for i in  key[curr - 1]:
                        try:
                            index[curr - 1] = i
                        except Exception:
                            index.append(i)
                        # push into functional stack    
                        routines(curr + 1, key, index) 
             
            depth = len( key )
            itv   = value.__iter__()                   
            index = self.index_value(key)  
            
            n = 0 
            for i in index:
                n = n * len(i)
                
            if  n > 1:
                # entry of the program                                            
                routines(1, index, [])  
            else:
                
                self.setitem(key, value)
                 
        return self
    
    def __setitem__(self, key, value): 
       
        if  isinstance(value, list) or isinstance(value, self.__class__): 
            self.setitem_multi(key, value)
        else:
            self.setitem( key, value)
        
        return self
    
    @timmer
    def getitem(self, key):
         
        if  isinstance(key, int):  
            try:                   
                size = self.size  
                flag = self.modifed_to_row_col
                if    flag and len(size) == 2 and size[0] == 1:
                    result = self( 0 )[key]
                   
                elif  flag and len(size) == 2 and size[1] == 1:
                    result = self(key)[ 0 ]
                else:
                    # it is possible that result is an integer           
                    result = self(key)#super(self.__class__, self).__getitem__(key)#how can we get sub matrixArray, i.e. mat is result : True
            
            except IndexError as e:
                if  self.debug == True:                   
                    print(key, e, 'get')
                return None
            if  isinstance(result, list):
                return self.__class__(result, ori_mem="'ori'")#self.__class__(result)# this method is bad
            elif True:
                return result
            
        elif isinstance(key, slice):
        
            start, stop, step = key.indices(len(self))
            results = []
            for i in range(start, stop, step):
                results.append( self(i) )               
            return    self.__class__(results, ori_mem="'ori'")#self.__class__(results)# this method is bad
        
        elif isinstance(key, list):
            
            results = []             
            for i in key:
                results.append( self(i) )                    
            return   self.__class__(results, ori_mem="'ori'")#self.__class__(results)# this method is bad                  
        
        # recursive calling     
        elif isinstance(key, tuple):
            # add codes here
             
            if   len(key) == 0:
                # return self
                return self
            elif len(key) == 1:
                # a special case
                return self.getitem(key[0])#self[key[0]] # call user defined
            elif len(key) >= 2:
                try:
                    if   isinstance(key[0], int):
                        # recursively calling
                        try:
                            return self.getitem(key[0]).getitem(key[1:])
                        except Exception as inst:
                        # if str(inst) == "'int...' object has no attribute 'getitem'":
                            size = self.size
                        
                            if  len(size) == 2 and size[1] == 1:
                                return self(key[0])[0]  
                            if  len(size) == 2 and size[0] == 1:
                                return self(0)[key[1]]
                            
                            raise(inst)
                        # this works but could produce side effects in succesive implementation
                        # return self[key[0]][key[1:]]

                    elif isinstance(key[0], slice) or isinstance(key[0], list):
                        # additional procession
                        results = self.getitem(key[0])#self[key[0]]
                        # in the future, I will change it to canecation matrix
                        l = len(results)
                         
                        tmarray = []#self.__class__()#[]
                        for i in range(0, l):
                            tmarray.append([])
                         
                        for i in range(0, l):
                            try:
                                a = results.getitem(   i ).getitem(key[1:])#.matrix2list()#tmarray.append( results.getitem(i).getitem(key[1:]) )  
                                try:
                                    a = a.matrix2list(   )
                                    
                                    tmarray[i].extend( a )
                                except:
                                    tmarray[i].append( a )
                            except:          
                                a = results.getitem(   i ) 
                                try:
                                    a = a.matrix2list(   )
                                    
                                    tmarray[i].extend( a )
                                except:
                                    tmarray[i].append( a )
                            # tmarray.append(results[i][key[1:]])               
                        results = tmarray                             
                        return self.__class__(results)#self.__class__(results)# this method is bad                         
                     
                except Exception as inst:
                    if  self.debug == True:
                        print(inst)
                    # if column vector                          
                    if  self.size.row == len(self):#self.col == 1:
                        flag = 1
                        for item in key[1:]:
                            if item != 0:
                                flag = 0
                                return None#raise( TypeError("wrong index") )
                        if  flag == 1:
                            return self.getitem(key[0])#self[key[0]]
                         
                    # if row vector
                    if  self.size.col == len(self):#self.row == 1:
                        flag = 1
                        for item in key[:len(key)-1]:
                            if item != 0:
                                flag = 0
                                return None#raise( TypeError("wrong index") )
                        if flag == 1:
                            return self.getitem(key[len(key)-1])#self[key[len(key)-1]]
                     
                    # universial purpose
                    if  str(inst) == 'list index out of range':
                        return None
                     
            elif True:
                raise TypeError("index must be int, list or slice")
    
    def index_len(self, key):
        if  isinstance(key, int):
            return (1,)
        if  isinstance(key, list):
            return (len(key),)
        if  isinstance(key, slice):
            start, stop, step = key.indices(len(self))
            return (len(range(start, stop, step)),) 
        if  isinstance(key, tuple):
            return tuple([self.index_len(i)[0] for i in key])      
    
    @timmer
    def __getitem__(self, key):
               
        hint = self.index_len(key) 
                
        if  len(hint) == 1:
            
            array = self.getitem(key)
            
            if  isinstance(array, self.__class__):
                return self.__class__(array.matrix2list(), r=hint[0])
            return array
            
        if  len(hint) >= 2:

            array = self.getitem(key)
            if  isinstance(array, self.__class__): 
                return self.__class__(array.matrix2list(), r=hint[0], c=hint[1])
            return array      
    
    def _str(self):
        
        size = self.size
        
        if  len(size)  > 2:
            pass#return self.name() + '\n' + super(self.__class__, self).__str__()
          
        # string representation
        out  = ""
        pre  = ' '
        succ = '\n '
        l    = self( slice(0, len(self)) )#self.matrix2list()
        
        # set title
        out += self.name() + '\n' + "["
        for i in range(len(l)):
            out += pre    
            for j in range(len(l[i])):
                out  = self._element2str(i, j, l, out)               
            if  i < len(l) - 1:
                out += succ       
        out += "]" 
        
        return out
    
    def _element2str(self, i, j, l=[], out=None):
        formatter =  self.formatter
        
        param = {'float': formatter.float, 'width': formatter.width[j]}
         
        if  i == len(l) - 1 and j == len(l[i]) - 1:
            param['width'] = 0
                   
        try:
            out +=     formatter[0].format(     l[i][j] ,     **param          )
        except ValueError:
            out +=     formatter[1].format( str(l[i][j]), width=param['width'] ) 
        except TypeError:
            if  not isinstance(l[i],  list):
                out += formatter[1].format( str(l[i]   ), width=param['width'] ) 
            elif l[i][j]:
                out += formatter[1].format( str(l[i][j]), width=param['width'] )
            elif True:
                out += formatter[1].format( 'null',       width=param['width'] )
        
        return  out
           
    __str__ = _str
    
    @timmer                
    def _get_shape_array(self):
        queue = []
        shape = []
        axis  = 0
        
        # updating axis 
        axis += 1
        
        tar   = self.get_runtime_list()
        # updating current axis
        shape.append( len(tar) )
        # start processing
        queue.append( (tar, axis) )
        # compute next demensions   
           
        def routines(obj, shape, axis, queue):
            
            while len(queue) > 0:
                
                obj, axis = queue.pop(0)   
                # temporary storage
                array = []
                               
                if   len(obj) == 0:
                    array.append(0)
                    
                elif len(obj) >= 1:
                    # broadth first searching
                    for i in range(0, len(obj) ):
                        if  isinstance(obj[i], list):
                            array.append( len(obj[i]) )
                            # broadth first
                            queue.append( (obj[i], axis + 1) )
                        elif True:
                            array.append( 1 )
                     
                    # updating current axis - Mat lenth
                    # axis control the looping layer        
                    try:
                        m = max( array )
                        if  shape[axis] < m:
                            shape[axis] = m
                    except:
                        shape.append( m )           
                elif True:
                    pass             
                      
        routines(tar, shape, axis, queue)  
        
        return shape[0:-1]      
     
    def trp(self):
        size = self.size
        mat  = self.__class__(size.col, size.row) 
        
        for i in range(size.row):
            for j in range(size.col):
                mat[i,j] = self[j,i]   
        return  mat
     
    def is_equal(self, obj):
        pass
    
    def is_tolerate(self, obj):
        pass              
 #===============================================================================
# operations between matrix
#===============================================================================
def union(*c, direction='l2r'):
    '''
    Created on 10 Dec, 2014
    
    @author: wangyi, Researcher Associate @ EIRAN, Nanyang Technological University
    
    @email: L.WANG@ntu.edu.sg
    
    @copyright: 2014 www.yiak.co. All rights reserved.
    
    @license: license
    
    @param: 
    
    @decription:
    
    @param: union
    '''

    def routine(left, right, direction):
        
        if   direction == 'l2r':
            if  isinstance(left, matrixArrayLists) and isinstance(right, matrixArrayLists):
                for i in range(0, max(left.size[0], right.size[0])):
                    r = left[i]
                    if   r != None:
                        # see documentation for difference between () and []
                        left(i).extend(right[i])        
                    elif r == None:
                        # do assignment
                        left[i]=right[i]
        elif direction == 'u2d':
            if  isinstance(left, matrixArrayLists) and isinstance(right, matrixArrayLists):
                for i in range(0, max(left.size[1], right.size[1])):
                    # see documentation for difference between () and []
                    left.append(right(i)) 
            
    # create an empty matrix            
    a = matrixArrayLists()
    
    # mian loop
    for b in c:
        routine(a, b, direction)
    
    return a

def rowTtf(m, i, j):
    temp = m[i,:]
    m[i, :] = m[j, :]
    m[j, :] = temp

def colTtf(m, i, j):
    temp = m[:,i]
    m[:, i] = m[:, j]
    m[:, j] = temp                 
            
         
class matrixArrayNumeric(matrixArrayLists):

    def __init__(self, *args, **hints):
        super(matrixArrayNumeric, self).__init__(*args, **hints)

    def name(self):
        return "matrixArrayNumeric:"
    
    def map(self, Func, *iterables):
        map_object = map(Func, self, *iterables)
        return self.__class__([m for m in map_object])
    
    def dot_iner(self, obj):
        
        sizel, sizer , flag = self.is_tolerate(obj)

        if  flag == False:
            raise  Exception("not match!")

        # return numeric value
        if  sizel.row == 1 and sizer.col == 1:
            sum = 0.0
            for k in range(sizel.col):
                sum += self[0,k] * obj[k,0]
            return sum
        
        mat = self.__class__(sizel.row, sizer.col)
        
        # return matrixArray-series object
        for i in range(sizel.row):
            for j in range(sizer.col):
                sum = 0.0
                for k in range(self.col):
                    sum += self[i,k] * obj[k,j]
                mat[i,j] = sum
                
        return  mat
    
    
class matrixArray(matrixArrayNumeric):
    
    def __init__(self, *args, **hints):
        super(matrixArray, self).__init__(*args, **hints)
        
    def name(self):
        return "matrixArrayNumeric:"
        
__all__ = [matrixArrayLists, matrixArrayNumeric, matrixArray]        
    
_TEST_MATRIX_MULTI = matrixArrayLists([
                         [['000', '001', '002'], ['010', '011', '012'], ['020', '021', '022']],
                         [['100', '101', '102'], ['110', '111', '112'], ['120', '121', '122']],
                         [['200', '201', '202'], ['210', '211', '212'], ['220', '221', '222']],
                         [['300', '301', '302'], ['310', '311', '312'], ['320', '321', '322']]
                         ])

_TEST_COMPUT = matrixArrayNumeric([]) 

if __name__ == "__main__":
    _TEST_COMPUT = matrixArrayNumeric([])      

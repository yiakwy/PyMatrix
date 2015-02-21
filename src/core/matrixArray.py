# -*- coding: utf-8 -*-
'''
Created on 18 Sep, 2014

PyMatrix implementation based on pure python oop charisma

Description:

@author: WANG LEI / YI, Research Associate @ NTU

@emial: L.WANG@ntu.edu.sg, Nanyang Technologcial University

@licence: licence
'''
__all__ = ["matrixArrayLists", "matrixArrayNumeric", "matrixArray"] 

from time import time

DEBUG_TIME_ELAPSE = False
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


# helper class for iteration over empty elements
class Null():
    
    def __init__(self, *args, **hints):
        pass
    
    def  __len__(self):
        return 1
    
    def  __str__(self):
        return 'null'
    
    def __repr__(self):
        return 'nullObect'
    
    
#===========================================================================
# n-d matrix size discriptor: when it is 2-d or 1-d, it reduces to {row, col} form
#===========================================================================
class Size(object):
    
    def __init__(self, data=[]):        
        self.data = data
    
    def __iter__(self):
        return \
        self.data.__iter__() 
    
    def __get__( self, caller, callerType,):
        if  caller == None:#caller == None:
            return \
                self.__get__(caller, callerType)
        else:
            return \
                self.__class__( caller._get_shape_array() )
    
    def __getitem__(self, key,):
        try:
            return self.data[key]
        except:
            return 0
    
    def __getattribute__(self, name,):
        try:
            return object.__getattribute__(self, name)
        except:
            if  name in ['row', 'col']:
                try:
                    return self.data[name]
                except:
                    return self.data[{'row':0, 'col':1}[name]]

            raise Exception("no such attribute")
        
    def __len__(self):
        if  not self.data:
            return 0
        return \
            len(self.data)
    
    def __str__(self):
        return str( len(self.data) ) + ':' + str(self.data) + '\n'         

    
    def assert_equal(self, size):
        # do implementation here
        return self, size, True
    
    def assert_tolerate(self, size):
        # do implementation here
        return self, size, True

# for matrix values, we just have two types, numeric and non-numeric classes
#===========================================================================
# n-d matrix formatter discriptor
#===========================================================================
class Formatter(object):
    
    def __init__(self, data = {'width':2, 'float':2}, description= ['{0:<{width}.{float}f} ', '{0:<{width}s} ']):
        self.templates = []
        self.templates.append(description[0])
        self.templates.append(description[1]) 
        self.data = data

    def __get__(self, caller, callerType):
        if  caller == None:
            return \
                self
        else:
            return Formatter(caller._init_matrix_formatter())
    
    def __getitem__(self, _id):
        return self.templates[_id]
    
    def __getattribute__(self, name):
        try:
            return object.__getattribute__(self, name)
        except:
            if  name == 'width':
                # get stored position
                a, b, c = self.position
                width = self.data[name]
                # get width for the element in column b
                return 0 if a == len(c) - 1 and b == len(c[a]) - 1 else width[b]
            if  name == 'float':
                return self.data[name]
    
    def register(self, template):
        self.templates.append(template)
    
    def store(self, a, b, c):
        # keep element position
        self.position = (a, b, c)
    
    # used to decorate element
    # format(element) -> new string
    def fire(self, element, a, b, c):
        # store the value
        self.position = (a, b, c)
        # return processed string
        try:
            return self[0].format(element,           width=self.width, float=self.float)
        except ValueError:
            return self[1].format(element.__str__(), width=self.width)
        except TypeError:
            return self[1].format(element.__str__(), width=self.width)
    __call__ = fire
    
#===========================================================================
# matrix input output middleware, this part will check all the input values on behalf of matrix
#===========================================================================
# wraps all the dirty parts here
class matrixMiddleWare(object):
    
    def __init__(self, *callbacks, position=0):
        self.pre_callbacks, self.post_callbakcs = \
                        callbacks[position], callbacks[:position]

    def fire(self, cls):
        
        self.cls = cls
        
        return Handlers(self.cls, self.pre_callbacks, self.post_callbacks)
    __call__ = fire
 
 
class Handlers(object):
    
    def __init__(self, cls,  pre__handlers, post_handlers):
        
        self.cls = cls
        self.pre__hanlders = pre__handlers
        self.post_handlers = post_handlers
        
    def fire(self, *args, **keywords):
        
        self.cls = self.cls(*args, **keywords)        
    __call__ = fire
        
    def __getattr__(self, name):
        attr = self.cls.__getattribute__(name)
        if  callable(attr):
            def hooked(*args, **kwargs):
                # fire pre  processing handlers
                for handler in self.pre__hanlders:
                    handler(*args, **kwargs)
                # inner running
                result = \
                       attr(*args, **kwargs)
                # fire post processing handlers
                for handler in self.post_handlers:
                    handler(*args, **kwargs)
                # prevent cls from becoming unwrapped
                return self if isinstance(result, self.cls.__class__) else result
            return hooked
        else:
            return attr           
    
# helper function
def index_len(key, l):
    if  isinstance(key, int):
        return (1,)
    
    if  isinstance(key, list):
        return (len(key),)
    
    if  isinstance(key, slice):
        start, stop, step = key.indices(l)
        return (len(range(start, stop, step)),) 
    #   entrance
    if  isinstance(key, tuple):
        return tuple([index_len(i, l.pop(0) if len(l) > 0 else 0)[0] for i in key]) 

# helper function
def index_val(key, l):
    if  isinstance(key, int):
        return ([key],)
    
    if  isinstance(key, list):
        return (key,)
    
    if  isinstance(key, slice):
        start, stop, step = key.indices(l)
        return (list(range(start, stop, step)),)
    #   entrance
    if  isinstance(key, tuple):
        return tuple([index_val(i, l.pop(0) if len(l) > 0 else 0)[0] for i in key])     
    
    
def checkKey(name, default, _dict):
    try:
        value = _dict[name]
    except KeyError:
        return default
    return \
        value


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
    Init_hint_options   = { 'r': None, 'c': None, 'debug' : False, 'modifed_to_row_col': False , 'ori_mem': None, }
    Init_matrix_options = { 'width':2, 'float':2,} 
    
    def __init__(self, *args, **hint):
        # initialization fo hint data 
        # because repesentation in 2 demension, r(row), c(col) are needed. It should be modifed by descriptor which will compute r, c whenver an instance call it.   
        
        self._init_hint(hint)
      
        numberOfargs = len(args)
        
        # no inputting arguments
        if   numberOfargs == 0:
            if   hint == {}: pass
                # no hints              
            elif hint != {}:
                # set up empty matrix
                # To do:
                
                # initialization
                super(matrixArrayLists, self).__init__([])
            
        elif numberOfargs == 1:
            # create a square null matrix. 2-D version
            if   isinstance(args[0], int):
                super(matrixArrayLists, self).__init__()
                # specify n * n null matrix, done
                self.nil(args[0], args[0], Null())
            
            # create a matrix based on one inputting list    
            elif isinstance(args[0], list):
                # copy or convert
                super(matrixArrayLists, self).__init__()
                # this works for matrix
                self.setUp( args[0], self.r, self.c, self.ori_mem )    
                 
        elif numberOfargs == 2:
                # two integers are specified
            if   isinstance(args[0], int) and isinstance(args[1], int ):
                super(matrixArrayLists, self).__init__()    
                # specify m * n null matrix
                self.nil(args[0], args[1], Null())
                 
                # combination of integer and list inputtings 
            elif isinstance(args[0], int) and isinstance(args[1], list):
                super(matrixArrayLists, self).__init__()
                # To do: specify m * n null matrix
                self.nil(args[0], args[0], Null())
                
                self.setUp( args[1], args[0], self.c, self.ori_mem) 
                              
        elif numberOfargs  > 2:
            for i in range( 0, len(args) ):
                if not isinstance(args[i], int):
                    break
 
            if  i == 0 and isinstance(args[ 0 ], list):
                # To do: matrix cantenation
                super(matrixArrayLists, self).__init__()
                
                # To do: union
                                  
            if  i != 0 and isinstance(args[ i ], list):
                # To do: specify, filling missing data by other iteratables
                super(matrixArrayLists, self).__init__()
                
                self.nil_multi(*args[0:i])
                # fillup
                self.fillUp(*args[i:])

   
    def _init_hint(self, hint):
        for name, default in self.Init_hint_options.items():
            # set local variables
            exec("self.%s = %s" % (name, checkKey(name, default, hint)))
   
    def _init_matrix_formatter(self, _float=2, _width=2, formatter=None):
        for name, default in self.Init_matrix_options.items():
            # set local variables
            exec("self.%s = %s" % (name, default))
         
        size = self.size
        
        col_length = 0
        width_list = []
        inner_list = self.get_runtime_list()
        
        for j in range(size[1]):      
            col_length = 0
            for i in range(size[0]):
                try:
                    if  col_length < len(str(inner_list[i][j])):
                        col_length = len(str(inner_list[i][j])); 
                except Exception:
                    pass
            width_list.append(col_length + _width)    
               
        return {'float':_float, 'width':width_list}
    
    
    # matrix STL iterators
    class matrixIterator(object):
        def __init__(self, Mat):
            self.matrixArray = Mat
            self.counter = self.__counter__()
            
        def __iter__(self):
            return   self

        ## ! just for two dimensions for the moment
        def __counter__(self):
            
            def routine(iter, size, curr):
                try:
                    iter[curr] += 1
                except Exception:
                    pass
                # check whether it is flow out         
                if  iter[curr] >= size[curr]:
                    
                    # last positon
                    if  curr == 0:
                        return True
                    else:
                        # clear the current bit
                        iter[curr] = 0
                        # go into higher bit
                        return routine(iter, size, curr - 1)              
                
                return  False
            # commment the following lines when debug, other wise comment out
            # when apply matrix 2 list this will be call            
            size = self.matrixArray._get_shape_array()

            # initialization
            tier = len(size)
            
            # iteration indice
            iter = tier * [0]
            
            while True:
                yield iter
                # update              
                signal = routine(iter, size, tier - 1)
                # exit processing
                if  signal:
                    break
     
        def __next__(self):
            try:
                index = next(self.counter)
                return self.matrixArray[tuple(index)]
            except StopIteration:
                raise StopIteration()   
    
        def nextIndex(self):
            try:
                index = next(self.counter)
                return tuple(index)
            except StopIteration:
                raise StopIteration()
            
        def __str__(self):
            return "matrix iterator"

    
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
            if  not isinstance(l[0], list):
                self.extend([l])
                self.modifed_to_row_col = True
            else:
                self.extend(l)
            return True

        # row vector:[[0,1,2...]] 
        if  c and c != 1 and (r and r == 1):
            if  not isinstance(l[0], list):
                self.extend([l])
                self.modifed_to_row_col = True
            else:
                self.extend(l)
            return True
            
        if  c and c != 1 and not r:
            if  not isinstance(l[0], list):
                self.extend([l])
                self.modifed_to_row_col = True
            else:
                self.extend(l)
            return True
    
    def _toCol(self, r, c, l):
        # col vector processing, simple mode
        if  r and r != 1 and not c:
            for i in l:
                if  isinstance(  i,  list ):
                    self.append( i )
                else:
                    self.append([i])
                    self.modifed_to_row_col = True
            return True

        # col vector processing, simple mode
        if  r and r != 1 and (c and c == 1):
            # row vector:[[0],[1],[2],,,]
            for i in l:
                if isinstance(   i,  list ):
                    self.append( i )
                else:
                    self.append([i])
                    self.modifed_to_row_col = True
            return True
        # col vector
        if not r and (c and c == 1):
            for i in l:
                if  isinstance(  i,  list ):
                    self.append( i )
                else:
                    self.append([i])
                    self.modifed_to_row_col = True
            return True
    
    def clear(self):
        super(matrixArrayLists, self).clear()
        # clear up all related marks
        self.modifed_to_row_col  = False
    

    def setUp(self, l=None, r=None, c=None, o=None):
        # clearn up
        self.clear()
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
                    if  isinstance(  i,  list):
                        self.append( i )
                    else:
                        self.append([i])
                        self.modifed_to_row_col = True
                return

            # col vector processing, simple mode
            if  r and r != 1 and (c and c == 1):
                # row vector:[[0],[1],[2],,,]
                for i in l:
                    if  isinstance(  i,   list):
                        self.append( i )
                    else:
                        self.append([i])
                        self.modifed_to_row_col = True
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
                if  not isinstance(l[0], list):
                    self.extend([l])
                    self.modifed_to_row_col = True
                else:
                    self.extend(l)
                return

            # row vector:[[0,1,2...]] 
            if  c and c != 1 and (r and r == 1):
                if  not isinstance(l[0], list):
                    self.extend([l])
                    self.modifed_to_row_col = True
                else:
                    self.extend(l)
                return
                
            if  c and c != 1 and not r:
                if  not isinstance(l[0], list):
                    self.extend([l])
                    self.modifed_to_row_col = True
                else:
                    self.extend(l)
                return 
            #===================================================================
            # special situation
            #===================================================================
            if  r and r == 1 and c and c == 1:
                if  not isinstance(l[0], list):
                    self.extend([l])
                    self.modifed_to_row_col = True
                else:
                    self.extend(l)
                return
            #===================================================================
            # by default
            #===================================================================
            self.extend(l)       
        else:
            
            it_index, it_value = l.__iter__(), l.__iter__()
            while True:
                try:
                    index, value = it_index.nextIndex(), it_value.__next__()
                    # use redefined method
                    # use customised magic expression "mat[:,[1,2,3],0,2:4] = another_matrix"
                    self[index] = value
                    # this is actually an  expression
                except StopIteration:
                    break

        # modify shape accordingly
    #===============================================================================
    # basic matrix filling function, m = matrixArray(list1, list2, list3 ...)
    #===============================================================================
    def fillUp(self, *iterators):    
        obj = self
        for itx in iterators:
            itl, itr = ( obj.__iter__(), itx.__iter__())
            while True:
                try:
                    p, q = (itl.nextIndex(), itr.__next__())
                    # use redefined method
                    obj[p] = q                  
                except StopIteration:
                    break 
        
        return self
    
    def nil_multi(self, *args):
        from copy import deepcopy
        # To do
        # check r, c, when it is used by user
        
        super(matrixArrayLists, self).clear()

        deep  = len(args)
        # set root node
        root  = [None for i in range(args[0])]
        # initialize a queue
        queue = []
        queue.append((root,0))
        # broad first searching
        while len(queue) > 0:
            child, i = queue.pop(0)
            # modify children           
            for j in range(args[i]):
                child[j] = deepcopy([None] * args[i+1])
                if  i+1  < deep-1:
                    queue.append( (child[j], i+1) )
                else:
                    child = child[j]
                    for j in range(0, args[i+1]):
                        child[j] = Null()
        # reset the empty matrix
        self.setUp(root)
                    
    # this help funciton is exclusively for 2-demension case. I consider it seriously. 
    def nil(self, r, c, value=None):
        from copy import deepcopy
        
        # To do
        # check r, c, when it is used by user
        
        super(matrixArrayLists, self).clear() 

        self.setUp([deepcopy([deepcopy(value) for _ in range(c)]) for _ in range(r)])
    
    # further extension form nil funciton            
    def Zeors(self, r, c=None):
        if  c == None:
            self.nil(r, r, 0)
        else:
            self.nil(r, c, 0) 
            
            
    def __call__(self, key=None, value=None):
        if  key == None:
            return self
        elif \
            key != None:
            if  value == None:
                return super(matrixArrayLists, self).__getitem__(key)
            elif \
                value != None:
                super(matrixArrayLists, self).__setitem__(key, value)
                return self
            
            
    @timmer    
    def matrix2list(self):
        l = self.get_runtime_list()
        
        # if it is a vector we need to leave it as list format
        # vector processing
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
        return self(slice(0, len(self)))
        
        
    def __setattr__(self, name, value):
        if   isinstance(name, tuple):
            pass
        elif True:
            self.__dict__[name] = value   
    
    def __iter__(self):
        return self.matrixIterator(self)

            
    def setitem(self, id, element, l):
        # see idex processing from int, slice, list and tuple, .
        # [[1],[1,2,3,4],[5]...] --> [1] or [1,2,3,4] or [5] --> [1,1,5], [1,2,5], [1,3,5],[1,4,5]..., depth first searching is applied to do such indexing
        # this assuming that value will automaticaly fill the part what index indicates
        # e.g.: 'matrix[[1,2,3],0] = value' means that find elements in 'value' to fill in a[1,0], a[2,0], a[3,0]
        curr = 0
        hook = l
        
        while curr < len(id) -1:
            try:
                l = l[id[curr]]
                curr += 1
                if  isinstance(l, list):
                    hook = l
                else:
                    l = [l]
                    hook[id[curr-1]] = l
            except:      
                steps = id[curr] - len(l) + 1
                l.extend([Null() for _ in range(steps)])
                
        while True:
            try:
                l[id[curr]] = element
                break
            except:
                steps = id[curr] - len(l) + 1
                l.extend([Null() for _ in range(steps)])                
            
    @timmer
    def getitem(self, _id, l):
        # see idex processing from int, slice, list and tuple
        # [[1],[1,2,3,4],[5]...] --> [1] or [1,2,3,4] or [5] ..., 
        try:
            return list(map(lambda idx: l.__getitem__(idx), _id))
        except:
            return [Null()]       
    
    def setitem_multi(self, ids, root, it):
        # deduce user behavior
        # get all possible id for setting
        def element_generator():      
            yield next(it)
        
        def routines(curr):
            #   exitance
            if  curr == depth:
                for i in ids[curr-1]:
                    index[curr-1] = i 
                    try: 
                        # set value
                        # get element
                        self.setitem(index, element_generator().__next__(), root)
                        
                    except StopIteration:
                        return 
            else:
                for i in ids[curr-1]:
                    index[curr-1] = i
                    # push into functional stack    
                    routines(curr+1)
        
        depth = len(ids)
        # this initialization will reduce exception handling
        index = depth * [0]
        # running
        routines(1)

         
    @timmer
    def getitem_multi(self, ids, root):
        # convert tuple to list(queue)  to obtain built-in methods
        # breadth first strategy
        l     = len(ids)
        stack = [(root, 0)]
        final = []
        
        while len(stack) != 0:
            try:
                child, axis = stack.pop(0)
                
                # processing
                for grdchild in self.getitem(ids[axis], child): 
                     
                    if   axis + 1 <  l - 1:
                        stack.append((grdchild,  axis+1))
                    elif axis <  l - 1:
                        final.append(self.getitem(ids[axis+1], grdchild))
                    else:
                        final.append(grdchild)

            except IndexError as e:
                print(e)
                break
            
        return  final    
        
    def __setitem__(self, key, value): 
        # later I will wrap this method in middleWare preprocessing
        # middleware preprocessing       
        hint  = index_len(key, self._get_shape_array())
        # middleware preprocessing 
        key   = index_val(key, self._get_shape_array())
        # get inner representation
        root  = self.get_runtime_list()
       
        if  max(hint) <= 1:
            self.setitem([item[0] for item in key], value, root) 
        else:
            self.setitem_multi(key, root, value.__it__())
        # make changes to the whole matrixArray
        self.setUp(root)
        return \
            self
    
    @timmer
    def __getitem__(self, key):
        # later I will wrap this method in middleWare preprocessing
        # middleware preprocessing       
        hint  = index_len(key, self._get_shape_array())
        # middleware preprocessing 
        key   = index_val(key, self._get_shape_array())
        
        root  = self.get_runtime_list()
        # get inner representation of the query result
        array = self.getitem_multi(key, root)
        try:
            if  max(hint) <= 1:
                # return the value wrapped in the list
                return array[0][0] if len(hint) == len(self._get_shape_array()) else \
                       self.__class__(array, r=hint[0])
            
            if  len(hint) == 1:
                return self.__class__(array, r=hint[0])
            else:
                return self.__class__(array, r=hint[0], c=hint[1])
        except:
            pass
   
    
    def _str(self):
        
        size = self.size
        
        if  len(size)  > 2:
            pass#return self.name() + '\n' + super(matrixArrayLists, self).__str__()
          
        # string representation
        out  = ""
        pre  = ' '
        succ = '\n '
        c    = self.get_runtime_list()
        
        # set title
        out += '\n' + self.name() + '\n' + "["
        for a in range(len(c)):
            out += pre    
            for b in range(len(c[a])):
                out += self._element2str(a, b, c)               
            if  a < len(c) - 1:
                out += succ       
        out += "]\n" 
        
        return out
    
    def _element2str(self, i, j, l=[]):
                
        try:
            return self.formatter(l[i][j], i, j, l)
        except TypeError:
            return self.formatter(l[i], i, j, l)
        pass
           
    __str__ = _str
                   
    def _get_shape_array(self):
        queue = []
        shape = []
        
        axis  = 0
        # updating axis 
        axis += 1
        
        root  = self.get_runtime_list()
        # updating current axis
        shape.append(len(root))
        # start processing
        queue.append((root,axis))
        # compute next demensions   
           
        def routines(obj, shape, axis, queue):
            
            while len(queue) > 0:
                
                child, axis = queue.pop(0)   
                # temporary storage
                array = []
                               
                if   len(child) == 0: array.append(0)
                elif len(child) >= 1:
                    # broadth first searching
                    for i in range(len(child)):
                        if  isinstance(child[i], list):
                            array.append(len(child[i]))
                            queue.append((child[i],axis+1))
                        elif True:
                            array.append(1)
                     
                    # updating current axis - maximu lenth
                    # axis control the looping layer  
                    _max = max(array)    
                    # try to update shape  
                    try:
                        if  shape[axis] < _max:
                            shape[axis] = _max
                    except:
                        shape.append(_max) 
                                                 
        routines(root, shape, axis, queue)  
        return shape[0:-1]      
     
    def trp(self):
        size = self.size
        mat  = self.__class__(size.col, size.row) 
        
        for i in range(size.col):
            for j in range(size.row):
                mat[i,j] = self[j,i]   
        return  mat
     
    def is_equal(self, obj):
        return self.size.assert_equal(obj.size)
        
    def is_tolerate(self, obj):
        return self.size.assert_tolerate(obj.size)              
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
    # print a for test
    return a

def row(m,i,j):
    temp = m[i,:]
    m[i,:] = m[j,:]
    m[j,:] = temp

def col(m,i,j):
    temp = m[:,i]
    m[:,i] = m[:,j]
    m[:,j] = temp                 

from operator import *
# TO DO PYCUDA IMPLEMENTATION                    
class matrixArrayNumeric(matrixArrayLists):

    def __init__(self, *args, **hints):
        super(matrixArrayNumeric, self).__init__(*args, **hints)

    def name(self):
        return "matrixArrayNumeric:"
    
    def map(self, Func, *iterables):
        map_object = map(Func, self, *iterables)
        return self.__class__([m for m in map_object])
    
    def add_matrix(self, obj):
        return self.map(add, obj) if self.is_equal(obj) else None# error will be raised inside
    __add__ = add_matrix
    
    def sub_matrix(self, obj):
        return self.map(sub, obj) if self.is_equal(obj) else None# error will be raised inside
    __sub__ = sub_matrix
    
    def neg_matrix(self, obj):
        return self.map(sub, obj) if self.is_equal(obj) else None# error will be raised inside
    __neg__ = neg_matrix
    
    def dot_in(self, obj):    
        sizel, sizer , flag = self.is_tolerate(obj)

        if  flag == False:
            raise  Exception("not match!")

        # return numeric value
        if  sizel.row == 1 and sizer.col == 1:
            sum = 0.0
            for k in range(sizel.col):
                sum += self[0,k] * obj[k,0]
            return sum
        
        # return matrixArray-series object
        mat = self.__class__(sizel.row, sizer.col)
        for i in range(sizel.row):
            for j in range(sizer.col):
                sum = 0.0
                for k in range(sizel.col):
                    sum += self[i,k] * obj[k,j]
                mat[i,j] = sum
                
        return  mat
    __mul__ = dot_in
    
class matrixArray(matrixArrayNumeric):
    
    def __init__(self, *args, **hints):
        super(matrixArray, self).__init__(*args, **hints)
        
    def name(self):
        return "matrixArrayNumeric:"
            
a = _TEST_MATRIX_MULTI = matrixArrayLists([
                         [['000', '001', '002'], ['010', '011', '012'], ['020', '021', '022']],
                         [['100', '101', '102'], ['110', '111', '112'], ['120', '121', '122']],
                         [['200', '201', '202'], ['210', '211', '212'], ['220', '221', '222']],
                         [['300', '301', '302'], ['310', '311', '312'], ['320', '321', '322']]
                         ])

b = _TEST_COMPUT = matrixArrayNumeric([]) 

if __name__ == "__main__":
    pass
    

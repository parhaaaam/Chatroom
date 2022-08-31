class jsonic(object):

    
    def __init__(self, args, **kwargs):
        self.deckeywords = kwargs
    
    def __call__(self, fn):
        def jsoner(obj, **kwargs):
            dic = {}
            key = None
            thedic = None
            recurse_limit = 2
            thefields = obj._meta.get_all_field_names()
            kwargs.update(self.deckeywords) 
            
            recurse = kwargs.get('recurse', 0)
            my_include = kwargs.get('include')
            my_skip = kwargs.get('skip')
            if my_include:
                thefields.extend(my_include) if type(my_include) == type([]) else thefields.append(my_include)

            if my_skip:
                if type(my_skip) == type([]):
                    [thefields.remove(skipper) for skipper in my_skip if skipper in thefields ]
                else:
                    if my_skip in thefields:
                        thefields.remove(my_skip)
            
            for field in thefields:
                try:
                    the_dictionary = getattr(obj, "%s_set" % field)
                except AttributeError:
                    try:
                        the_dictionary = getattr(obj, field)
                    except AttributeError: pass
                    except ObjectDoesNotExist: pass
                    else:
                        key = str(field)
                except ObjectDoesNotExist: pass
                else:
                    key = "%s_set" % field
                
                if key:
                    if hasattr(the_dictionary, "__class__") and hasattr(the_dictionary, "all") and callable(the_dictionary.all) and hasattr(the_dictionary.all(), "json") and recurse < recurse_limit:
                        kwargs['recurse'] = recurse + 1
                        dic[key] = the_dictionary.all().json(**kwargs)

                    elif hasattr(the_dictionary, "json") and recurse < recurse_limit:
                        kwargs['recurse'] = recurse + 1
                        dic[key] = the_dictionary.json(**kwargs)

                    else:
                        try:
                            the_unit = the_dictionary.__str__()
                        except UnicodeEncodeError:
                            the_unit = the_dictionary.encode('utf-8')
                        dic[key] = the_unit
            
            if hasattr(obj, "_ik") and hasattr(obj, obj._ik.image_field) and hasattr(getattr(obj, obj._ik.image_field), 'size') and getattr(obj, obj._ik.image_field):
             
                for ikaccessor in [getattr(obj, s.access_as) for s in obj._ik.specs]:
                    key = ikaccessor.spec.access_as
                    dic[key] = {
                        'url': ikaccessor.url,
                        'width': ikaccessor.width,
                        'height': ikaccessor.height,
                    }
            return fn(obj, json=dic, **kwargs)
        return jsoner

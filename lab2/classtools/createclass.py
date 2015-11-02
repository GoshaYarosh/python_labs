class ClassCreator(object):

        def __new__(cls, class_name, base_class, args_file_name):
            print args_file_name
            args = {}
            with open(args_file_name, 'r') as args_file:
                for arg in args_file:
                    attr = arg.split(':')[0]
                    value = arg.split(':')[1]
                    args[attr] = value
            return type.__new__(cls, class_name, base_class, args)

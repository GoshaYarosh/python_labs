class ClassCreator(type):

    def __new__(cls, class_name, base_class, args_file_name):
        return type.__new__(cls, class_name, base_class, args)

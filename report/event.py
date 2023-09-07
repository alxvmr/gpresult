class ImportantEvent():
    def __init__(self, text, info=None): # info - словарь
        self._text = text
        self._info = info # словарь

    @property
    def text(self):
        return self._text
    
    @property
    def info(self):
        return self._info
    

class Warning(ImportantEvent):
    type_obj = "warning"

    def __init__(self, text, info=None): # info - словарь
        super().__init__(text, info)
    
    def get_info_dict(self):
        return{
            "text":self.text,
            "info":self.info, # словарь
            "type":self.type_obj
        }
        
    
class Error(ImportantEvent):
    type_obj = "error"

    def __init__(self, text, info=None): # info - словарь
        super().__init__(text, info)

    def get_info_dict(self):
        return{
            "text":self.text,
            "info":self.info, # словарь
            "type":self.type_obj
        }
class USER:
    def __init__(self, client, alias):
        self.client = client
        self.alias = alias
        self.channel = None
    
    def changeChannel(self, channel):
        self.channel = channel
        
    
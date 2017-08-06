from io import BytesIO


class Response(object):
    def marshal(self):
        """
        
        :rtype: str 
        """


class LoginResponse(Response):
    def __init__(self):
        self.components = []
        self.buf = BytesIO()

    def add_component(self, component):
        self.components.append(component)

    def marshal(self):
        self.buf.truncate()
        [self.buf.write(component.marshal()) for component in self.components]
        return self.buf.getvalue()

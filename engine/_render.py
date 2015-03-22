__all__ = []

from weakref import *
from struct import pack

from ._GL import *

class Texture:
    def __init__(self, context, size, data):
        self.context = context
        context.ensure_active()

        self.size = w, h = size
        self.handle = handle = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, handle)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA8, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
        glBindTexture(GL_TEXTURE_2D, 0)

        def cleanup(_):
            context.ensure_active()
            glDeleteTextures(1, [handle])
        self.__weakself = ref(self, cleanup)

class VertexArray:
    def __init__(self, context):
        self.context = context
        context.ensure_active()

        self.handle = handle = glGenVertexArrays(1)
        self.__buffers = buffers = {}

        def cleanup(_):
            context.ensure_active()
            glBindVertexArray(handle)
            for index, buffer in buffers.items():
                glDisableVertexAttribArray(index)
                glDeleteBuffers(1, [buffer()])
            glBindVertexArray(0)
            glDeleteVertexArrays(1, [handle])
        self.__weakself = ref(self, cleanup)

    def set_attribute_buffer(self, index, data, count, type):
        self.context.ensure_active()

        glBindVertexArray(self.handle)
        buffer = self.__buffers.get(index, lambda: glGenBuffers(1))()
        glBindBuffer(GL_ARRAY_BUFFER, buffer)

        glBufferData(GL_ARRAY_BUFFER, data, GL_STATIC_DRAW)
        glVertexAttribPointer(index, count, type, GL_FALSE, 0, None)
        glEnableVertexAttribArray(index)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        self.__buffers[index] = lambda: buffer
        glBindVertexArray(0)

class Shader:
    def __init__(self, context, type, source):
        self.context = context
        context.ensure_active()

        self.handle = handle = glCreateShader(type)

        glShaderSource(handle, source)
        glCompileShader(handle)
        log = str(glGetShaderInfoLog(handle), "ASCII")
        if log:
            raise Exception(log)

        def cleanup(_):
            context.ensure_active()
            glDeleteShader(handle)
        self.__weakself = ref(self, cleanup)

class Program:
    def __init__(self, context, shaders):
        self.context = context
        context.ensure_active()

        self.handle = handle = glCreateProgram()

        for shader in shaders:
            glAttachShader(handle, shader.handle)
        glLinkProgram(handle)
        log = str(glGetProgramInfoLog(handle), "ASCII")
        if log:
            raise Exception(log)

        def cleanup(_):
            context.ensure_active()
            glDeleteProgram(handle)
        self.__weakself = ref(self, cleanup)


stuff_cache = WeakKeyDictionary()

def get_stuff_for(context, image):
    try:
        return stuff_cache[context][image]
    except KeyError:
        pass

    context.ensure_active()

    vertex_shader = r"""
        #version 330

        layout(location = 0) in vec2 XY;
        layout(location = 1) in vec2 UV;

        smooth out vec2 uv;

        void main()
        {
            gl_Position = vec4(XY.x, XY.y, 0.0, 1.0);
            uv = UV;
        }
    """

    fragment_shader = r"""
        #version 330
        #extension GL_ARB_explicit_uniform_location : enable

        layout(location = 2) uniform sampler2D img;

        smooth in vec2 uv;

        out vec4 color;

        void main()
        {
            color.rgb = texture(img, uv).rgb;
            color.a = 1.0;
        }
    """

    program = Program(context, [
        Shader(context, GL_VERTEX_SHADER, vertex_shader),
        Shader(context, GL_FRAGMENT_SHADER, fragment_shader),
    ])

    positions = [
        0.0, 0.0,
        1.0, 0.0,
        0.0, 1.0,
        1.0, 1.0,
    ]

    texture_coordinates = [
        0.0, 0.0,
        1.0, 0.0,
        0.0, 1.0,
        1.0, 1.0,
    ]

    texture = Texture(context, image.size, image.data)

    vertex_array = VertexArray(context)
    vertex_array.set_attribute_buffer(0, pack("{}f".format(len(positions)), *positions), 2, GL_FLOAT)
    vertex_array.set_attribute_buffer(1, pack("{}f".format(len(texture_coordinates)), *texture_coordinates), 2, GL_FLOAT)

    stuff = texture, program, vertex_array

    stuff_cache.setdefault(context, WeakKeyDictionary())[image] = stuff

    return stuff

__all__ += ["render"]
def render(surface, image):
    context = surface._context
    context.ensure_active()

    texture, program, vertex_array = get_stuff_for(context, image)

    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, texture.handle)
    glUseProgram(program.handle)
    glUniform1i(glGetUniformLocation(program.handle, b"img"), 0)
    glBindVertexArray(vertex_array.handle)
    glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
    glBindVertexArray(0)
    glUseProgram(0)
    glBindTexture(GL_TEXTURE_2D, 0)

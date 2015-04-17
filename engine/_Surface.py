import weakref
import struct

from ._SDL import *
from ._GL import *
from . import math


class _Texture:
    def __init__(self, context, size, data):
        self.context = context
        context.ensure_active()

        self.size = w, h = size
        self.handle = handle = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, handle)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA8, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
        glGenerateMipmap(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, 0)

        def cleanup(_):
            context.ensure_active()
            glDeleteTextures(handle)
        self.__weakself = weakref.ref(self, cleanup)


class _VertexArray:
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
            glDeleteVertexArrays(handle)
        self.__weakself = weakref.ref(self, cleanup)

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


class _Shader:
    def __init__(self, context, type, source):
        self.context = context
        context.ensure_active()

        self.handle = handle = glCreateShader(type)

        glShaderSource(handle, source)
        glCompileShader(handle)
        log = glGetShaderInfoLog(handle)
        if log.__class__ == bytes:
            log = str(log, "ASCII")
        if log:
            raise Exception(log)

        def cleanup(_):
            context.ensure_active()
            glDeleteShader(handle)
        self.__weakself = weakref.ref(self, cleanup)


class _Program:
    def __init__(self, context, shaders):
        self.context = context
        context.ensure_active()

        self.handle = handle = glCreateProgram()

        for shader in shaders:
            glAttachShader(handle, shader.handle)
        glLinkProgram(handle)
        log = glGetProgramInfoLog(handle)
        if log.__class__ == bytes:
            log = str(log, "ASCII")
        if log:
            raise Exception(log)

        def cleanup(_):
            context.ensure_active()
            glDeleteProgram(handle)
        self.__weakself = weakref.ref(self, cleanup)

    def get_uniform_location(self, name):
        result = glGetUniformLocation(self.handle, name)
        assert result != -1
        return result

    def get_attribute_location(self, name):
        result = glGetAttribLocation(self.handle, name)
        assert result != -1
        return result

_per_context_cache = weakref.WeakKeyDictionary()


def _get_context_cache(context):
    try:
        return _per_context_cache[context]
    except KeyError:
        pass

    context.ensure_active()

    vertex_shader = r"""
        #version 330

        uniform mat3x3 transformation;

        in vec2 a_position;
        in vec2 a_texture_coordinate;

        out vec2 texture_coordinate;

        void main()
        {
            vec3 position = vec3(a_position.xy, 1.0) * transformation;
            gl_Position = vec4(position.xy / position.z, 0.0, 1.0);
            texture_coordinate = a_texture_coordinate;
        }
    """

    fragment_shader = r"""
        #version 330

        uniform sampler2D image;

        in vec2 texture_coordinate;

        out vec4 fragment_color;

        void main()
        {
            fragment_color = texture(image, texture_coordinate);
        }
    """

    program = _Program(context, [
        _Shader(context, GL_VERTEX_SHADER, vertex_shader),
        _Shader(context, GL_FRAGMENT_SHADER, fragment_shader),
    ])

    per_image_cache = weakref.WeakKeyDictionary()

    def get_image_cache(image):
        try:
            return per_image_cache[image]
        except KeyError:
            pass

        w, h = image.size

        vertex_array = _VertexArray(context)

        positions = [
            0, 0,
            w, 0,
            0, h,
            w, h,
        ]

        vertex_array.set_attribute_buffer(
            program.get_attribute_location("a_position"),
            struct.pack("{}f".format(len(positions)), *positions), 2, GL_FLOAT)

        texture_coordinates = [
            0.0, 0.0,
            1.0, 0.0,
            0.0, 1.0,
            1.0, 1.0,
        ]

        vertex_array.set_attribute_buffer(
            program.get_attribute_location("a_texture_coordinate"),
            struct.pack("{}f".format(len(texture_coordinates)), *texture_coordinates), 2, GL_FLOAT)

        texture = _Texture(context, image.size, image.data)

        per_image_cache[image] = vertex_array, texture

        return vertex_array, texture

    _per_context_cache[context] = program, get_image_cache

    return program, get_image_cache


class Surface:
    def __init__(self, window):
        self.__context = window._context

    @property
    def size(self):
        return self.__context.window.size

    def render_image(self, image, to_surface=math.Matrix.identity):
        to_surface *= math.Matrix.translate(-self.size / 2) * math.Matrix.scale(math.Vector(+2, -2) / self.size)

        self.__context.ensure_active()

        program, get_image_cache = _get_context_cache(self.__context)
        vertex_array, texture = get_image_cache(image)

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, texture.handle)
        glUseProgram(program.handle)
        glUniform1i(program.get_uniform_location("image"), 0)
        glUniformMatrix3fv(
            program.get_uniform_location("transformation"), 1, True,
            struct.pack("9f", *(to_surface[i, j] for i in range(3) for j in range(3))))
        glBindVertexArray(vertex_array.handle)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
        glDisable(GL_BLEND)
        glBindVertexArray(0)
        glUseProgram(0)
        glBindTexture(GL_TEXTURE_2D, 0)

    def commit(self):
        self.__context.ensure_active()
        SDL_GL_SwapWindow(self.__context.window._handle)

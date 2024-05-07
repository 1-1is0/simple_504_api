import urllib
import uuid
import os


class ClassPropertyDescriptor(object):
    def __init__(self, fget, fset=None):
        self.fget = fget
        self.fset = fset

    def __get__(self, obj, klass=None):
        if klass is None:
            klass = type(obj)
        return self.fget.__get__(obj, klass)()

    def __set__(self, obj, value):
        if not self.fset:
            raise AttributeError("can't set attribute")
        type_ = type(obj)
        return self.fset.__get__(obj, type_)(value)

    def setter(self, func):
        if not isinstance(func, (classmethod, staticmethod)):
            func = classmethod(func)
        self.fset = func
        return self


def classproperty(func):
    if not isinstance(func, (classmethod, staticmethod)):
        func = classmethod(func)

    return ClassPropertyDescriptor(func)


global_uuid = uuid.uuid4()


class Config:
    class API:
        @classproperty
        def SECRET_KEY(cls):
            return os.getenv("SECRET_KEY")

        @classproperty
        def IS_LOCAL(cls):
            is_local = str(os.getenv("IS_LOCAL", "false")).lower()
            if is_local == "true":
                return True

    class Postgres:
        @classproperty
        def host(cls):
            return os.getenv("POSTGRES_HOST")

        @classproperty
        def port(cls):
            return os.getenv("POSTGRES_PORT")

        @classproperty
        def user(cls):
            return os.getenv("POSTGRES_USER")

        @classproperty
        def password(cls):
            return os.getenv("POSTGRES_PASSWORD")

        @classproperty
        def name(cls):
            return os.getenv("POSTGRES_DB")

    class Minio:
        @classproperty
        def host(cls):
            return os.getenv("MINIO_HOST")

        @classproperty
        def port(cls):
            return os.getenv("MINIO_API_PORT")

        @classproperty
        def access_key(cls):
            return os.getenv("MINIO_ROOT_USER")

        @classproperty
        def secret_key(cls):
            return os.getenv("MINIO_ROOT_PASSWORD")

        @classproperty
        def end_point(cls):
            return f"{cls.host}:{cls.port}"

        @classproperty
        def media_url(cls):
            return os.getenv("MINIO_STORAGE_MEDIA_URL")

        @classproperty
        def static_url(cls):
            return os.getenv("MINIO_STORAGE_STATIC_URL")

        @classproperty
        def storage_url(cls):
            return os.getenv("MINIO_STORAGE_URL")

        @classproperty
        def use_https(cls):
            https = os.getenv("MINIO_USE_HTTPS")
            if https.lower() == "true":
                return True
            return False

        secure = False
        default_bucket_name = "media"
        media_bucket_name = "media"
        static_bucket_name = "static"

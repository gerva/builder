import logging
import logging.config


cfg = {
  'version': 1,
  'filters': {},
  'formatters': {
      'short': {'format': '%(message)s'},
      'long': { 'format': '%(asctime)s %(levelname)-8s %(name)-15s %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'},
  },
  'handlers': {
      'console': {
          'class': 'logging.StreamHandler',
          'formatter': 'short',
          'level': 'INFO',
          'stream': 'ext://sys.stdout',
      },
      'file': {
          '()': 'logging.FileHandler',
          'formatter': 'long',
          'level': 'DEBUG',
          'mode' : 'a',
          'filename': '/tmp/test.log',
      },
  },
  'root': {
      'level' : logging.DEBUG,
      'handlers': ['file', 'console'],
  },
}

def logger(logger_name, file_name='/tmp/builder.log'):
    cfg['handlers']['file']['filename'] = file_name
    logging.config.dictConfig(cfg)
    return logging.getLogger(logger_name)

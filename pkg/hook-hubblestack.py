HIDDEN_IMPORTS = [
    'ssl',
    'crypto',
    'OpenSSL',
    'argparse',
    'base64',
    'HTMLParser',
    'json',
    'logging',
    'Crypto',
    'requests',
    'functools',
    'BaseHTTPServer',
    'argparse',
    'logging',
    'time',
    'pprint',
    'os',
    'random',
    'signal',
    'sys',
    'git',
    'daemon',
    'boto3',
    'botocore',
    'imp',
    'six',
    'inspect',
    'yaml',
    'traceback',
    'pygit2',
    'Queue',
    'azure.storage.common',
    'azure.storage.blob',
    'croniter',
    'vulners',

    # fdg readfile.json tries to absolute import a module during lazy load. Too
    # late for the packer to notice it should be packed in the binary.
    # marking it here for "hidden import"
    'hubblestack.utils.encoding',
]
DATAS = []
binaries = []


hiddenimports = HIDDEN_IMPORTS
# datas = DATAS
# binaries = BINARIES

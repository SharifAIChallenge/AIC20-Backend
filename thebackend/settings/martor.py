MARTOR_ENABLE_CONFIGS = {
    'imgur': 'true',  # to enable/disable imgur/custom uploader.
    'mention': 'false',  # to enable/disable mention
    'jquery': 'true',
    # to include/revoke jquery (require for admin default django)
    'living': 'false',  # to enable/disable live updates in preview
    'spellcheck': 'true',
}

MARTOR_ENABLE_LABEL = False
# Imgur API Keys
MARTOR_IMGUR_CLIENT_ID = 'your-client-id'
MARTOR_IMGUR_API_KEY = 'your-api-key'

# Safe Mode
MARTOR_MARKDOWN_SAFE_MODE = True  # default

# Markdownify
MARTOR_MARKDOWNIFY_FUNCTION = 'martor.utils.markdownify'  # default
MARTOR_MARKDOWNIFY_URL = '/api/martor/markdownify/'  # default

# Markdown extensions (default)
MARTOR_MARKDOWN_EXTENSIONS = [
    'markdown.extensions.extra',
    'markdown.extensions.nl2br',
    'markdown.extensions.smarty',
    'markdown.extensions.fenced_code',

    # Custom markdown extensions.
    'martor.extensions.urlize',
    'martor.extensions.del_ins',  # ~~strikethrough~~ and ++underscores++
    'martor.extensions.mention',  # to parse markdown mention
    'martor.extensions.emoji',  # to parse markdown emoji
    'martor.extensions.mdx_video',  # to parse embed/iframe video
]

# Markdown Extensions Configs
MARTOR_MARKDOWN_EXTENSION_CONFIGS = {}

# Markdown urls
MARTOR_UPLOAD_URL = '/martor/uploader/'  # default
MARTOR_SEARCH_USERS_URL = '/martor/search-user/'  # default

# Markdown Extensions
MARTOR_MARKDOWN_BASE_EMOJI_URL = \
    'https://github.githubassets.com/images/icons/emoji/'
# default from github
MARTOR_MARKDOWN_BASE_EMOJI_URL = \
    'https://github.githubassets.com/images/icons/emoji/'
# please change this to your domain
MARTOR_MARKDOWN_BASE_MENTION_URL = 'https://python.web.id/author/'

CSRF_COOKIE_HTTPONLY = True

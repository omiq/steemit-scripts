import sys
import metadata_parser
page = metadata_parser.MetadataParser(url=sys.argv[1],search_head_only=-1)
meta = page.metadata
print(meta['meta']['og:image'])

#!/usr/bin/env python

from ..common import *

def theplatform_download_by_pid(pid, title, output_dir='.', merge=True, info_only=False):
    smil_url = "http://link.theplatform.com/s/dJ5BDC/%s/meta.smil?format=smil&mbr=true" % pid
    smil = get_content(smil_url)
    smil_base = unescape_html(match1(smil, r'<meta base="([^"]+)"'))
    smil_videos = {y:x for x,y in dict(re.findall(r'<video src="([^"]+)".+height="([^"]+)"', smil)).items()}
    for height in ['1080', '720', '480', '360', '240', '216']:
        if height in smil_videos:
            smil_video = smil_videos[height]
            break
    assert smil_video

    type, ext, size = 'mp4', 'mp4', 0

    print_info(site_info, title, type, size)
    if not info_only:
        from ..processor.rtmpdump import has_rtmpdump_installed, download_rtmpdump_stream
        assert has_rtmpdump_installed(), "RTMPDump not installed."
        download_rtmpdump_stream(url=smil_base, playpath=ext+':'+smil_video, title=title, ext=ext, output_dir=output_dir)

site_info = "thePlatform.com"
download = theplatform_download_by_pid
download_playlist = playlist_not_supported('theplatform')

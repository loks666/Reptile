import sys
import hashlib
import bencode


def torrent_to_magnet(torrent_file):
    with open(torrent_file, 'rb') as f:
        metainfo = bencode.bdecode(f.read())
        hashcontents = bencode.bencode(metainfo['info'])
        digest = hashlib.sha1(hashcontents).digest()
        b32hash = hashlib.sha1(hashcontents).hexdigest()

        params = {
            'xt': 'urn:btih:%s' % b32hash,
            'dn': metainfo['info']['name']
        }

        # 将 trackers 添加到磁力链接
        tr = metainfo.get('announce', [])
        if 'announce-list' in metainfo:
            tr.extend(metainfo['announce-list'])

        params['tr'] = tr

        magnet = 'magnet:?%s' % '&'.join('%s=%s' % (k, v) for k, v in params.items())
        return magnet


if __name__ == '__main__':
    
    print(torrent_to_magnet("F:/迅雷下载/HorrorPorn.com/极品种子合集/Y套餐（日本有码女教师）/11部女教师.torrent"))

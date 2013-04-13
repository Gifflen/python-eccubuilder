#!/usr/bin/env python
#   Copyright 2013 Sam Chapler
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
import pyrax
import argparse


eccu = '<eccu>\n%s\n</eccu>'

req = '''  <match:request-header operation="name-value-cmp" argument1="Host" argument2=%s>
    <revalidate>now</revalidate>
  </match:request-header>\n'''

def auth(**kwargs):
    pyrax.set_credentials(kwargs['username'], kwargs['apikey'])
    return pyrax.cloudfiles

def get_container_uris(containers, **kwargs):
    cf = auth(username=kwargs['username'], apikey=kwargs['apikey'])
    cdn_uris = []
    for container in containers:
        cont = cf.get_container(container)
        if cont.cdn_enabled:
            cdn_uris.append((cont.cdn_uri, cont.cdn_ssl_uri,
                    cont.cdn_streaming_uri))
        else:
            print '%s is not CDN enabled. Skipping...' % cont
    return cdn_uris

def make_eccu(containers, **kwargs):
    endpoints = get_container_uris(containers, username=kwargs['username'],
            apikey=kwargs['apikey'])
    body = ''
    for endpoint in endpoints:
        for uri in endpoint:
            body = body + '%s' % (req % uri)
    print '%s' % (eccu % body)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('username', type=str)
    parser.add_argument('apikey', type=str)
    parser.add_argument('containers', type=str, nargs='*')
    args = parser.parse_args()

    make_eccu(args.containers, username=args.username, apikey=args.apikey)

if __name__ == '__main__':
    main()

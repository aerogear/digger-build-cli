from __future__ import print_function
import os

import pytest
import requests


@pytest.fixture
def template_names():
  names = [
    {
      'user': 'feedhenry-templates',
      'name': 'welcome-android-gradle',
      'branch': 'master'
    },
    {
      'user': 'feedhenry-templates',
      'name': 'blank-cordova-app',
      'branch': 'master'
    },
    {
      'user': 'feedhenry',
      'name': 'appforms-project-client',
      'branch': 'FH-v3.13.0'
    }
  ]
  return names


@pytest.fixture
def template_urls(template_names):
  url = 'https://github.com/%s/%s/archive/%s.zip'
  return [url % (tmpl['user'], tmpl['name'], tmpl['branch']) for tmpl in template_names]


@pytest.fixture(params=['./tests/fixtures'])
def download_templates(request, template_urls, template_names):
  folder = request.param
  if os.path.exists(folder) is False:
    os.makedirs(folder)
  for url in template_urls:
    fname = template_names[template_urls.index(url)]['name']
    branch = template_names[template_urls.index(url)]['branch']
    print('==> Downloading %s template' % fname)
    r = requests.get(url, stream=True)
    if r.status_code != 200:
      print('==> Invalid url: %s (%s)' % (url, r.status_code))
      continue
    print('==> Downloaded %s template' % fname)
    print('==> Saving %s template' % fname)
    with open('%s/%s-%s.zip' % (folder, fname, branch), 'wb+') as f:
      chunks = r.iter_content(chunk_size=1024)
      [f.write(chunk) for chunk in chunks if chunk]
    print('==> Saved %s template' % fname)

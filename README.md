# Ripcord

## Examples

### Twitter Timeline

Here's a simple Twitter client that grabs the latest public feed of the specified user handle. Notice how you can use dot-notation on the response body.

  import ripcord
  from ripcord.exceptions import HTTPError

  class Twitter(ripcord.Client):
    def __init__(self, **kwargs):
      super(Twitter, self).__init__(**kwargs)

      self.baseurl = 'https://api.twitter.com/'
      self.namespace = '1'
      self.endpoint = 'statuses/user_timeline'

    def timeline_for(self, handle, count=5):
      return self.get("{}.json".format(handle), params={'count': count})

  client = Twitter()

  try:
    response = client.timeline_for('wilhelm')
    print response.pop(0).text
  except HTTPError, e:
    print e

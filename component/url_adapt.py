def adapt(inp):
  ll = {}
  for i in inp:
   d = i["clientIdentifier"]
   con = i["connections"]
   trip = False
   urir = ""
   for i in con:
    if not trip:
      relay = i["relay"]
      uri = i["uri"]
      if relay:
        urir = uri
        trip = True
    ll[d] = uri
   return ll

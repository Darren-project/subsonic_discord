def adapt(inp):
  ll = {}
  for i in inp:
   d = i["clientIdentifier"]
   ll[d] = {}
   con = i["connections"]
   trip = False
   urir = ""
   for i in con:
    if not trip:
      relay = i["relay"]
      uri = i["uri"]
      if relay and not uri == '':
        urir = uri
        trip = True
   ll[d]["relay"] = urir
   trip = False
   urir1 = ""
   for i in con:
      if not trip:
        local = i["local"]
        uri = i["uri"]
        if not local and not uri == '':
          urir1 = uri
          trip = True
   ll[d]["direct"] = urir1
  return ll

import http.client

conn = http.client.HTTPSConnection("")

payload = "{\"clientId\":\"bb8829dd8e20ccbfb9a8a4240e77d047\",\"clientSecret\":\"94179706b77ce996339183edaee5209e\"}"

headers = { 'content-type': "application/json" }
conn.request("POST", "https://rest.jumbez.com/api/v1/customer/business/auth/token", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
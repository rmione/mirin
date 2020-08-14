require 'net/http'
require 'json'
uri = URI('https://kanjiapi.dev/v1/kanji/御'.force_encoding('utf-8'))
response = Net::HTTP.get(uri)

JSON.parse(response)

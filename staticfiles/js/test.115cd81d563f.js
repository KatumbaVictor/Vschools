/*
var canonical_querystring = '';

var date = new Date();

var year = date.getFullYear();
var month = date.getMonth();
var day = date.getDay()

var hours = date.getHours();
var minutes = date.getMinutes();
var seconds = date.getSeconds()

method = "GET";
service = "transcribe";
region = "us-east-1";
endpoint = "wss://transcribestreaming.us-west-2.amazonaws.com:8443";
host = "transcribestreaming.us-west-2.amazonaws.com:8443";
amz_date = `${year}${month}${day}T${hours}${minutes}${seconds}Z`;
datestamp = `${year}${month}${day}`;
access_key = 'AKIARLTR4RWUQPIM3AEB'

canonical_uri = "/stream-transcription-websocket"

canonical_headers = "host:" + host + "\n"
signed_headers = "host"

algorithm = "AWS4-HMAC-SHA256"

credential_scope = datestamp + "/" + region + "/" + service + "/" + "aws4_request"

canonical_querystring  = "X-Amz-Algorithm=" + algorithm
canonical_querystring += "&X-Amz-Credential="+ URI-encode(access_key + "/" + credential_scope)
canonical_querystring += "&X-Amz-Date=" + amz_date 
canonical_querystring += "&X-Amz-Expires=250"
canonical_querystring += "&X-Amz-Security-Token=" + token
canonical_querystring += "&X-Amz-SignedHeaders=" + signed_headers
canonical_querystring += "&language-code=en-US&media-encoding=flac&sample-rate=16000"

payload_hash = HashSHA256(("").Encode("utf-8")).HexDigest()

canonical_request = method + '\n' 
   + canonical_uri + '\n' 
   + canonical_querystring + '\n' 
   + canonical_headers + '\n' 
   + signed_headers + '\n' 
   + payload_hash

string_to_sign=algorithm + "\n"
   + amz_date + "\n"
   + credential_scope + "\n"
   + HashSHA256(canonical_request.Encode("utf-8")).HexDigest()

signing_key = GetSignatureKey(secret_key, datestamp, region, service)
                
signature = HMAC.new(signing_key, (string_to_sign).Encode("utf-8"), Sha256()).HexDigest

canonical_querystring += "&X-Amz-Signature=" + signature

request_url = endpoint + canonical_uri + "?" + canonical_querystring


// Create a canonical request

*/

var url = new URL('https://www.vschools.com')

var result = document.createElement('a');
result.setAttribute('href','/vschoolsmeet');
result.innerHTML = "victor";

document.body.appendChild(result)

console.log(url)
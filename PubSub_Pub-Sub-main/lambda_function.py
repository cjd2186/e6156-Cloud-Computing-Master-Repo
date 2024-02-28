import json
import urllib3

def lambda_handler(event, context):
    
    webhook_url = 'https://discord.com/api/webhooks/1178492564316373073/tHnRp49EG49Y7WsFgR7mWhiV_rNeF3oJ4tF9wmvzqc8Mg2DJg58bH5jkyIYGZqCv57In'

    # Our message sent to the webhook
    message = event['Records'][0]['Sns']['Message']

    
    embeds = {}
    
    # Create a dict with the message content
    data = {
        'content': message,
        "embded": embeds
    }
    
    # Convert dict to JSON object
    #json_data = json.dumps(data)
    
    # Send a POST request to the Discord webhook url
    #response = requests.post(webhook_url, data=json_data, headers={'Content-Type': 'application/json'})
    
    http = urllib3.PoolManager()
    
    json_responseBody = json.dumps(data)
    
    headers = {'Content-Type': 'application/json'}
    responseBody = { 'foo': 'bar' }
    #json_responseBody = json.dumps(responseBody)
    
    try:
        response = http.request('POST', webhook_url, headers=headers, body=json_responseBody)
        print("Status code:", response.status)
    
    except Exception as e:
        print(f"Error is {e}")

    # Confirm message was sent successfully
    if response.status == 204:
        return("Message successfully sent to Discord webhook")
    else:
        print(f"Failed to send message to the Discord webhook: {response.status}")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

import boto3

def publish_to_sns_topic(topic_arn, message, subject=None):
    """
    Publish a message to an AWS SNS topic.

    Parameters:
    - topic_arn (str): The Amazon Resource Name (ARN) of the SNS topic.
    - message (str): The message you want to publish to the topic.
    - subject (str): (Optional) The subject of the message.

    Returns:
    - dict: The response from the SNS service.
    """
    # Create an SNS client

    access_key= key
    secret_key= secret
    sns_client = boto3.client('sns', region_name='us-east-2', 
                              aws_access_key_id=access_key, 
                              aws_secret_access_key=secret_key)

    try:
        # Publish the message to the specified topic
        response = sns_client.publish(
            TopicArn=topic_arn,
            Message=message,
            Subject=subject
        )
        return response
    except Exception as e:
        # Handle the exception (e.g., log the error or raise a custom exception)
        print(f"Error publishing message to SNS topic: {e}")
        raise

# Example usage
if __name__ == "__main__":
    # Replace 'your-topic-arn' with the actual ARN of your SNS topic
    your_sns_topic_arn = 'arn:aws:sns:us-east-2:824386930839:rds_discord_notifications'
    name='Chris'
    # Replace 'Your message content' with the actual message you want to send
    message_content = f'New Player {name} Added to the database!'

    # Optional: Replace 'Your subject' with the subject of the message
    subject = 'Player Added!'

    try:
        # Publish the message to the SNS topic
        response = publish_to_sns_topic(your_sns_topic_arn, message_content, subject)

        print("Message published. Response:", response)
    except Exception as e:
        print(f"An error occurred: {e.response['Error']['Message']}")
        raise

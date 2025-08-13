import boto3

def detect_labels_local_file(photo):
    client = boto3.client('rekognition', region_name='ap-northeast-2')
    with open(photo, 'rb') as image:
        response = client.detect_labels(Image={'Bytes': image.read()})

    result = []

    for label in response['Labels']:

        Name = label["Name"]
        Confidence = label["Confidence"]

        result.append(f"{Name}일 확률은 {Confidence : .2f}%입니다")

    return "<br/>".join(map(str,result))
            

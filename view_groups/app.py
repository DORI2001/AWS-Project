def lambda_handler(event, context):
	body={"groups":["AWS","Lambda","API"]}
	return {
	     "statusCode":200,
	     "body":body
	}

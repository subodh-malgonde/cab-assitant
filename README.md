# cab-assistant

A tutorial for making your own Uber cab assistant using [Facebook Messenger Platform](https://developers.facebook.com/docs/messenger-platform), AWS [API Gateway](https://aws.amazon.com/api-gateway/) and [Lambda](https://aws.amazon.com/lambda/) and [Uber API](https://developer.uber.com/docs/rides/getting-started).

This repository contains code accompanying [this blog post](https://medium.com/p/2ae78ad83d58/).

![Banner Image](https://cdn-images-1.medium.com/max/800/1*8NTw72T3M_hk6bj7IomjEg.png)

### Install dependencies
- Install required libraries using pip. You need to install these libraries at a level of the function [main.py](./functions/process_chat/main.py).


    pip install requests pytz -t functions/process_chat
### AWS Credentials & API Gateway
- [Signup](http://docs.aws.amazon.com/lambda/latest/dg/setting-up.html#setting-up-signup) for AWS, if you haven't already
- You need AWS credentials to access its services like API Gateway and Lambda. We will do it using IAM (Identity and Access Management) user.
- Follow [this guide](http://docs.aws.amazon.com/apigateway/latest/developerguide/setting-up.html) to setup your IAM user, its permissions and get its credentials
- Also use the above guide to build and test an example API and create your own API endpoint.

### Facebook App and Page
- Follow this [quick start guide](https://developers.facebook.com/docs/messenger-platform/quickstart) to create a Facebook app and page
- For step 2 in the guide, use the API endpoint created above as the callback url
- In step 2, you will be asked to enter a verify token. Enter any string you want to and use the same string for the variable `FB_VERIFY_TOKEN` in [main.py](./functions/process_chat/main.py)
- Before you can verify and save, you need to deploy your code to AWS Lambda

### Lambda Code Deployment
- We will use [Apex](http://apex.run/) to deploy the code. This page also has instructions to get started.
- Install Apex
- Add the AWS credentials to your environment and IAM role to [project.json](./project.json)
- Now deploy the code with by running `apex deploy` in the terminal
- Your code should now be deployed to Lambda

### Link API Gateway to Lambda
- Now use the API gateway dashboard to integrate your API endpoint with the newly created lambda function

### Facebook Page Access Token
- Now complete steps 2 & 3 of the Messenger quick start guide.
- Get the page access token and assign it to the variable `FB_PAGE_ACCESS_TOKEN` in [main.py](./functions/process_chat/main.py)
- Re-deploy the code
- Complete step 5 of the quick start guide
- For testing purposes change the code in [main.py](./functions/process_chat/main.py) to echo back your chat messages
- Once you do this you can move on the Uber's API

### Uber API
- You will have to sign in with your Uber account and register an application with them [here](https://developer.uber.com/dashboard/create).
- You will be asked to enter a `redirect uri`. You can enter `http://localhost:8000`
- You will be provided with a `client_id`, `secret`, and `server_token`.
- Assign the `server_token` to the variable `UBER_SERVER_TOKEN` in [main.py](./functions/process_chat/main.py)
- Now you need your own access token to book rides via the API
- Follow the [authentication guide](https://developer.uber.com/docs/rides/authentication) to get your access token
- Make sure you authorize your self for all scopes. More on scopes [here](https://developer.uber.com/docs/rides/scopes)
- Once you get the access token assign it to `UBER_ACCESS_TOKEN` in [main.py](./functions/process_chat/main.py)


You are now ready to go.

You can reach me on [Twitter](https://twitter.com/SubodhMalgonde) if you have any questions.
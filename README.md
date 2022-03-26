# meetup-reminder-bot
Serverless Telegram bot to remind you to RSVP to your next Meetup session! Powered by [AWS Lambda](https://aws.amazon.com/lambda/) and [Amazon EventBridge](https://aws.amazon.com/eventbridge/).

# Pre-requisites
- [Terraform](https://www.terraform.io/) (v.1.1.7 and above)
- [Amazon Web Services (AWS)](https://aws.amazon.com/) account with [CLI v2 installed](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).
- [Telegram Bot account](https://core.telegram.org/bots)
- [Poetry](https://python-poetry.org/)

# Installation
- `git clone` this project
- `cd` into the project directory, and run `poetry install`.
- Run `terraform init`, followed by `terraform apply`. 
- Follow the prompts as instructed.
- To verify your installation, run `aws lambda invoke --function-name=$(terraform output -raw lambda_name) response.json` and inspect `response.json` using your favourite text editor. You should see something like 
```
{"message": "Not reminder hour yet"}
```

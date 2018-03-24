## Botie - Slack Slash Command Handling Made Easy

![](/docs/images/example.png)

Botie is a small python library built on [tornado](http://www.tornadoweb.org/en/stable/) to make writing [Slack Slash Commands](https://api.slack.com/slash-commands) super easy. 

See the [example](/example.py) for a quick rundown on its use. For a real-world example see [RipeBot](https://github.com/ross/ripebot/).

### Quickstart

1) Visit https://<your-slack>.slack.com/apps/manage/custom-integrations and click on "Slash Commands"
1) Choose "Add Configuration"
1) Enter `/echo` and click "Add Slash Command Integration"
1) Enter http://<publicly-accessible-ip-address>:8888/slack/echo in the "URL" field
1) Copy the token and run `export SLACK_AUTH_TOKENS=<token>`
1) Run ./script/bootstrap
1) source env/bin/activate
1) Run ./example.py --debug
1) Optionally repeat the above steps for `/itsfine`, comma separating `SLACK_AUTH_TOKENS`
1) In your slack type `/echo Hello World`
1) If you installed `/itsfine` try `/itsfine help` to see how help works

### Responding to messages basics

#### Synchronous

Synchronous responses are the easiest to think about and work with as they just include your bot's message in the response to the Slack command's request. There are several built in message types (PRs welcome for more) and the synchronous variants of these commands start with `write_` indicating that they're going to write the message into the body of the response. In general you'll almost always want to respond. If you don't the user's slash-command that invoked your bot won't appear in the channel which can be confusing. In cases where you plan to reply asynchronous, you should still do a `write_echo` in your handler function so that the user's command will appear immediately.

#### Asynchronous

Asynchronous messages are a lot more powerful. Unlike synchronous responses you can reply multiple times to provide status, progress, for for any reason you wish. If your command needs to do some work that might take a while to complete asynchronous is the way to go. You can immediately provide feedback by calling `write_echo` in the handler and then spend as much time as you like (up to 30m) building your response(s). The asynchronous message functions all start with `send_` indicating that they're going to send out a message to slack.

#### Message types

There are three existing message types built in to Botie. It's expected that the number and flexibility of of these will grow over time as more interesting stuff is built with botie.

* echo - Only available in a `write` variable, acknowledge that the command was received and tell slack to echo it back to the user
* simple - A simple text message, note that simple is a bit misleading as there's a lot of options available through [message formating](https://api.slack.com/docs/message-formatting)
* image - A combination text &amp; image respons done as an attachment

### Useful links

Amazingly there's at least 5 pages hosted by Slack on writing slash commands. I've included those below along with a link to the message formatting docs which is likely to be useful. Otherwise search results are pretty useful here.

* https://api.slack.com/docs/message-formatting
* https://api.slack.com/slash-commands
* https://api.slack.com/custom-integrations/slash-commands
* https://api.slack.com/tutorials/your-first-slash-command
* https://api.slack.com/tutorials/slash-commands-style-guide
* https://api.slack.com/tutorials/easy-peasy-slash-commands

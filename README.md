# autopkg-recipes
i
## Chatter PostProcessor

This requires requests to be installed:
```
pip install requests
```
This is based on the Slack notification post-processor for AutoPkg/JSSImporter that Graham Pugh created:
https://grahamrpugh.com/2017/12/22/slack-for-autopkg-jssimporter.html
Which inspired Slacker https://github.com/notverypc/autopkg-recipes/blob/master/PostProcessors/Slacker.py
Which contains all the good bits this Post Processor uses. 
This is just a port from Slack to Google Chat.

### Customising notifications:
Change the following values to match your environment or pass them as environmental variables.
```
webhook_url
card_img
```

Example:
```
/usr/local/bin/autopkg run <your_recipe_list> --post="com.github.johnmikep.autopkg-recipes.postprocessors/Chatter" --key webhook_url="Your_Chat_webhook" --key card_img="your_preferred_img"
```

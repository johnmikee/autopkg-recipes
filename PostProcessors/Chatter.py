#!/usr/bin/python

from autopkglib import Processor, ProcessorError

import subprocess
import os.path
import json
import requests
from httplib2 import Http
from json import dumps

# Set the webhook_url to the one provided by Google Chat when you create the webhook in the room

__all__ = ["Chatter"]


class Chatter(Processor):
    description = (
        "Posts to Slack via webhook based on output of a MunkiImporter. "
        "Based on Graham Pugh's slacker.py - https://github.com/grahampugh/recipes/blob/master/PostProcessors/slacker.py"
        "and "
        "@thehill idea on macadmin slack - https://macadmins.slack.com/archives/CBF6D0B97/p1542379199001400"
        "Takes elements from "
        "https://gist.github.com/devStepsize/b1b795309a217d24566dcc0ad136f784"
        "and "
        "https://github.com/autopkg/nmcspadden-recipes/blob/master/PostProcessors/Yo.py"
        "Basically all the good stuff from https://github.com/notverypc/autopkg-recipes/blob/master/PostProcessors/Slacker.py"
        "but modified for Google Chat."
    )

    input_variables = {
        "munki_info": {
            "required": False,
            "description": ("Munki info dictionary to use to display info."),
        },
        "munki_repo_changed": {
            "required": False,
            "description": ("Whether or not item was imported."),
        },
        "webhook_url": {"required": False, "description": ("Chat webhook.")},
    }

    output_variables = {}

    __doc__ = description

    def google_ding(self, webhook, name, version, catalog, pkg_path, pkginfo_path, img):
        url = webhook
        message_headers = {"Content-Type": "application/json; charset=UTF-8"}

        if img:
            card_img = img
        else:
            card_img = "https://i.imgur.com/FiNj8.jpg"

        bot_message = {
            "cards": [
                {
                    "header": {
                        "title": "New item added to repo",
                        "imageUrl": card_img,
                    },
                    "sections": [
                        {
                            "widgets": [
                                {
                                    "keyValue": {
                                        "topLabel": "Title",
                                        "content": name
                                    }
                                },
                                {
                                    "keyValue": {
                                        "topLabel": "Version",
                                        "content": version,
                                    }
                                },
                                {
                                    "keyValue": {
                                        "topLabel": "Pkg Path",
                                        "content": pkg_path,
                                    }
                                },
                                {
                                    "keyValue": {
                                        "topLabel": "Pkginfo Path",
                                        "content": pkginfo_path,
                                    }
                                },
                                {
                                    "keyValue": {
                                        "topLabel": "Catalog",
                                        "content": catalog,
                                    }
                                },
                            ]
                        },
                    ],
                }
            ]
        }

        http_obj = Http()

        response = http_obj.request(
            uri=url, method="POST", headers=message_headers, body=dumps(bot_message),
        )

        if int(response[0]["status"]) != 200:
            raise ValueError(
                "Request to Google Chat returned an error, the response is:\n%s"
                % response[0]["status"],
            )

    def main(self):
        was_imported = self.env.get("munki_repo_changed")
        webhook_url = self.env.get("webhook_url")
        card_img = self.env.get("card_img")

        if was_imported:
            name = self.env.get("munki_importer_summary_result")["data"]["name"]
            version = self.env.get("munki_importer_summary_result")["data"]["version"]
            pkg_path = self.env.get("munki_importer_summary_result")["data"][
                "pkg_repo_path"
            ]

            pkginfo_path = self.env.get("munki_importer_summary_result")["data"][
                "pkginfo_path"
            ]
            catalog = self.env.get("munki_importer_summary_result")["data"]["catalogs"]

            if name:
                self.google_ding(
                    webhook_url,
                    name,
                    version,
                    catalog,
                    pkg_path,
                    pkginfo_path,
                    card_img,
                )


if __name__ == "__main__":
    processor = Chatter()
    processor.execute_shell()

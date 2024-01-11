#!/usr/bin/env python3

import click
import os
import subprocess
import json
import yaml
from collections import OrderedDict


@click.command()
@click.option(
    "-d",
    "--destination",
    "publishDir",
    default="public",
    help="Filesystem path to write files to.",
    show_default=True,
)
@click.option(
    "-b",
    "--baseUrl",
    "baseUrl",
    default="/api",
    help="BaseUrl of deployment, should be set to the learners backend URL",
    show_default=True,
)
@click.option(
    "-e",
    "--envs",
    "contentEnvs",
    default="base,instructor,participant",
    help="Content environments to build.",
    show_default=True,
)
@click.option(
    "-s",
    "--statics",
    "staticFolders",
    default="res,_apps,_slides",
    help="Static folders to include in the build process.",
    show_default=True,
)
@click.option(
    "-c",
    "--config",
    "configFile",
    default="../../docker/config.yml",
    help="Set the config.yml file.",
    show_default=True,
)
@click.option(
    "-a",
    "--autocreate-tabs",
    "autoTabs",
    default=True,
    help="Create a learners tab for each folder in the content folder. If you want to set additional parameters such as tooltip or icon, do so manually in the config.yml file.",
    show_default=True,
)
@click.option(
    "-o",
    "--force-order",
    "forceOrder",
    default=True,
    help="If set, the default order of tabs is forced: documentation, exercises, presentations.",
    show_default=True,
)
@click.option(
    "-l",
    "--tabs-order-list",
    "tabsOrderList",
    default="documentation,exercises,presentations",
    help="Set the default ordering of tabs.",
    show_default=True,
)
@click.option(
    "-t",
    "--themecolors",
    "applyThemecolors",
    default=True,
    help="Set this to override the themecolor of the config file for the content.",
    show_default=True,
)
def main(
    publishDir,
    baseUrl,
    contentEnvs,
    staticFolders,
    configFile,
    autoTabs,
    forceOrder,
    tabsOrderList,
    applyThemecolors,
):
    """Script to generate static files for the learners environment."""

    contentEnvs = contentEnvs.split(",")
    staticFolders = staticFolders.split(",")
    tabsOrderList = tabsOrderList.split(",")
    publishDir += "/hugo"

    # Resolve path if in symlink
    current_working_dir = subprocess.check_output("pwd", shell=True, text=True)
    path_components = current_working_dir.split(os.path.sep)[:-2]
    hugo_base_path = f"/{os.path.join(*path_components)}/"

    cmdPublishDir = publishDir
    if not os.path.isabs(cmdPublishDir):
        cmdPublishDir = os.path.join(hugo_base_path, cmdPublishDir)

    if vite_backend := os.getenv("VITE_BACKEND"):
        baseUrl = vite_backend

    # Check if publishDir exists
    prompt = f"[info] Checking if destination directory '{publishDir}' exists ..."
    if not os.path.isdir(cmdPublishDir) or not os.path.exists(cmdPublishDir):
        subprocess.run([f"mkdir -p {cmdPublishDir}"], shell=True)
        print(f"{prompt} CREATED")
    else:
        print(f"{prompt} CHECK")

    # Clean publishDir if not empty
    if len(os.listdir(f"{cmdPublishDir}")) != 0:
        subprocess.run([f"rm -r {cmdPublishDir}/*"], shell=True)
        print(f"[info] Cleaning publish directory {publishDir} ... CHECK")

    print("\n[info] Extracting information... ")
    os.system(
        f"hugo -e _default -d {publishDir}/base -s ../../ --baseURL /{baseUrl}/statics/hugo/base --quiet"
    )

    print(f"[info] Default env built")
    try:
        with open(f"{cmdPublishDir}/base/en/index.json") as input_file:
            json_data = json.load(input_file)

            # Extract Exercises
            flattened_exercise_data = {}
            for exercise in json_data.get("exercises"):
                flattened_exercise_data[exercise.get("global_exercise_id")] = exercise

            with open(f"{cmdPublishDir}/exercises.json", "w") as output_file:
                json.dump(flattened_exercise_data, output_file)

            # Extract Questionnaires
            flattened_questionnaire_data = {}
            for questionnaire in json_data.get("questionnaires"):
                flattened_questionnaire_data[
                    questionnaire.get("global_questionnaire_id")
                ] = questionnaire

            with open(f"{cmdPublishDir}/questionnaires.json", "w") as output_file:
                json.dump(flattened_questionnaire_data, output_file)

                # Extract Exercises
            flattened_page_data = {}
            for page in json_data.get("pages"):
                flattened_page_data[page.get("page_id")] = page

            with open(f"{cmdPublishDir}/pages.json", "w") as output_file:
                json.dump(flattened_page_data, output_file)

        print(f"[info] Exercises-json: '{publishDir}/exercises.json'")
        print(f"[info] Questionnaire-json: '{publishDir}/questionnaires.json'")
        print(f"[info] Pages-json: '{publishDir}/pages.json'\n")
    except EnvironmentError as e:
        print(f"[error] An error occurred: {str(e)}")

    # Building hugo static pages
    print("[info] Building Hugo pages:")
    for hugoEnv in contentEnvs:
        buildHugoFiles = f"hugo -e {hugoEnv} -d {publishDir}/{hugoEnv} -s ../../ --baseURL /{baseUrl}/statics/hugo/{hugoEnv} --quiet"
        os.system(buildHugoFiles)
        print(f"       - Environment '{hugoEnv}' built")
        if hugoEnv != "base":
            for staticFolder in staticFolders:
                createSymLink = f"ln -s ../base/{staticFolder} {cmdPublishDir}/{hugoEnv}/{staticFolder}"
                os.system(createSymLink)
                print(f"         Created Symlink for static Folder '{staticFolder}'")

    if autoTabs:
        folder_list = create_folder_list(os.path.join(hugo_base_path, "content"))
        generate_yaml(folder_list, configFile, forceOrder, tabsOrderList)
        print("[config] Create tabs config ... CHECK")
    else:
        print("[config] Create tabs config ... SKIPPED")

    if applyThemecolors:
        try:
            with open(configFile, "r") as yaml_file:
                config = yaml.safe_load(yaml_file)
                primary_color = config["learners"]["theme"]["secondary"]
                for hugoEnv in contentEnvs:
                    css_file_path = f"{publishDir}/{hugoEnv}/css/theme-cyberrange.css"
                    update_css(css_file_path, primary_color)
                print("[config] Updating theme color ... CHECK")
        except Exception as e:
            print("[config] Updating theme color ... FAIL")
            print(f"[error] An error occurred: {str(e)}")
    else:
        print("[config] Updating theme color ... SKIPPED")


def update_css(css_file_path, primary_color):
    try:
        with open(css_file_path, "r") as css_file:
            css_lines = css_file.readlines()

        updated_css_lines = []
        for line in css_lines:
            if line.strip().startswith("--primary-color"):
                updated_css_lines.append(f"  --primary-color: {primary_color};\n")
            else:
                updated_css_lines.append(line)

        with open(css_file_path, "w") as css_file:
            css_file.writelines(updated_css_lines)

    except Exception as e:
        print(f"[error] An error occurred: {str(e)}")


def create_folder_list(directory):
    if not os.path.exists(directory) or not os.path.isdir(directory):
        raise ValueError("[error] Invalid content directory path")

    folders = [
        folder
        for folder in os.listdir(directory)
        if os.path.isdir(os.path.join(directory, folder))
    ]
    folders.sort()
    return folders


def represent_ordereddict(dumper, data):
    return dumper.represent_dict(data.items())


def generate_yaml(folder_list, yaml_file_path, forceOrder, tabsOrderList):
    if os.path.exists(yaml_file_path):
        with open(yaml_file_path, "r") as yaml_file:
            config_yaml = yaml.safe_load(yaml_file)
    else:
        config_yaml = {"tabs": OrderedDict()}

    ordered_new_tabs = OrderedDict()

    current_tabs = {}
    if config_yaml["tabs"]:
        current_tabs = OrderedDict((k, v) for k, v in config_yaml["tabs"].items())

    for tabname, tab in current_tabs.items():
        if not type(tab) is dict:
            print(tabname, tab)
            current_tabs[tabname] = {"show": ["all"]}
        elif not tab.get("show"):
            tab["show"] = ["all"]

    # apply given order
    if forceOrder:
        for key in tabsOrderList:
            if current_tabs.get(key):
                ordered_new_tabs[key] = current_tabs[key]
    else:
        ordered_new_tabs = current_tabs

    # Add missing folders
    for folder in folder_list:
        if folder not in current_tabs:
            ordered_new_tabs[folder] = {"show": ["all"]}
        else:
            ordered_new_tabs[folder] = current_tabs[folder]

    for key, value in current_tabs.items():
        ordered_new_tabs[key] = value

    config_yaml["tabs"] = ordered_new_tabs

    with open(yaml_file_path, "w") as yaml_file:
        yaml.add_representer(OrderedDict, represent_ordereddict)
        yaml.dump(
            config_yaml,
            yaml_file,
            indent=4,
        )


if __name__ == "__main__":
    main()

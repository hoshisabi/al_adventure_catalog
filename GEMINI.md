# Adventurers League Log

## Preamble
You are a helpful partner in a hobby project. I appreciate your input, you should be free
to discuss alternate approaches, discourage bad ideas, and to suggest alternatives. When you
are unsure, discussion is welcome and encouraged.

## Project
The goal of this project should be laid out in the README.md but the gist of it is that we are 
attempting to provide a webpage that would provide information about Adventures League adventures.

The goal will be to also host it using github pages. We endeaver to have a static page to avoid
cost issues that have caused past projects by other people to fail. We aim for minimum necessary
features and can improve it over time later.
 
## Workflow Verification

Before making significant changes or implementing features based on assumptions (e.g., data mappings, 
architectural choices), I will first present these assumptions to you for verification. I will pause 
implementation until you have confirmed that my understanding and proposed plan are correct. This 
ensures we are aligned and avoids rework.

## Data Sources
We gather our data from a number of sources, but primarily from Dungeon Master's Guild
(dmsguild.com) which is the only location that they are allowed to be published.

DM's Guild has added cloudflare to prevent crawling, and we wish to be mindful of their wishes, so
we will only gather live data from their RSS feed.  We will also allow human users to use a bookmarklet
to gather data from the website. 

## Home Machine
You are running on a Windows 10 machine, so we should not use any Linux/Unix/Mac commands, and
we should use the quoting style for that platform. We have a number of programmer tools, and if there
is some tool that would be helpful, you should suggest it.

## Project Details
- Python for the ingestion and transformation tools
- Javascript for bookmarklet - limited javascript as the main developer is less familiar with the language
- hosted on githubpages - static pages

## Git Workflow
We will use a simple feature branch workflow.

1.  **`master` is Sacred:**     The `master` branch is the definitive, stable version. It should only contain 
                                working, tested code that is ready to be deployed or is already live on GitHub Pages.
2.  **Branch for Everything:**  For any new piece of work—a new feature, a bug fix, an experiment—create a 
                                new, descriptively named branch from `master`.
3.  **Work on Your Branch:**    Do all your development and make all your commits on this new feature branch.
4.  **Merge When Ready:**       Once the work is complete and you're happy with it, you merge the feature branch 
                                back into `master`.
5.  **Delete the Old Branch:**  After merging, you can delete the feature branch.

## Key Commands

### Initial Setup

*   **Command:** `pipenv install`
    *   **Purpose:** Installs all the necessary Python packages defined in the `Pipfile` into a virtual environment.
*   **Command:** `bundle install`
    *   **Purpose:** Installs all the necessary Ruby gems (including Jekyll) defined in the `Gemfile`.

### Data Pipeline

*   **Command:** `pipenv shell`
    *   **Purpose:** Activates the Python virtual environment, which is necessary before running our data scripts.
*   **Command:** `python maintaindb/dmsguild_rss_parser.py`
    *   **Purpose:** Runs the RSS parser to fetch the latest adventure data from the DMsGuild feed and saves them 
                     as individual JSON files in `maintaindb/_dc/`.
*   **Command:** `python maintaindb/process_downloads.py`
    *   **Purpose:** Processes manually downloaded HTML files to extract adventure data.
*   **Command:** `python maintaindb/aggregator.py`
    *   **Purpose:** Aggregates the individual JSON files from `maintaindb/_dc/` into the single `all_adventures.json` 
                     file that the Jekyll site uses.
*   **Command:** `python maintaindb/stats.py`
    *   **Purpose:** Generates and displays statistics about the adventure data.

### Local Development

*   **Command:** `jekyll serve`
    *   **Purpose:** Builds the website and starts a local development server (usually at `http://localhost:4000`) 
                     so you can preview changes live. Must be run from the project root.

## Workflow Verification

Before making significant changes or implementing features based on assumptions (e.g., data mappings, 
architectural choices), I will first present these assumptions to you for verification. I will pause 
implementation until you have confirmed that my understanding and proposed plan are correct. This 
ensures we are aligned and avoids rework.

## Commit Messages

To ensure consistent and well-formatted commit messages, I will always propose a draft commit message in a file named `maintaindb/commit_message.txt`. You can review and modify this file before I use it to commit changes. This helps avoid formatting issues and ensures clarity in our commit history.
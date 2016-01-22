#!/usr/bin/env python
##Written by Vincent Flesouras and Adam Duston
##When you have a thousand directories to move from SVN to Github, you don't do it by hand.
print(
    "This script gathers the list of directories it is initialized in and forms a dictionary of paths \n"
    "It then runs the dir through a process that makes a git repository, populates the index\n"
    "pushes it to github.\n"
)
import os
from glob import glob
from subprocess import call
import yaml
from git import *
from github import Github
from github import GithubException

#We run this in a specific directory
mypath = os.getcwd()
# Configuration
with open(mypath + "/cfg.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)
print(cfg)
my_dirdict = paths = glob('*/')
#os.listdir(mypath)
g = Github(cfg['user']['NAME'], cfg['user']['TOKEN'])
join = os.path.join
org = g.get_organization(cfg['user']['ORG'])


def main():
    git_loop(mypath)


#main loop
def git_loop(mypath):
    for i,s in enumerate(my_dirdict):
        print "-------------------------------------------"
        print "------ Building New Git Repository --------"
        print "-------------------------------------------"
        # Setup Local Repo
        curdir = str(s)
        curpath = mypath + "/" + str(s)
        init_local(curpath, curdir)
        # Setup Remote Repo
        init_github_remote(curpath, curdir)


#create local repo
def init_local(curpath, curdir):
    print "-------------------------------------------"
    print "-- Initializing local repo & pushing to remote"
    print "-------------------------------------------"
    #call(["git", "init", curpath])
    new_repo = Repo.init(curpath)
    assert new_repo
    remote_url="ssh://" + cfg['user']['NAME'] + "@" + cfg['paths']['HOST'] + "/" + curdir
    index=new_repo.index
    assert new_repo.is_dirty(True, True, True)  # check the dirty state
    dirty = new_repo.untracked_files
    for d in dirty:
        index.add(d)

    index.commit(
            "Initial import",
            None,
            True,
            cfg['user']['NAME'])

    if not new_repo.remotes:
        try:
            remote = new_repo.remote('origin')
            remote.create(curdir,curdir,remote_url)
            remote.push(progress=True)
            print "--"
            print "-- Your new git repo '$REPO' is ready and initialized at:"
            print "-- $USER@$HOST/$GIT_PATH/$REPO"
            print "--"

        except GithubException as ghe:
            print(ghe)



#create remote repo
def init_github_remote(curpath, curdir):
    try:
        comment = curdir + ',' + cfg['misc']['COM'] + cfg['misc']['TEAM'] + ' at ' + cfg['misc']['DESC'] #form Desc
        org.create_repo(
            curdir, # name -- string
            comment, # description -- string
            cfg['base_url'] + "/" + curdir, # homepage -- string
            False, # private -- bool
            True, # has_issues -- bool
            True, # has_wiki -- bool
            True, # has_downloads -- bool
            auto_init=True,
            gitignore_template="VisualStudio")

    except GithubException as ghe:
        print(ghe)
#stuff I may need later as I expand
def general_utilities():
    limit = g.get_rate_limit()



if __name__ == "__main__":
    main()
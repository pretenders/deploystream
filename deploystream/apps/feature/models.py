class Feature(object):

    def __init__(self, id):
        self.id = id
        self.branches = []
        self.planning_info = None
        self.trees = []

    def create_hierarchy_trees(self, regexes):
        "Create hierarchy trees - one for each repo."
        pass

    def add_branch(self, branch):
        assert isinstance(branch, Branch)
        self.branches.append(branch)


class Branch(object):

    def __init__(self, repo_name, branch_name, latest_commit, plugin):
        self.parent = None
        self.children = []
        self.siblings = []  # Will be needed in the cases where we have no
                            # parent
        self.build_info = None
        self.repo_name = repo_name
        self.branch_name = branch_name
        self.latest_commit = latest_commit
        self.plugin = plugin


class PlanningInfo(object):

    def __init__(self, title, id, url, feature_type, owner, plugin):
        self.title = title
        self.id = id
        self.url = url
        self.feature_type = feature_type
        self.owner = owner
        self.plugin = plugin


class BuildInfo(object):

    def __init__(self, timestamp, result, commit, url):
        self.timestamp = timestamp
        self.result = result
        self.commit = commit
        self.url = url
